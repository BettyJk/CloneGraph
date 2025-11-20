from setuptools import setup, find_packages

setup(
    name="CloneGraph",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "tree-sitter==0.20.4",
        "tree-sitter-python==0.20.4",
        "tree-sitter-java==0.20.4",
        "tree-sitter-cpp==0.20.4",
        "networkx==3.2.1",
        "gensim==4.3.2",
        "pyspark==3.5.0",
        "streamlit==1.28.1",
        "pandas==2.1.4",
        "numpy==1.26.2",
        "scikit-learn==1.3.2",
        "matplotlib==3.8.2",
        "seaborn==0.13.0",
        "pytest==7.4.3",
        "javalang==0.13.0",
        "clang==16.0.6"
    ],
    entry_points={
        "console_scripts": [
            "clonegraph-extract = extraction.load_code:main",
            "clonegraph-ast = ast_generation.python_ast:main",
            "clonegraph-embed = embeddings.graph2vec_cpu:main",
            "clonegraph-spark = spark_pipeline.spark_similarity:main",
            "clonegraph-detect = detection.detect_clones:main",
        ],
    },
)