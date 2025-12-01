# Complete CloneGraph Setup & Execution Guide

Follow these steps exactly in order to make CloneGraph work completely.

---

## **PHASE 1: PREREQUISITES & INSTALLATION**

### **Step 1: Install Required Software**

#### Option A: Windows (PowerShell)

1. **Install Python 3.8+**
   - Download from https://www.python.org/downloads/
   - **IMPORTANT**: Check "Add Python to PATH" during installation
   - Verify:
     ```powershell
     python --version
     ```

2. **Install Java**
   - Download JDK from https://www.oracle.com/java/technologies/downloads/
   - Install and note installation path (e.g., `C:\Program Files\Java\jdk-21`)
   - Set JAVA_HOME environment variable:
     ```powershell
     [Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\Program Files\Java\jdk-21", "User")
     ```
   - Verify:
     ```powershell
     java -version
     ```

3. **Install Git**
   - Download from https://git-scm.com/download/win
   - Install with default options

#### Option B: macOS

```bash
# Install Homebrew first if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python@3.9 java git
```

---

### **Step 2: Clone and Navigate to Project**

```powershell
# Create a projects folder
mkdir C:\Projects
cd C:\Projects

# Clone the repository
git clone https://github.com/BettyJk/CloneGraph.git
cd CloneGraph
```

---

### **Step 3: Set Up Python Virtual Environment**

```powershell
# Create virtual environment
python -m venv clonegraph_env

# Activate it (Windows PowerShell)
.\clonegraph_env\Scripts\activate

# Verify activation (you should see (clonegraph_env) prefix)
python --version
```

---

### **Step 4: Install Dependencies**

```powershell
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# Verify tree-sitter is installed
python -c "import tree_sitter; print('Tree-sitter installed')"
```

**If you get errors with tree-sitter:**
```powershell
pip install --no-cache-dir tree-sitter==0.20.4
pip install tree-sitter-python==0.20.4
```

---

## **PHASE 2: PREPARE YOUR DATA**

### **Step 5: Add Code Files to Analyze**

The project already has sample files. To add your own:

1. **Create a test folder** (optional):
   ```powershell
   mkdir data\raw\my_project
   ```

2. **Add code files** (.py, .java, .cpp):
   - Copy your Python files to `data\raw\`
   - Copy your Java files to `data\raw\`
   - Copy your C++ files to `data\raw\`

3. **Example**: If you have a file `calculator.py`, put it in:
   ```
   data/raw/calculator.py
   ```

---

## **PHASE 3: RUN THE PIPELINE**

### **Step 6: Extract and Clean Code**

```powershell
# Navigate to project root
cd C:\Projects\CloneGraph

# Make sure virtual environment is activated
# (you should see (clonegraph_env) in terminal)

# Load code files
python -m src.extraction.load_code data\raw\

# Expected output:
# Loaded X files
```

---

### **Step 7: Generate ASTs (Abstract Syntax Trees)**

Run this for each language you have:

#### **For Python Files:**
```powershell
python -m src.ast_generation.python_ast data\raw\ data\ast\
```

#### **For Java Files:**
```powershell
python -m src.ast_generation.java_ast data\raw\ data\ast\
```

#### **For C++ Files:**
```powershell
python -m src.ast_generation.cpp_ast data\raw\ data\ast\
```

**What happens**: Creates JSON files in `data/ast/` showing code structure

---

### **Step 8: Generate Graph2Vec Embeddings (CPU)**

```powershell
python -m src.embeddings.graph2vec_cpu data\ast\ data\embeddings\
```

**Output**: Creates `data/embeddings/graph2vec_embeddings.json` with 128-dimensional vectors

**If it fails:**
- Make sure `data/ast/` contains JSON files from Step 7
- Check that embeddings directory exists:
  ```powershell
  mkdir data\embeddings -Force
  ```

---

### **Step 9: Compute Similarity with Spark**

```powershell
# Create output directory
mkdir data\similarities -Force

# Run Spark pipeline
python -m src.spark_pipeline.spark_similarity data\embeddings\graph2vec_embeddings.json data\similarities\
```

**Expected output**:
```
Computed X similarity pairs
```

**If Spark fails:**
```powershell
# Verify Java is accessible
java -version

