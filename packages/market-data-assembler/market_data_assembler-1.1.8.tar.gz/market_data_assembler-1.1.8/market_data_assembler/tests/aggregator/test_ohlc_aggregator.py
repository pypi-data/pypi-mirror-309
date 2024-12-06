import unittest
from datetime import datetime, timezone

from market_data_assembler.aggregator.ohlc_aggregator import OHLCAggregator
from market_data_assembler.tests.aggregator.test_ohlc_aggregator_expected import expected_history_1, \
    expected_current_window_candles_2


class TestOHLCAggregator(unittest.TestCase):
    def setUp(self):
        self.window_sec = 300
        self.history_size = 5

    def test_aggregation(self):
        self.aggregator = OHLCAggregator(self.window_sec, self.history_size)
        minutes = list(range(0, 26))
        candles = self._generate_candles(minutes)

        for candle in candles:
            # print(datetime.fromtimestamp(candle['t'] / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))
            self.aggregator.aggregate(candle, "TEST")

        self.assertEqual(self.aggregator.current_window_candles, [candles[-1]],
                         "Current window candle does not match the expected value")
        self.assertEqual(self.aggregator.history, expected_history_1, "History does not match the expected value")
        self.assertTrue(self.aggregator.is_fully_aggregated())
        self.assertTrue(self.aggregator.is_ready())

    def test_aggregation_2(self):
        self.aggregator = OHLCAggregator(self.window_sec, self.history_size)
        minutes = list(range(0, 25))
        candles = self._generate_candles(minutes, 59)

        for candle in candles:
            self.aggregator.aggregate(candle, "TEST")

        self.assertEqual(self.aggregator.current_window_candles, expected_current_window_candles_2,
                         "Current window candle does not match the expected value")
        self.assertEqual(self.aggregator.history, expected_history_1, "History does not match the expected value")
        self.assertFalse(self.aggregator.is_fully_aggregated())
        self.assertTrue(self.aggregator.is_ready())

    def test_aggregation_3(self):
        self.aggregator = OHLCAggregator(self.window_sec, self.history_size)
        candles = self._generate_candles([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 30, 31, 32, 33, 34, 35])

        for candle in candles:
            self.aggregator.aggregate(candle, "TEST")

        self.assertEqual(self.aggregator.current_window_candles, [candles[-1]],
                         "Current window candle does not match the expected value")
        self.assertEqual(self.aggregator.history[3]['n'], candles[-7]['n'])
        self.assertEqual(self.aggregator.history[3]['o'], candles[-7]['o'])
        self.assertEqual(self.aggregator.history[3]['c'], candles[-7]['c'])
        self.assertEqual(self.aggregator.history[3]['l'], candles[-7]['l'])
        self.assertEqual(self.aggregator.history[3]['h'], candles[-7]['h'])
        self.assertEqual(self.aggregator.history[3]['v'], candles[-7]['v'])
        self.assertEqual(self.aggregator.history[2]['v'], 450)
        self.assertEqual(self.aggregator.history[2]['v'], 450)
        self.assertEqual(self.aggregator.history[4]['v'], 600)
        self.assertEqual(self.aggregator.history[4]['n'], 600)
        self.assertTrue(self.aggregator.is_fully_aggregated())
        self.assertTrue(self.aggregator.is_ready())


    @staticmethod
    def _generate_candles(times, second= 0):
        candles = [
            {
                "t": int(datetime(2024, 11, 1, 0, minute, second, tzinfo=timezone.utc).timestamp() * 1000),
                "o": 5 * (i + 1),
                "h": 10 * (i + 1),
                "l": 3 * (i + 1),
                "c": 4 * (i + 1),
                "v": 5 * (i + 1),
                "n": 5 * (i + 1),
            }
            for i, minute in enumerate(times)
        ]

        t_from = datetime.fromtimestamp(candles[0]['t'] / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        t_to = datetime.fromtimestamp(candles[-1]['t'] / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        print(f'From {t_from} - to {t_to}')

        return candles


if __name__ == "__main__":
    unittest.main()
