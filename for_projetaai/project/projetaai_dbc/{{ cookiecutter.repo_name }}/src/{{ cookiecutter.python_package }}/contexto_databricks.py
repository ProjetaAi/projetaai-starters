"""Define os parâmetros para conexão com o Databricks."""
import json
from pathlib import Path
from typing import Any, Dict, Union

from kedro.config import ConfigLoader
from kedro.framework.context import KedroContext
from pluggy import PluginManager
from pyspark import SparkConf
from pyspark.sql import SparkSession


class ContextoDatabricksAzure(KedroContext):
    """Define Classe para conexão com Databricks."""

    def __init__(
        self,
        package_name: str,
        project_path: Union[Path, str],
        config_loader: ConfigLoader,
        hook_manager: PluginManager,
        env: str = None,
        extra_params: Dict[str, Any] = None,
    ):
        super().__init__(
            package_name, project_path, config_loader, hook_manager, env, extra_params
        )
        self.init_spark_session(package_name)

    def init_spark_session(self, package_name) -> None:
        """Initialises a SparkSession using
        the config defined in project's conf folder."""
        # Load the spark configuration in spark.yaml using the config loader
        parameters = self.config_loader.get("spark*", "spark*/**")

        # gettin databricks token from databricks-connect file on /root
        f = open("/root/.databricks-connect")
        db_connect_file = json.load(f)

        parameters["spark.databricks.service.token"] = db_connect_file["token"]

        spark_conf = SparkConf().setAll(parameters.items())

        # closing opened file
        f.close()

        # Initialise the spark session
        spark_session_conf = (
            SparkSession.builder.appName(self._package_name)
            .enableHiveSupport()
            .config(conf=spark_conf)
        )
        _spark_session = spark_session_conf.getOrCreate()
        _spark_session.sparkContext.setLogLevel("WARN")
