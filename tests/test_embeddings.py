import pytest
import json
from src.embeddings.graph2vec_cpu import ast_to_graph, graph2vec_embedding
from src.ast_generation.python_ast import parse_python_to_ast

def test_graph2vec():
    code = "def hello(): pass"
    ast = parse_python_to_ast(code)
    G = ast_to_graph(ast)
    emb = graph2vec_embedding(G)
    assert len(emb) == 128