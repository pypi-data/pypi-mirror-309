import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List

from market_data_assembler.assembling.aggregation_config import AggregationConfig
from market_data_assembler.assembling.dataset_assembler import DatasetAssembler
from market_data_assembler.assembling.dataset_cache import DatasetCache
from market_data_assembler.common.common import random_string, load_compressed_json, generate_date_range
from market_data_assembler.labeling.dataset_labeler_abstract import BaseDatasetLabeler


class HistoricalAssemblerManager:
    """Assembles a dataset from cryptocurrency series data."""

    dataset_out_root_folder = './out/datasets'

    def __init__(
            self,
            instruments: List[str],
            day_from: datetime,
            day_to: datetime,
            dataset_labeler: BaseDatasetLabeler,
            aggregations_configs: List[AggregationConfig],
            raw_series_folder: str,
            max_workers: int
    ):

        self.instruments = instruments
        self.aggregations_configs = aggregations_configs
        self.selected_days = generate_date_range(day_from, day_to)
        self.dataset_labeler: BaseDatasetLabeler = dataset_labeler
        self.raw_series_folder = raw_series_folder
        self.max_workers = max_workers
        self.dataset_unique_name = random_string()
        self.cache = DatasetCache(
            day_from,
            day_to,
            self.dataset_out_root_folder,
            self.instruments,
            self.aggregations_configs,
            self.dataset_labeler,
            self.dataset_unique_name
        )

    def generate_dataset(self):
        datasets_path = self.cache.get_cached()
        if datasets_path:
            return datasets_path

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for instrument in self.instruments:
                futures.append(executor.submit(self._process_instrument, instrument))

            for future in as_completed(futures):
                future.result()

        datasets_path = self.cache.save_config()
        return datasets_path

    def _process_instrument(self, instrument):
        assembler = DatasetAssembler(instrument=instrument, aggregations_configs=self.aggregations_configs)
        for file_path in self._filter_and_sort_files(instrument):
            print(f"process-{os.getpid()}, time: {datetime.now()}, assembling file : {file_path}")
            series = load_compressed_json(file_path)
            for raw_candle in series:
                self._process_aggregations(raw_candle, instrument, assembler)

    def _process_aggregations(self, candle, instrument, assembler):
        assembler.update_aggregations(candle, instrument)

        if assembler.is_ready():
            labels = self.dataset_labeler.apply(assembler.get_aggregations())
            dataset = assembler.to_dataset()
            dataset.update(labels)
            self.cache.save_dataset(dataset, instrument)

    def _filter_and_sort_files(self, instrument):
        instrument_raw_folder = os.path.join(self.raw_series_folder, instrument)
        selected_days_naive = [day.replace(tzinfo=None) for day in self.selected_days]

        if not os.path.exists(instrument_raw_folder) or not os.listdir(instrument_raw_folder):
            raise FileNotFoundError(f"Raw data for instrument {instrument} was not loaded. Cannot create datasets.")

        instrument_files = []
        for f in os.listdir(instrument_raw_folder):
            if f.startswith(instrument):
                date_str = f.split('_')[1].split('.')[0]
                file_date = datetime.strptime(date_str, '%Y-%m-%d')
                if file_date in selected_days_naive:
                    instrument_files.append((file_date, f))

        instrument_files.sort(key=lambda x: x[0])
        return [os.path.join(self.raw_series_folder, instrument, f[1]) for f in instrument_files]
