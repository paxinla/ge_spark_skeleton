# coding=utf-8

import os
import logging
import configparser
import io
import shutil
from great_expectations.data_context import BaseDataContext
from great_expectations.data_context.types.base import (
    DataContextConfig,
    FilesystemStoreBackendDefaults
)

from {{project_root}}.mapping import DATASET_RULE_MAP

logger = logging.getLogger("dqc_{{render_id}}")


def parse_binary_conf(conf_bin_data):
    conf_loader = configparser.ConfigParser()
    conf_loader.read_file(io.StringIO(conf_bin_data.decode("utf-8")))
    return conf_loader


def clear_store_backend(config):
    """ Config the data doc locations. The dbfs is the default filesystem on Databricks.
    """
    root_directory = config.get("dbfs", "root_directory")

    shutil.rmtree(f"{root_directory}/checkpoints/", ignore_errors=True)
    shutil.rmtree(f"{root_directory}/expectations/", ignore_errors=True)
    shutil.rmtree(f"{root_directory}/profilers/", ignore_errors=True)
    shutil.rmtree(f"{root_directory}/uncommitted/", ignore_errors=True)


def get_data_context(config):
    root_directory = config.get("dbfs", "root_directory")
    data_context_config = DataContextConfig(
        store_backend_defaults = FilesystemStoreBackendDefaults(
            root_directory = root_directory
        ),
    )

    context =  BaseDataContext(project_config=data_context_config)

    data_source_name = config.get("datasource", "datasource_name")
    data_connector_name = config.get("datasource", "data_connector_name")

    batch_stage_key = config.get("datasource", "batch_stage_key")
    batch_run_key = config.get("datasource", "batch_run_key")
    batch_identifiers = [batch_stage_key, batch_run_key]

    custom_spark_datasource_config = {
        "name": data_source_name,
        "class_name": "Datasource",
        "execution_engine": {"class_name": "SparkDFExecutionEngine"},
        "data_connectors": {
            data_connector_name: {
                "module_name": "great_expectations.datasource.data_connector",
                "class_name": "RuntimeDataConnector",
                "batch_identifiers": batch_identifiers,
            }
        },
    }

    context.add_datasource(**custom_spark_datasource_config)
    logger.info("Data context for validating data of {{project_name}} is ready.")

    return context


def get_checkpoint(context):
    checkpoint_name = "ckpt_{{project_name}}"

    checkpoint_config = {
        "name": checkpoint_name,
        "config_version": 1.0,
        "class_name": "SimpleCheckpoint",
        "run_name_template": "%Y%m%d-%H%M%S-{{project_name}}-validation",
    }

    context.add_checkpoint(**checkpoint_config)
    logger.info(f"Checkpoint {checkpoint_name} for validating data of {{project_name}} is ready.")
    return checkpoint_name



def get_validations(case_key, case_query_params, case_rule_params, config, data_context, execution_context):

    execute_on = execution_context["spark"]
    validation = DATASET_RULE_MAP[case_key]

    logger.info(f"Input: case_key = {case_key}")
    logger.info(f"Input: case_query_params = {case_query_params}")
    logger.info(f"Input: case_rule_params = {case_rule_params}")

    logger.info(f"Case: data_spec = {validation.data_spec.__name__}")
    logger.info(f"Case: rule_spec = {validation.rule_spec.__name__}")

    try:
        validations = [{
            "batch_request": validation.data_spec(config, execute_on, **case_query_params).get_dataset(),
            "expectation_suite_name": validation.rule_spec(data_context, **case_rule_params).suite_name 
        }]
    except Exception as e:
        logger.error(f"Cannot get validations for {case_key} , query params are {case_query_params} , rule params are {case_rule_params} .")
        raise e

    return validations

