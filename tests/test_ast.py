import pytest
from src.ast_generation.python_ast import parse_python_to_ast

def test_python_ast():
    code = "def hello(): pass"
    ast = parse_python_to_ast(code)
    assert ast['type'] == 'module'
    assert len(ast['children']) > 0