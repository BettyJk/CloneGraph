import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
import os

def plot_similarity_heatmap(similarities_file, output_file=None):
    """
    Plot similarity heatmap.
    """
    # Load similarities (assuming JSON list of [id1, id2, sim])
    with open(similarities_file, 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data, columns=['id1', 'id2', 'similarity'])
    
    # Pivot for heatmap
    pivot = df.pivot(index='id1', columns='id2', values='similarity').fillna(0)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot, annot=True, cmap='viridis')
    plt.title('Code Clone Similarity Heatmap')
    
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()

def plot_embedding_scatter(embeddings_file, output_file=None):
    """
    Plot embeddings in 2D (using PCA if high dim).
    """
    from sklearn.decomposition import PCA
    
    with open(embeddings_file, 'r') as f:
        data = json.load(f)
    
    ids = list(data.keys())
    vectors = list(data.values())
    
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(vectors)
    
    plt.figure()
    plt.scatter(reduced[:, 0], reduced[:, 1])
    for i, id_ in enumerate(ids):
        plt.annotate(id_, (reduced[i, 0], reduced[i, 1]))
    
    plt.title('Embedding Scatter Plot')
    
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python visualization.py <similarities_file> <output_file>")
        sys.exit(1)
    plot_similarity_heatmap(sys.argv[1], sys.argv[2])