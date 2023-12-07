"""Define os parâmetros para conexão com o Databricks."""
from pathlib import Path
from typing import Any, Dict, Union

from kedro.config import ConfigLoader
from kedro.framework.context import KedroContext
from pluggy import PluginManager
from pyspark import SparkConf
from pyspark.sql import SparkSession
import json

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azureml.core import Run


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
        """init."""
        super().__init__(
            package_name, project_path, config_loader, hook_manager, env, extra_params
        )
        self.init_spark_session(package_name)

    def check_if_not_azureml(self) -> bool:
        """Check if the code is running on AzureML."""
        c = Run.get_context()
        if c._run_id.startswith("OfflineRun"):
            return True
        else:
            return False

    def get_keyvault_secret(self,
                            parameters: dict) -> str:
        """Gets the secret from keyvault."""
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=parameters['url_key_vault'],
                              credential=credential)
        parameters = self.fix_token_name(parameters)
        parameters['spark.databricks.service.token'] = client.get_secret(parameters['spark.databricks.service.token']).value
        parameters.pop('url_key_vault')
        return parameters

    def fix_token_name(self, parameters: dict) -> str:
        """Fixes the token name to be used on keyvault."""
        token_name = parameters['spark.databricks.service.token']
        parameters['spark.databricks.service.token'] = token_name if not token_name.startswith("kv::") else token_name.replace("kv::", "")
        return parameters

    def init_spark_session(self: Any, package_name: Any) -> None:
        """Initialises a SparkSession using the config defined in project's conf folder."""
        parameters = self.config_loader.get("spark*", "spark*/**")
        # Load the spark configuration in spark.yaml using the config loader
        if self.check_if_not_azureml():
            parameters = self.get_keyvault_secret(parameters)
        else:
            f = open("/root/.databricks-connect")
            db_connect_file = json.load(f)
            parameters['spark.databricks.service.token'] = db_connect_file['token']
        spark_conf = SparkConf().setAll(parameters.items())
        # Initialise the spark session
        spark_session_conf = (
            SparkSession.builder.appName(self._package_name)
            .enableHiveSupport()
            .config(conf=spark_conf)
        )
        _spark_session = spark_session_conf.getOrCreate()
        _spark_session.sparkContext.setLogLevel("WARN")