# If error, restart terminal and try again
```

---

### **Step 10: Detect and Rank Clones**

```powershell
# Create output directory
mkdir data\output -Force

# Run detection (threshold 0.8, top 10 clones)
python -m src.detection.detect_clones data\similarities\ 0.8 10 data\output\clones.json
```

**Output**: Creates `data/output/clones.json` with ranked clone pairs

---

## **PHASE 4: VIEW RESULTS**

### **Step 11: Visualize with Streamlit (Optional but Recommended)**

```powershell
# Make sure you're in the project root with venv activated
streamlit run src\interface\streamlit_app.py
```

**What happens:**
- Browser opens automatically (usually http://localhost:8501)
- Upload your code files
- See ASTs, embeddings, and similarity heatmaps

---

## **PHASE 5: GPU EMBEDDINGS (Optional - For Better Accuracy)**

### **Step 12: GPU Embeddings with CodeBERT**

Only do this if you have an NVIDIA GPU.

```powershell
# Install GPU dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers

# Install Jupyter
pip install jupyter

# Start Jupyter
jupyter notebook
```

1. Navigate to `notebooks/codebert_embeddings_gpu.ipynb`
2. Run all cells
3. Embeddings saved to `data/embeddings/codebert_embeddings.json`

---

## **PHASE 6: TEST & VERIFY**

### **Step 13: Run Tests**

```powershell
# Install pytest if not installed
pip install pytest

# Run all tests
python -m pytest tests\ -v
```

**Expected**: All tests should pass

---

## **QUICK REFERENCE - COMPLETE WORKFLOW**

```powershell
# 1. Activate environment
.\clonegraph_env\Scripts\activate

# 2. Load code
python -m src.extraction.load_code data\raw\

# 3. Generate ASTs (do for each language)
python -m src.ast_generation.python_ast data\raw\ data\ast\

# 4. Generate embeddings
python -m src.embeddings.graph2vec_cpu data\ast\ data\embeddings\

# 5. Compute similarities
mkdir data\similarities -Force
python -m src.spark_pipeline.spark_similarity data\embeddings\graph2vec_embeddings.json data\similarities\

# 6. Detect clones
mkdir data\output -Force
python -m src.detection.detect_clones data\similarities\ 0.8 10 data\output\clones.json

# 7. View results
streamlit run src\interface\streamlit_app.py
```

---

## **TROUBLESHOOTING**

### **Problem: "Python not found"**
```powershell
# Make sure Python is in PATH
python --version

# If not, reinstall Python with "Add to PATH" checked
```

### **Problem: Virtual environment won't activate**
```powershell
# Try this command instead
& ".\clonegraph_env\Scripts\Activate.ps1"

# If error about execution policy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Problem: "No module named tree_sitter"**
```powershell
pip install --upgrade tree-sitter
pip install tree-sitter-python
```

### **Problem: Spark fails**
```powershell
# Check Java is working
java -version

# Set Java home manually if needed
$env:JAVA_HOME = "C:\Program Files\Java\jdk-21"

# Retry Spark command
```

### **Problem: "Permission denied" on files**
```powershell
# Windows usually doesn't have this, but try:
# Run PowerShell as Administrator
```

### **Problem: Out of memory**
```powershell
# Reduce data size - analyze fewer files
# Or use less data from data\raw\
```

---

## **SUCCESS INDICATORS**

✅ Step 6 shows "Loaded X files"  
✅ Step 7 creates JSON files in `data/ast/`  
✅ Step 8 creates `graph2vec_embeddings.json`  
✅ Step 9 completes without errors  
✅ Step 10 creates `clones.json`  
✅ Step 11 opens Streamlit in browser  
✅ Step 13 all tests pass  

---

## **NEXT STEPS**

1. **Analyze your own code** - Add files to `data/raw/`
2. **Tune similarity threshold** - Change 0.8 to 0.7 for more clones
3. **Use GPU embeddings** - Follow Phase 5 for better accuracy
4. **Export results** - Check `data/output/clones.json`

---

**Need Help?** Check the README.md or HOW_TO_RUN.md files.