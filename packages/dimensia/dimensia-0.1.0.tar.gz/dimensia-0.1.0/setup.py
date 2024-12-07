from setuptools import setup, find_packages

setup(
    name="dimensia",
    version="0.1.0",
    description="A lightweight vector database for storage, retrieval, and management of high-dimensional vector data.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Aniruddha Salve",
    author_email="salveaniruddha180@gmail.com",
    url="https://github.com/aniruddhasalve/dimensia",
    packages=find_packages(),
    install_requires=[
        "numpy==1.26.4",
        "torch==2.2.2",
        "sentence-transformers==3.3.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    include_package_data=True,
)
