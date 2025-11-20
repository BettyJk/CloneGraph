from pyspark.sql import SparkSession

def get_spark_config():
    """
    Get Spark configuration for CPU.
    """
    return {
        "spark.master": "local[*]",
        "spark.executor.memory": "2g",
        "spark.driver.memory": "2g"
    }

def init_spark_session(config=None):
    """
    Initialize Spark session with config.
    """
    builder = SparkSession.builder.appName("CloneGraph")
    if config:
        for k, v in config.items():
            builder = builder.config(k, v)
    return builder.getOrCreate()

def stop_spark_session(spark):
    """
    Stop Spark session.
    """
    spark.stop()