import networkx as nx
import json
import os
from gensim.models import Word2Vec
import numpy as np

def ast_to_graph(ast_json):
    """
    Convert AST JSON to NetworkX graph.
    """
    G = nx.DiGraph()
    def add_nodes(node, parent=None):
        node_id = f"{node['type']}_{id(node)}"
        G.add_node(node_id, label=node['type'])
        if parent:
            G.add_edge(parent, node_id)
        for child in node.get('children', []):
            add_nodes(child, node_id)
    add_nodes(ast_json)
    return G

def weisfeiler_lehman_subtrees(G, iterations=2):
    """
    Generate Weisfeiler-Lehman subtree patterns.
    """
    labels = {node: G.nodes[node]['label'] for node in G.nodes()}
    subtrees = []
    for _ in range(iterations):
        new_labels = {}
        for node in G.nodes():
            neighbor_labels = sorted([labels[nei] for nei in G.neighbors(node)])
            new_labels[node] = f"{labels[node]}_{'_'.join(neighbor_labels)}"
        labels = new_labels
        subtrees.append(list(labels.values()))
    return subtrees

def graph2vec_embedding(G):
    """
    Generate Graph2Vec embedding.
    Simplified: use WL subtrees and Word2Vec.
    """
    subtrees = weisfeiler_lehman_subtrees(G)
    # Flatten subtrees
    sentences = [subtrees[i] for i in range(len(subtrees))]
    model = Word2Vec(sentences, vector_size=128, window=5, min_count=1, sg=1)
    # Average vectors
    vectors = [model.wv[word] for word in model.wv.index_to_key]
    return np.mean(vectors, axis=0) if vectors else np.zeros(128)

def generate_embeddings(ast_dir, output_dir):
    """
    Generate embeddings for all AST files.
    """
    os.makedirs(output_dir, exist_ok=True)
    embeddings = {}
    for root, _, files in os.walk(ast_dir):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(root, file), 'r') as f:
                    ast = json.load(f)
                G = ast_to_graph(ast)
                emb = graph2vec_embedding(G)
                rel_path = os.path.relpath(os.path.join(root, file), ast_dir)
                embeddings[rel_path] = emb.tolist()
    
    with open(os.path.join(output_dir, 'graph2vec_embeddings.json'), 'w') as f:
        json.dump(embeddings, f)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python graph2vec_cpu.py <ast_dir> <output_dir>")
        sys.exit(1)
    generate_embeddings(sys.argv[1], sys.argv[2])