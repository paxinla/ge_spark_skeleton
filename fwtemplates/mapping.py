# coding=utf-8

import logging
from collections import namedtuple

from {{project_root}}.rules.rule_value_is_zero import RuleValueIsZero

from {{project_root}}.data_assets.dataset_example_data_001 import DatasetExampleData001

logger = logging.getLogger("dqc_{{render_id}}")


ValidatePair = namedtuple("ValidatePair", ["data_spec", "rule_spec"])

# This is a global dict for all validations.
# Add each dataset(class name) and rule(class name) binding as a ValidatePair
# here. The key name is for caller to find the validation
DATASET_RULE_MAP = {
    "call_key_001": ValidatePair(data_spec = DatasetExampleData001,
                                 rule_spec = RuleValueIsZero)
}

