#!/usr/bin/python3

# Copyright 2023 Telefonica
# See LICENSE for details.

# License Apache2!!
# https://github.com/Telefonica/baikal-sdk/tree/master/node


import json
from typing import Any, Dict, Tuple
from pyspark.sql import SparkSession, DataFrame


def load_config(
    config_path: str = 'dataset-config.json'
) -> Dict[str, Any]:
    """Loads the dataset configuration from a JSON file

    Returns:
        deserialized configuration
    """

    print(f'\033[93m>>> [CONFIG] Loading dataset configuration from file \"{config_path}\"\033[0m')

    with open(config_path, 'r') as f:
        config = json.loads(f.read())

    print(f'\033[93m>>> [CONFIG] Loaded configuration for dataset \"{config["dataset-id"]}\"\033[0m')
    print(f'\033[33m{format_record(config)}\033[0m')

    return config


def build_session(
    config: Dict[str, Any]
) -> SparkSession:
    """Builds a Spark session.

    Returns:
        Spark session
    """
    print('\033[92m>>> [SPARK] Building Spark session\033[0m')

    spark_session = SparkSession.builder \
        .master("local") \
        .config(
            key='spark.jars.repositories',
            value=config["maven-repository"]
        ) \
        .config(
            key='spark.jars.packages',
            value=f'{config["avro-version"]},{config["sdk-version"]}'
        ) \
        .getOrCreate()

    spark_session.sparkContext.setLogLevel("WARN")

    return spark_session

def format_entry(
    entry: Tuple[str, Any]
) -> str:
    return f">>> - {entry[0]}: {entry[1]}"


def format_record(
    record: Dict[str, Any]
) -> str:
    return "\n".join(format_entry((k, v)) for k, v in record.items())


def read_dataset(
    spark_session: SparkSession,
    config: Dict[str, Any]
) -> DataFrame:
    """Reads a dataset

    Args:
        spark: pyspark session
        config: the configuration to access the dataset

    Returns:
        dataframe containing the data of the dataframe
    """
    print(f'\033[92m>>> [SPARK] Fetching data from dataset \"{config["dataset-id"]}\"\033[0m')

    return spark_session.read \
        .format('telefonica') \
        .option('dataset.id', config['dataset-id']) \
        .option('dataset.version', config['dataset-version']) \
        .option('4p.baseurl', config['environment']) \
        .option('client.id', config['client-id']) \
        .option('client.secret', config['client-secret']) \
        .load()


def showing_fetched_data(
    df: DataFrame,
    max_records_to_show: int = 20
) -> None:
    """
    """

    print('\033[94m>>> [DATA] Loading dataframe to show fetched records, please wait...\033[0m')
    print(f'\033[94m>>> [DATA] The dataframe has a total of {df.count()} entries\033[0m')

    df.show(max_records_to_show)

    print(f'\033[94m>>> [DATA] {max_records_to_show} records shown successfully\033[0m')

    return


def main():
    """This script only reads data from a dataset.
    """
    print('\033[95m>>> [SCRIPT] Script execution starts now\033[0m')

    config = load_config()
    spark_session = build_session(config)
    max_records_to_show = 20

    showing_fetched_data(
        read_dataset(spark_session,config),
        max_records_to_show
    )

    spark_session.stop()
    print('\033[92m>>> [SPARK] Session closed successfully\033[0m')

    print('\033[95m>>> [SCRIPT] Script execution finished\033[0m')

if __name__ == '__main__':
    main()
