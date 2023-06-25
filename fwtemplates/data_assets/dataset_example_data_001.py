# coding=utf-8

import logging
import datetime

from delta.tables import *

from {{project_root}}.data_assets.dataset import SparkDataset

logger = logging.getLogger("dqc_{{render_id}}")


class DatasetExampleData001(SparkDataset):
    def __init__(self, config, spark, **kwargs):
        super(DatasetExampleData001, self).__init__(config, spark, **kwargs)

        self._target_table_name = "some_name"

        target_table_name = f"some_database_name.some_table_name"

        today = datetime.datetime.today()
        day2before = today - datetime.timedelta(days=2)
        stat_date = day2before.strftime("%Y-%m-%d")

        self.dataset = spark.sql(
            f""" SELECT t.some_integer_column_name  AS check_column
                   FROM {target_table_name} t
                  WHERE t.data_date = to_date('{stat_date}')
            """
        )

