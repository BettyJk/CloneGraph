# How to Run CloneGraph: Step-by-Step Guide

This guide provides detailed, step-by-step instructions to set up and run the CloneGraph code clone detection system.

## Prerequisites

1. **Python 3.8+**: Ensure Python is installed. Download from [python.org](https://www.python.org/).
2. **Java 8+**: Required for Apache Spark. Download from [oracle.com](https://www.oracle.com/java/).
3. **Git**: For cloning the repository. Download from [git-scm.com](https://git-scm.com/).
4. **Optional: GPU**: For running CodeBERT/GraphCodeBERT notebooks. Requires CUDA-compatible GPU and PyTorch with CUDA support.

## Step 1: Clone the Repository

1. Open a terminal (Command Prompt, PowerShell, or Git Bash).
2. Navigate to the directory where you want to store the project:
   ```
   cd path/to/your/projects/folder
   ```
3. Clone the repository:
   ```
   git clone https://github.com/BettyJk/CloneGraph.git
   ```
4. Enter the project directory:
   ```
   cd CloneGraph
   ```

## Step 2: Set Up Python Environment

1. Create a virtual environment (recommended):
   ```
   python -m venv clonegraph_env
   ```
2. Activate the virtual environment:
   - On Windows (PowerShell):
     ```
     .\clonegraph_env\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source clonegraph_env/bin/activate
     ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Step 3: Prepare Data

1. The `data/raw/` folder contains sample data. If you want more data:
   - Add your own code files (.py, .java, .cpp) to `data/raw/`.
   - Or download datasets like BigCloneBench from [research websites](https://github.com/clonebench/BigCloneBench).

2. Ensure data files are in `data/raw/`.

## Step 4: Run the CPU Pipeline

### Step 4.1: Load and Clean Code

1. Run the code loading script:
   ```
   python -m src.extraction.load_code data/raw/
   ```
   - This loads all supported files from `data/raw/`.

### Step 4.2: Generate ASTs

1. For Python files:
   ```
   python -m src.ast_generation.python_ast data/raw/ data/ast/
   ```
2. For Java files:
   ```
   python -m src.ast_generation.java_ast data/raw/ data/ast/
   ```
3. For C++ files:
   ```
   python -m src.ast_generation.cpp_ast data/raw/ data/ast/
   ```

### Step 4.3: Generate Graph2Vec Embeddings

1. Run the Graph2Vec embedding generation:
   ```
   python -m src.embeddings.graph2vec_cpu data/ast/ data/embeddings/
   ```
   - This creates `graph2vec_embeddings.json` in `data/embeddings/`.

### Step 4.4: Run Spark Similarity Computation

1. Ensure Java is set up (JAVA_HOME environment variable).
2. Run the Spark pipeline:
   ```
   python -m src.spark_pipeline.spark_similarity data/embeddings/graph2vec_embeddings.json data/similarities/
   ```
   - This computes pairwise similarities and saves to `data/similarities/`.

### Step 4.5: Detect Clones

1. Run clone detection:
   ```
   python -m src.detection.detect_clones data/similarities/ 0.8 10 data/clones.json
   ```
   - Threshold 0.8, top 10 clones.

## Step 5: Run GPU Notebooks (Optional)

1. If you have a GPU, install additional dependencies:
   ```
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   pip install transformers
   ```

2. Open Jupyter Notebook:
   ```
   jupyter notebook
   ```

3. Navigate to `notebooks/` and open:
   - `codebert_embeddings_gpu.ipynb` for CodeBERT embeddings.
   - `graphcodebert_embeddings_gpu.ipynb` for GraphCodeBERT embeddings.

4. Run all cells in the notebook.
   - Embeddings will be saved to `data/embeddings/`.

5. Combine embeddings if needed:
   ```
   python -m src.embeddings.combine_embeddings data/embeddings/graph2vec_embeddings.json data/embeddings/codebert_embeddings.json data/embeddings/combined_embeddings.json
   ```

## Step 6: Run the Streamlit Interface

1. Launch the web app:
   ```
   streamlit run src/interface/streamlit_app.py
   ```

2. Open the provided URL in your browser (usually http://localhost:8501).

3. Upload code files or view pre-loaded data.

4. Explore ASTs, embeddings, and similarity heatmaps.

## Step 7: Run Tests

1. Run unit tests:
   ```
   python -m pytest tests/
   ```

2. Check for any failures and fix if necessary.

## Step 8: View Documentation

1. Open `README.md` for project overview.

2. Open `docs/report_etat_avancement.tex` for the progress report (requires LaTeX viewer).

## Troubleshooting

- **Spark issues**: Ensure JAVA_HOME is set correctly.
- **Import errors**: Check if all dependencies are installed.
- **GPU not detected**: Verify CUDA installation for notebooks.
- **Data empty**: Add files to `data/raw/` as described.

## Next Steps

- Experiment with different datasets.
- Tune similarity thresholds.
- Contribute improvements to the GitHub repository.

For more details, refer to the source code comments.