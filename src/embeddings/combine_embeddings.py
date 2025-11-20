import json
import numpy as np
import os

def combine_embeddings(graph2vec_file, codebert_file=None, output_file=None):
    """
    Combine Graph2Vec with CodeBERT embeddings if available.
    """
    with open(graph2vec_file, 'r') as f:
        g2v_emb = json.load(f)
    
    combined = {}
    for key, vec in g2v_emb.items():
        combined[key] = np.array(vec)
    
    if codebert_file and os.path.exists(codebert_file):
        with open(codebert_file, 'r') as f:
            cb_emb = json.load(f)
        for key, vec in cb_emb.items():
            if key in combined:
                combined[key] = np.concatenate([combined[key], np.array(vec)])
    
    # Save
    if output_file:
        combined_serial = {k: v.tolist() for k, v in combined.items()}
        with open(output_file, 'w') as f:
            json.dump(combined_serial, f)
    
    return combined

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python combine_embeddings.py <graph2vec_file> <codebert_file> <output_file>")
        sys.exit(1)
    codebert = sys.argv[2] if len(sys.argv) > 2 else None
    output = sys.argv[3] if len(sys.argv) > 3 else None
    combine_embeddings(sys.argv[1], codebert, output)