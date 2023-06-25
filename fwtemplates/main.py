# coding=utf-8

import sys
import pkgutil
import logging
import traceback
import json
import shutil

from great_expectations.core.util import get_or_create_spark_application

from {{project_root}}.config import (
    parse_binary_conf,
    clear_store_backend,
    get_data_context,
    get_checkpoint
)

logFormatter = logging.Formatter('%(asctime)s [%(levelname)s] (%(pathname)s:%(lineno)d@%(funcName)s) -> %(message)s')
logger = logging.getLogger("dqc_{{render_id}}")
logger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


def main():
    """Input positional arguments:
       1. case_key : Must have. Defined in DATASET_RULE_MAP in mapping.py file.
       2. case_query_params: Optional. Json formatted parameters for dataset objects.
       3. case_rule_params: Optional. Json formatted parameters for rule objects.
    """
    args = sys.argv
    logger.info(f"Params length: {len(sys.argv)}")

    case_key = args[1].strip()
    case_query_params = json.loads(args[2].strip(), strict=False) if len(args) >= 3 else {}
    case_rule_params = json.loads(args[3].strip(), strict=False) if len(args) >= 4 else {}

    logger.info(f"Input: case_key = {case_key}")
    logger.info(f"Input: case_query_params = {case_query_params}")
    logger.info(f"Input: case_rule_params = {case_rule_params}")

    if case_key == 'dummy':
        assert True
    elif case_key == 'clear_root':
        CONFIGFILE_DATA = pkgutil.get_data(__package__, "config.ini")

        config = parse_binary_conf(CONFIGFILE_DATA)

        clear_store_backend(config)

        assert True
    else:
        CONFIGFILE_DATA = pkgutil.get_data(__package__, "config.ini")

        config = parse_binary_conf(CONFIGFILE_DATA)

        data_context = get_data_context(config)

        checkpoint_name = get_checkpoint(data_context)

        spark = get_or_create_spark_application()

        all_validations = get_validations(
            case_key,
            case_query_params,
            case_rule_params,
            config,
            data_context,
            {"spark": spark}
        )

        valiate_result = data_context.run_checkpoint(
            checkpoint_name = checkpoint_name,
            validations = all_validations
        )

        try:
            assert valiate_result.success
            logger.info(">>>>>>>> Following are run results")
            logger.info(valiate_result.run_results)
        except Exception as e:
            logger.error(valiate_result.run_results)
            raise e


if __name__ == "__main__":
    main()

