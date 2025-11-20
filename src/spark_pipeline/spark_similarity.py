from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import Normalizer
from pyspark.sql.functions import udf, col, explode, arrays_zip
from pyspark.sql.types import ArrayType, DoubleType, StructType, StructField, StringType
import json
import os

def create_spark_session():
    return SparkSession.builder \
        .appName("CloneGraph Similarity") \
        .getOrCreate()

def load_embeddings_as_df(spark, embeddings_file):
    """
    Load embeddings JSON as Spark DataFrame.
    """
    with open(embeddings_file, 'r') as f:
        data = json.load(f)
    
    rows = [(k, Vectors.dense(v)) for k, v in data.items()]
    schema = StructType([
        StructField("id", StringType(), True),
        StructField("vector", Vectors.dense.__class__.__name__, True)
    ])
    return spark.createDataFrame(rows, schema)

def compute_cosine_similarity(df):
    """
    Compute pairwise cosine similarities.
    """
    normalizer = Normalizer(inputCol="vector", outputCol="norm_vector")
    df_norm = normalizer.transform(df)
    
    # Cross join for all pairs
    df1 = df_norm.withColumnRenamed("id", "id1").withColumnRenamed("norm_vector", "vec1")
    df2 = df_norm.withColumnRenamed("id", "id2").withColumnRenamed("norm_vector", "vec2")
    
    pairs = df1.crossJoin(df2).filter(col("id1") < col("id2"))
    
    # Cosine similarity UDF
    def cosine_sim(vec1, vec2):
        return float(vec1.dot(vec2))
    
    cosine_udf = udf(cosine_sim, DoubleType())
    similarities = pairs.withColumn("similarity", cosine_udf(col("vec1"), col("vec2")))
    
    return similarities.select("id1", "id2", "similarity")

def save_similarities(similarities, output_dir):
    """
    Save similarities to JSON.
    """
    os.makedirs(output_dir, exist_ok=True)
    similarities.write.json(os.path.join(output_dir, "similarities"))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python spark_similarity.py <embeddings_file> <output_dir>")
        sys.exit(1)
    
    spark = create_spark_session()
    df = load_embeddings_as_df(spark, sys.argv[1])
    sim_df = compute_cosine_similarity(df)
    save_similarities(sim_df, sys.argv[2])
    spark.stop()