import streamlit as st
import json
import os
from extraction.load_code import load_code_files
from extraction.clean_code import clean_files
from ast_generation.python_ast import parse_python_to_ast
from embeddings.graph2vec_cpu import ast_to_graph, graph2vec_embedding
from detection.visualization import plot_similarity_heatmap
import matplotlib.pyplot as plt

st.title("CloneGraph: Code Clone Detector")

uploaded_files = st.file_uploader("Upload code files", accept_multiple_files=True, type=['py', 'java', 'cpp'])

if uploaded_files:
    files = {}
    for uploaded_file in uploaded_files:
        files[uploaded_file.name] = uploaded_file.read().decode('utf-8')
    
    cleaned = clean_files(files)
    
    st.header("Cleaned Code")
    for name, code in cleaned.items():
        st.subheader(name)
        st.code(code, language='python' if name.endswith('.py') else 'java' if name.endswith('.java') else 'cpp')
    
    st.header("ASTs")
    asts = {}
    for name, code in cleaned.items():
        if name.endswith('.py'):
            ast = parse_python_to_ast(code)
            asts[name] = ast
            st.subheader(name)
            st.json(ast)
    
    st.header("Embeddings")
    embeddings = {}
    for name, ast in asts.items():
        G = ast_to_graph(ast)
        emb = graph2vec_embedding(G)
        embeddings[name] = emb.tolist()
        st.subheader(name)
        st.write(emb.tolist()[:10])  # First 10 dims
    
    # Mock similarities for demo
    similarities = []
    names = list(embeddings.keys())
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            sim = sum(a*b for a,b in zip(embeddings[names[i]], embeddings[names[j]])) / (sum(a**2 for a in embeddings[names[i]])**0.5 * sum(b**2 for b in embeddings[names[j]])**0.5)
            similarities.append([names[i], names[j], sim])
    
    st.header("Similarity Heatmap")
    fig, ax = plt.subplots()
    # Simple plot
    ax.bar(range(len(similarities)), [s[2] for s in similarities])
    st.pyplot(fig)