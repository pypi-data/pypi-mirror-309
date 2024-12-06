from datetime import datetime

from market_data_assembler.loader.binance_vision.book_depth_loader import BinanceVisionBookDepthLoader
from market_data_assembler.loader.binance_vision.ohlc_loader import BinanceVisionOhlcLoader
from market_data_assembler.loader.binance_vision.trades_loader import BinanceVisionTradesLoader
from market_data_assembler.providers.crypto_series_data_provider import CryptoSeriesDataProvider

if __name__ == "__main__":
    provider = CryptoSeriesDataProvider(instruments=['RAYUSDT'],
                                        day_from=datetime(2024, 11, 10),
                                        day_to=datetime(2024, 11, 17),
                                        ohlc_loader_class=BinanceVisionOhlcLoader,
                                        trades_loader_class=BinanceVisionTradesLoader,
                                        book_depth_loader_class=BinanceVisionBookDepthLoader,
                                        max_workers=5)

    provider.load_raw_series()
    #
    # prepare_directory(HistoricalAssemblerManager.dataset_out_root_folder)
    # organizer = HistoricalAssemblerManager(instruments=['ETHUSDT', 'UNIUSDT'],
    #                                        day_from=datetime(2024, 10, 30),
    #                                        day_to=datetime(2024, 11, 3),
    #                                        aggregations_configs=
    #                                        [
    #                                            {
    #                                                "ohlc": {"window_sec": 300, "history_size": 40},
    #                                                "indicators": [{"indicator_class": MovingAverageIndicator,
    #                                                                "window_length": 10},
    #                                                               {"indicator_class": MovingAverageIndicator,
    #                                                                "window_length": 3}]
    #                                            },
    #                                            {
    #                                                "ohlc": {"window_sec": 1200, "history_size": 10},
    #                                                "indicators": [{"indicator_class": MovingAverageIndicator,
    #                                                                "window_length": 10}]
    #                                            },
    #                                            {
    #                                                "ohlc": {"window_sec": 10600, "history_size": 10},
    #                                                "indicators": []
    #                                            }
    #                                        ],
    #                                        dataset_labeler=VolatilityDatasetLabeler(training_window=0.75),
    #                                        raw_series_folder=CryptoSeriesDataProvider.raw_series_folder,
    #                                        max_workers=5)
    #
    # datasets_path = organizer.generate_dataset()
    # print(datasets_path)
