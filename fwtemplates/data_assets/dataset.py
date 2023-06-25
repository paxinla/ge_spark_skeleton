# coding=utf-8

import logging
import datetime
import time

from great_expectations.core.batch import RuntimeBatchRequest

logger = logging.getLogger("dqc_{{render_id}}")


class SparkDataset:
    def __init__(self, config, spark, **kwargs):
        self._target_table_name = "<your-target-table-name>"
        self._stage = "prod"

        self.data_source_name = config.get("datasource", "datasource_name")
        self.data_connector_name = config.get("datasource", "data_connector_name")
        self.batch_stage_key = config.get("datasource", "batch_stage_key")
        self.batch_run_key = config.get("datasource", "batch_run_key")

        self.dataset = None


    def get_dataset(self,):
        self.batch_request = RuntimeBatchRequest(
            datasource_name = self.data_source_name,
            data_connector_name = self.data_connector_name,
            data_asset_name = f"last_inc_{self._target_table_name}",
            batch_identifiers = {
                self.batch_stage_key: self._stage,
                self.batch_run_key: f"inc_{self._target_table_name}_{datetime.date.today().strftime('%Y%m%d')}"
            },
            runtime_parameters={"batch_data": self.dataset}
        )

        return self.batch_request


    def filecoin_mainnet_get_current_height(self,):
        return (int(time.time()) - 1598306400) // 30


    def filecoin_mainnet_get_scan_height_range(self,):
        current_height = self.get_current_height() 
        one_week_epoch = 2880 * 7
        height_end = current_height - one_week_epoch
        height_start = height_end - one_week_epoch
        return (height_start, height_end)

