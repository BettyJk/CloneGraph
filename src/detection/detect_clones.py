import json
import os
from pyspark.sql import SparkSession

def detect_clones(similarities_dir, threshold=0.8, top_k=10):
    """
    Detect clones from similarities.
    """
    spark = SparkSession.builder.appName("Detect Clones").getOrCreate()
    
    # Load similarities
    sim_df = spark.read.json(similarities_dir)
    
    # Filter by threshold
    clones = sim_df.filter(col("similarity") >= threshold).orderBy(col("similarity").desc()).limit(top_k)
    
    # Collect results
    results = clones.collect()
    clones_list = [(row.id1, row.id2, row.similarity) for row in results]
    
    spark.stop()
    return clones_list

def save_clones(clones, output_file):
    """
    Save clones to JSON.
    """
    with open(output_file, 'w') as f:
        json.dump(clones, f)

if __name__ == "__main__":
    import sys
    from pyspark.sql.functions import col
    if len(sys.argv) != 4:
        print("Usage: python detect_clones.py <similarities_dir> <threshold> <output_file>")
        sys.exit(1)
    
    threshold = float(sys.argv[2])
    clones = detect_clones(sys.argv[1], threshold)
    save_clones(clones, sys.argv[3])