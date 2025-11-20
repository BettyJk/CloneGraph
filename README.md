# CloneGraph: Multi-Language Code Clone Detector

CloneGraph is a production-ready system for detecting code clones across multiple programming languages (Python, Java, C++) using a combination of AST-based graph representations, embeddings (Graph2Vec, CodeBERT, GraphCodeBERT), and distributed similarity computation with Apache Spark.

## Features

- **Multi-language support**: Python, Java, C++
- **AST extraction**: Using Tree-sitter for accurate syntax trees
- **Embeddings**: CPU-safe Graph2Vec, GPU-optional CodeBERT/GraphCodeBERT
- **Distributed processing**: Spark for large-scale similarity computation
- **Visualization**: Streamlit interface for interactive clone detection

## Architecture

The system consists of the following modules:

1. **Extraction**: Load and clean raw code files
2. **AST Generation**: Parse code into Abstract Syntax Trees using Tree-sitter
3. **Embeddings**: Generate vector representations (Graph2Vec on CPU, CodeBERT on GPU)
4. **Spark Pipeline**: Distributed cosine similarity computation
5. **Detection**: Identify and rank clone pairs
6. **Interface**: Streamlit web app for visualization

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/CloneGraph.git
   cd CloneGraph
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. For Spark support, ensure Java is installed and set JAVA_HOME.

## Usage

### CPU-only Pipeline

Run the complete pipeline on CPU:

```bash
python -m src.extraction.load_code data/raw/
python -m src.ast_generation.python_ast data/raw/ data/ast/
python -m src.embeddings.graph2vec_cpu data/ast/ data/embeddings/
python -m src.spark_pipeline.spark_similarity data/embeddings/
python -m src.detection.detect_clones
```

### GPU Notebooks

For CodeBERT embeddings (requires GPU):

1. Open `notebooks/codebert_embeddings_gpu.ipynb`
2. Run the notebook to generate embeddings

For GraphCodeBERT:

1. Open `notebooks/graphcodebert_embeddings_gpu.ipynb`
2. Run the notebook

### Streamlit Interface

Launch the web interface:

```bash
streamlit run src/interface/streamlit_app.py
```

Upload code files, view ASTs, embeddings, and clone similarity heatmaps.

## Project Status

- **Completed**: 80% (extraction, AST generation, Graph2Vec, Spark pipeline, basic detection)
- **In Progress**: 15% (CodeBERT/GraphCodeBERT notebooks, advanced visualization)
- **Remaining**: 5% (final testing, documentation polish)

**Risks**: GPU dependency for deep learning embeddings; mitigated by CPU fallbacks.

**Next Steps**: Complete notebooks, add more tests, optimize Spark jobs.

## Dependencies

- tree-sitter
- networkx
- gensim
- pyspark
- streamlit
- transformers (for notebooks)
- torch (for notebooks)

## Testing

Run tests:

```bash
python -m pytest tests/
```

## Documentation

See `docs/report_etat_avancement.tex` for the detailed progress report (in French).