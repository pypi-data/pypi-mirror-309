import os
import socket
from typing import List

from pyspark import SparkConf
from pyspark.sql import SparkSession

from bridgtl_edm_dp_python_library.common import get_env_or_raise


class KubernetesSparkSession:
    def __init__(
            self,
            name: str,
            master: str | None = None,
            spark_ui_port: int = 4040,
            image: str = "registry.gitlab.com/bridigital/bgd/dp/bridgtl-bgd-dp-k8s-spark:v1.0.2",
            image_pull_policy: str = "IfNotPresent",

            google_service_account_path: str = None,

            executor_instances: int | None = None,
            executor_cores: int | None = None,
            executor_memory: str | None = None,

            jars: List[str] | None = None,
            packages: List[str] | None = None,

            config: dict | None = None
    ):
        self.name = name
        self.master = master or get_env_or_raise("KUBERNETES_SPARK_MASTER")
        self.spark_ui_port = spark_ui_port

        self.kubernetes_spark_image = image or get_env_or_raise("KUBERNETES_SPARK_IMAGE")
        self.kubernetes_spark_image_pull_policy = image_pull_policy

        self.google_service_account_path = google_service_account_path

        # Using the provided arguments or default values
        self.executor_instances = executor_instances or 1
        self.executor_cores = executor_cores or 1
        self.executor_memory = executor_memory or "4g"

        # Adding default jars if not provided
        self.jars = [
            "https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-hadoop3-latest.jar",
            "https://storage.googleapis.com/spark-lib/bigquery/spark-3.5-bigquery-0.40.0.jar",
        ]
        self.jars = self.jars + (jars or [])

        self.packages = [
            "com.microsoft.sqlserver:mssql-jdbc:12.6.3.jre11",
        ]
        self.packages = self.packages + (packages or [])

        # Initialize configuration with defaults and environment variables
        self.config = config or {}
        self._initialize_default_config()

    def _initialize_default_config(self):
        self.config["spark.bigquery.viewsEnabled"] = "true"
        self.config["spark.kubernetes.node.selector.node-type"] = "spot"
        self.config["spark.sql.sources.partitionOverwriteMode"] = "dynamic"

        self.config["spark.ui.port"] = self.spark_ui_port

        self.config["spark.kubernetes.container.image"] = self.kubernetes_spark_image
        self.config["spark.kubernetes.container.image.pullPolicy"] = self.kubernetes_spark_image_pull_policy

        self.config["spark.kubernetes.namespace"] = "jupyterhub"
        self.config["spark.kubernetes.container.image.pullSecrets"] = "gitlab-pull-secret"
        self.config["spark.driver.host"] = socket.gethostbyname(socket.gethostname())

        # Set executor configurations
        self.config["spark.executor.instances"] = self.executor_instances
        self.config["spark.executor.cores"] = self.executor_cores
        self.config["spark.executor.memory"] = self.executor_memory
        self.config["spark.kubernetes.executor.limit.cores"] = self.executor_cores

        # Google Cloud configurations
        if self.google_service_account_path:
            self.config["fs.AbstractFileSystem.gs.impl"] = "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS"
            self.config["spark.hadoop.fs.gs.impl"] = "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem"
            self.config["spark.executorEnv.GOOGLE_APPLICATION_CREDENTIALS"] = "application_default_credentials.json"

        # Google Cloud Storage configurations
        jars_str = ",".join(self.jars)
        self.config["spark.jars"] = jars_str

        packages_str = ",".join(self.packages)
        self.config["spark.jars.packages"] = packages_str

        # Logging configurations
        history_path = os.getenv("KUBERNETES_SPARK_HISTORY_PATH")
        if history_path:
            self.config["spark.eventLog.enabled"] = "true"
            self.config["spark.eventLog.rolling.enabled"] = "true"
            self.config["spark.eventLog.rolling.maxFileSize"] = "10m"
            self.config["spark.eventLog.dir"] = history_path
            self.config["spark.history.fs.logDirectory"] = history_path

    def create(self):
        config = SparkConf()

        for key, value in self.config.items():
            config.set(key, str(value))

        session = SparkSession.builder \
            .appName(self.name) \
            .master(self.master) \
            .config(conf=config) \
            .enableHiveSupport() \
            .getOrCreate()

        session.sparkContext.addFile(self.google_service_account_path)

        print(f"Spark UI: http://127.0.0.1:4040")

        return session
