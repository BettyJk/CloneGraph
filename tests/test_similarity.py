import pytest
from src.spark_pipeline.spark_similarity import create_spark_session, load_embeddings_as_df
import tempfile
import json

def test_spark_similarity():
    spark = create_spark_session()
    # Mock embeddings
    data = {"file1.py": [1.0]*128, "file2.py": [0.9]*128}
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        f.flush()
        df = load_embeddings_as_df(spark, f.name)
    assert df.count() == 2
    spark.stop()