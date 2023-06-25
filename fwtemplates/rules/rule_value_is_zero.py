# coding=utf-8

import logging
from great_expectations.core.expectation_configuration import ExpectationConfiguration

logger = logging.getLogger("dqc_{{render_id}}")


class RuleValueIsZero:
    def __init__(self, context, **kwargs):
        result_detail_level = kwargs.get("result_format", "BASIC")
        column_name = kwargs.get("column_name", "check_column")
        min_value = kwargs.get("min_value", 0)
        max_value = kwargs.get("max_value", 0.001)

        logger.info(f"Input: kwargs = {kwargs}")
        logger.info(f"Got: result_format = {result_detail_level}")
        logger.info(f"Got: column_name = {column_name}")
        logger.info(f"Got: min_value = {min_value}")
        logger.info(f"Got: max_value = {max_value}")

        self.suite_name = f"rules_for_value_should_be_zero"
        self.suite = context.create_expectation_suite(
            expectation_suite_name = self.suite_name,
            overwrite_existing = True
        )

        self.rules = [
            ExpectationConfiguration(
                expectation_type = "expect_column_values_to_be_between",
                kwargs = {
                    "column": column_name,
                    "min_value": min_value,
                    "max_value": max_value,
                    "result_format": result_detail_level
                },
                meta = {
                    "notes": {
                        "format": "markdown",
                        "content": f"Specific column value should be 0."}}
            ), 
        ]

        for idx, each_rule in enumerate(self.rules):
            self.suite.add_expectation(expectation_configuration=each_rule)
            logger.debug(f"Add number {idx+1} for rule {self.suite_name}.")

        context.save_expectation_suite(self.suite, self.suite_name)
        logger.info(f"Expectation suite for rule {self.suite_name} has been built.")

