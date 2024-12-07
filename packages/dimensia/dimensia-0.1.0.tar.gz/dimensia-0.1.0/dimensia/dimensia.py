import os
import pickle
from concurrent.futures import ThreadPoolExecutor, as_completed
from sentence_transformers import SentenceTransformer
from dimensia.exceptions import (
    CollectionAlreadyExistsError, CollectionNotFoundError, DocumentAlreadyExistsError,
    DatabaseLoadError, DatabaseSaveError, EmbeddingModelNotSetError, InvalidVectorError,
    DocumentNotFoundError, InvalidDatabasePathError
)
from dimensia.hnsw import HNSW
from dimensia.utils import ensure_directory_exists
import numpy as np

class Dimensia:
    """
    Dimensia is a high-performance vector database designed for efficient semantic search and storage
    of vector embeddings. It supports adding documents, performing searches, and managing collections
    using a customizable embedding model.

    Attributes:
        db_path (str): The path to the database directory or file.
        collections (dict): A dictionary holding all the collections and their associated data.
        embedding_model (SentenceTransformer): The model used for generating document embeddings.
    """

    def __init__(self, db_path=None):
        """
        Initializes the Dimensia instance by loading or creating the database at the given path.

        Args:
            db_path (str, optional): Path to the database directory or file. Defaults to 'dimensia_data'.
            model_name (str, optional): The name of the sentence transformer model to use for embeddings.
        """
        self.db_path = db_path or "dimensia_data"
        self.collections = {}
        self.embedding_model = None
        self.set_embedding_model()
        self._load_db()

    def _load_db(self):
        """
        Loads the database from the specified path. If the path is a directory, it will look for
        'data.dim' inside. If the path is a file, it will use that directly. If the database file
        doesn't exist, it will create a new one.

        Raises:
            InvalidDatabasePathError: If the database path is invalid.
            DatabaseLoadError: If an error occurs during loading the database.
        """
        ensure_directory_exists(self.db_path)

        if os.path.isdir(self.db_path):
            db_file = os.path.join(self.db_path, "data.dim")
            if not os.path.exists(db_file):
                self._save_db()
                print(f"Database file created at: {db_file}")

            try:
                with open(db_file, "rb") as f:
                    self.collections = pickle.load(f)
            except Exception as e:
                raise DatabaseLoadError(f"Error loading database: {str(e)}")
        elif os.path.isfile(self.db_path):
            db_file = self.db_path
            try:
                with open(db_file, "rb") as f:
                    self.collections = pickle.load(f)
            except Exception as e:
                raise DatabaseLoadError(f"Error loading database: {str(e)}")
        else:
            raise InvalidDatabasePathError(f"Invalid database path: {self.db_path}")

    def _save_db(self):
        """
        Saves the current state of the database to the 'data.dim' file in the specified database path.

        Raises:
            PermissionError: If there are permission issues when writing to the database file.
            DatabaseSaveError: If an error occurs during saving the database.
        """
        db_file = os.path.join(self.db_path, "data.dim")
        try:
            with open(db_file, "wb") as f:
                pickle.dump(self.collections, f)
        except PermissionError:
            print(f"Permission denied when trying to write to {db_file}. Please check file permissions.")
            raise
        except Exception as e:
            raise DatabaseSaveError(f"Error saving database: {str(e)}")

    def set_embedding_model(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        """
        Sets the embedding model used for generating vector embeddings for documents and queries.
        Initializes the model from sentence_transformers.
        """
        try:
            self.embedding_model = SentenceTransformer(model_name)
        except Exception as e:
            raise ValueError(f"Error while setting embedding model: {str(e)}")

    def get_collections(self):
        """
        Returns the list of all collections in the database.

        Returns:
            list: A list of collection names.
        """
        return list(self.collections.keys())

    def create_collection(self, collection_name, metadata_schema=None):
        """
        Creates a new collection with the specified name and metadata schema. If the collection already exists,
        it raises a `CollectionAlreadyExistsError`.

        Args:
            collection_name (str): The name of the collection to create.
            metadata_schema (dict, optional): The schema defining metadata structure for the collection.
                                          Defaults to an empty dictionary.
        Raises:
            CollectionAlreadyExistsError: If a collection with the same name already exists.
        """
        if collection_name in self.collections:
            raise CollectionAlreadyExistsError(f"Collection '{collection_name}' already exists.")
        self.collections[collection_name] = {
            "metadata_schema": metadata_schema or {},
            "documents": [],
            "index": HNSW(M=16, ef_construction=200, ef_search=50, space="cosine")
        }
        self._save_db()

    def add_documents(self, collection_name, documents):
        """
        Adds a list of documents to the specified collection. If a document with the same ID already exists,
        it is not added again.

        Args:
            collection_name (str): The name of the collection to add documents to.
            documents (list): A list of dictionaries representing the documents to add.

        Raises:
            CollectionNotFoundError: If the collection does not exist.
            DocumentAlreadyExistsError: If a document with the same ID already exists in the collection.
        """
        if collection_name not in self.collections:
            raise CollectionNotFoundError(f"Collection '{collection_name}' not found.")
        collection = self.collections[collection_name]

        existing_docs = {doc['id'] for doc in collection['documents']}
        new_documents = [doc for doc in documents if doc['id'] not in existing_docs]

        if not new_documents:
            print("No new documents to add.")
            return

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self._process_document, doc, collection) for doc in new_documents}
            for future in as_completed(futures):
                future.result()

        self._save_db()

    def _process_document(self, doc, collection):
        """
        Processes a document by generating its embedding and adding it to the collection's index.

        Args:
            doc (dict): A dictionary representing the document to process.
            collection (dict): The collection to which the document belongs.

        Raises:
            DocumentAlreadyExistsError: If a document with the same ID already exists in the collection.
        """
        if self.embedding_model is None:
            raise EmbeddingModelNotSetError("Embedding model is not set.")

        # Check if the document already exists
        existing_doc = next((existing for existing in collection['documents'] if existing['id'] == doc['id']), None)
        if existing_doc:
            raise DocumentAlreadyExistsError(f"Document with ID '{doc['id']}' already exists.")

        vector = self.generate_embedding(doc['content'])
        if vector is None:
            raise InvalidVectorError(f"Generated an invalid vector for document with ID '{doc['id']}'")

        doc['vector'] = vector
        collection['documents'].append(doc)
        collection['index'].add(vector, doc['id'])

    def generate_embedding(self, text):
        """
        Generates the vector embedding for a given text using the specified embedding model.

        Args:
            text (str): The input text to generate embedding for.

        Returns:
            list: The vector representation of the text.

        Raises:
            EmbeddingModelNotSetError: If the embedding model is not set.
        """
        if self.embedding_model is None:
            raise EmbeddingModelNotSetError("Embedding model is not set.")
        return self.embedding_model.encode(text).tolist()

    def _normalize_vector(self, vector):
        """
        Normalizes a vector (scales it to unit length).

        Args:
            vector (list): The input vector to normalize.

        Returns:
            list: The normalized vector.

        Raises:
            InvalidVectorError: If the vector cannot be normalized.
        """
        norm = np.linalg.norm(vector)
        if norm == 0:
            raise InvalidVectorError(f"Cannot normalize a zero-length vector: {vector}")
        return (vector / norm).tolist()

    def _cosine_similarity(self, vec1, vec2):
        """
        Calculates the cosine similarity between two vectors.

        Args:
            vec1 (list): The first vector.
            vec2 (list): The second vector.

        Returns:
            float: The cosine similarity between the two vectors.
        """
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        if norm_vec1 == 0 or norm_vec2 == 0:
            return 0.0
        return dot_product / (norm_vec1 * norm_vec2)

    def search(self, query, collection_name, top_k=5):
        """
        Searches for the top `k` documents in the specified collection based on semantic similarity to the query.

        Args:
            query (str): The query string to search for.
            collection_name (str): The name of the collection to search within.
            top_k (int, optional): The number of top documents to retrieve. Defaults to 5.

        Returns:
            list: A list of the top `k` documents sorted by similarity score.
        """
        if collection_name not in self.collections:
            raise CollectionNotFoundError(f"Collection '{collection_name}' not found.")

        collection = self.collections[collection_name]
        query_vector = self.generate_embedding(query)
        query_vector = self._normalize_vector(query_vector)

        # Perform search
        results = []
        for doc in collection['documents']:
            doc_vector = doc['vector']
            cosine_sim = self._cosine_similarity(query_vector, doc_vector)
            results.append((cosine_sim, doc))

        # Sort results by cosine similarity and return the top k results
        results.sort(reverse=True, key=lambda x: x[0])
        return results[:top_k]

    def get_collection_schema(self, collection_name):
        """
        Retrieves the full schema for the specified collection, including the documents and indexing structure.

        Args:
            collection_name (str): The name of the collection to retrieve the schema for.

        Returns:
            dict: The full schema of the collection, including documents and indexing structure.

        Raises:
            CollectionNotFoundError: If the collection does not exist.
        """
        if collection_name not in self.collections:
            raise CollectionNotFoundError(f"Collection '{collection_name}' not found.")

        collection = self.collections[collection_name]
        collection_schema = {
            "metadata_schema": collection["metadata_schema"],
            "documents_count": len(collection["documents"]),
            "index_type": type(collection["index"]).__name__,
            "index_params": {
                "M": collection["index"].M,
                "ef_construction": collection["index"].ef_construction,
                "ef_search": collection["index"].ef_search,
                "space": collection["index"].space
            }
        }

        return collection_schema


    def get_vector_size(self):
        """
        Retrieves the size of the vectors generated by the embedding model.

        Returns:
            int: The size of the embedding vector.

        Raises:
            EmbeddingModelNotSetError: If the embedding model is not set.
        """
        if self.embedding_model is None:
            raise EmbeddingModelNotSetError("Embedding model is not set.")
        return len(self.embedding_model.encode("test"))

    def get_document(self, collection_name, document_id):
        """
        Retrieves a document by its ID from the specified collection.

        Args:
            collection_name (str): The name of the collection to retrieve the document from.
            document_id (str): The ID of the document to retrieve.

        Returns:
            dict: The document with the specified ID.

        Raises:
            CollectionNotFoundError: If the collection does not exist.
            DocumentNotFoundError: If the document does not exist in the collection.
        """
        if collection_name not in self.collections:
            raise CollectionNotFoundError(f"Collection '{collection_name}' not found.")

        collection = self.collections[collection_name]

        # Search for the document by ID
        document = next((doc for doc in collection['documents'] if doc['id'] == document_id), None)

        if document is None:
            raise DocumentNotFoundError(
                f"Document with ID '{document_id}' not found in collection '{collection_name}'.")

        return document
