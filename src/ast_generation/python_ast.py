import tree_sitter_python as tspython
from tree_sitter import Language, Parser
import json
import os

PY_LANGUAGE = Language(tspython.language())

def parse_python_to_ast(code):
    """
    Parse Python code to AST using Tree-sitter.
    Returns JSON representation.
    """
    parser = Parser(PY_LANGUAGE)
    tree = parser.parse(bytes(code, "utf8"))
    return tree_to_json(tree.root_node)

def tree_to_json(node):
    """
    Convert tree-sitter node to JSON.
    """
    return {
        "type": node.type,
        "start": node.start_point,
        "end": node.end_point,
        "children": [tree_to_json(child) for child in node.children]
    }

def generate_asts(files, output_dir):
    """
    Generate ASTs for files and save as JSON.
    """
    os.makedirs(output_dir, exist_ok=True)
    for filename, content in files.items():
        if filename.endswith('.py'):
            ast = parse_python_to_ast(content)
            out_path = os.path.join(output_dir, filename.replace('.py', '.json'))
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, 'w') as f:
                json.dump(ast, f, indent=2)

if __name__ == "__main__":
    import sys
    from extraction.load_code import load_code_files
    from extraction.clean_code import clean_files
    
    if len(sys.argv) != 3:
        print("Usage: python python_ast.py <input_dir> <output_dir>")
        sys.exit(1)
    
    files = load_code_files(sys.argv[1])
    cleaned = clean_files(files)
    generate_asts(cleaned, sys.argv[2])