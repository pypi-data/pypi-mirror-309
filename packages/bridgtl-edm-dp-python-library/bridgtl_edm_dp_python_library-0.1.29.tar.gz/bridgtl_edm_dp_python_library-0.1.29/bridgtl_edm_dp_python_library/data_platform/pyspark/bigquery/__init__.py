import os

from pyspark.sql.connect.session import SparkSession


def read(statement: str, session: SparkSession, partition: int = 32):
    return session.read.format("bigquery") \
        .option("viewsEnabled", "true") \
        .option("parentProject", os.getenv("DEFAULT_GCP_PROJECT")) \
        .option("materializationProject", os.getenv("DEFAULT_GCP_MATERIALIZATION_PROJECT")) \
        .option("materializationDataset", os.getenv("DEFAULT_GCP_MATERIALIZATION_DATASET")) \
        .load(statement) \
        .repartition(partition) \
        .cache()
