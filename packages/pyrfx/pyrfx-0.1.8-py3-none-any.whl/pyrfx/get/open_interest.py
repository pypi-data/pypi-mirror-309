import logging
import time
from logging import Logger
from typing import Any

from pyrfx.config_manager import ConfigManager
from pyrfx.get.data import Data
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.utils import execute_threading


class OpenInterest(Data):
    """
    Class responsible for retrieving and processing open interest data for RFX markets.
    """

    def __init__(self, config: ConfigManager, log_level: int = logging.INFO) -> None:
        """
        Initialize the OpenInterest class with configuration and logger setup.

        :param config: ConfigManager object containing chain configuration.
        :param log_level: Logging level for this class.
        """
        super().__init__(config=config, log_level=log_level)
        self.config: ConfigManager = config
        self._prices: dict[str, dict[str, Any]] | None = None

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

    def _get_data_processing(self) -> dict[str, Any]:
        """
        Generate the dictionary of open interest data.

        :return: Dictionary containing open interest data.
        """
        self.logger.info("Processing RFX open interest data ...")

        if not self._prices:
            self._prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()

        # Lists for multithreaded execution
        long_oi_output_list: list = []
        short_oi_output_list: list = []
        long_pnl_output_list: list = []
        short_pnl_output_list: list = []
        mapper: list = []
        long_precision_list: list = []

        for market_key in self.markets.info:
            self._filter_swap_markets()
            self._get_token_addresses(market_key)

            index_token_address = self.markets.get_index_token_address(market_key)
            market = [market_key, index_token_address, self._long_token_address, self._short_token_address]

            # Fetch oracle prices for the index token
            min_price, max_price = self._get_min_max_prices(self._prices, index_token_address)

            # Get precision factors
            precision = self._get_precision_factor(market_key)
            long_precision_list.append(precision)

            # Get long and short open interest with PnL
            long_oi_with_pnl, long_pnl = self._get_pnl(market, [min_price, max_price], is_long=True)
            short_oi_with_pnl, short_pnl = self._get_pnl(market, [min_price, max_price], is_long=False)

            # Add to lists for threading
            long_oi_output_list.append(long_oi_with_pnl)
            short_oi_output_list.append(short_oi_with_pnl)
            long_pnl_output_list.append(long_pnl)
            short_pnl_output_list.append(short_pnl)
            mapper.append(self.markets.get_market_symbol(market_key))

        # Execute threading for long/short open interest and PnL
        long_oi_threaded_output, short_oi_threaded_output, long_pnl_threaded_output, short_pnl_threaded_output = (
            self._execute_multithreading(
                long_oi_output_list, short_oi_output_list, long_pnl_output_list, short_pnl_output_list
            )
        )

        # Process results
        self._process_results(
            mapper,
            long_oi_threaded_output,
            short_oi_threaded_output,
            long_pnl_threaded_output,
            short_pnl_threaded_output,
            long_precision_list,
        )

        return self.output

    @staticmethod
    def _get_min_max_prices(oracle_prices_dict: dict[str, Any], index_token_address: str) -> tuple[int, int]:
        """
        Get the minimum and maximum price for a given index token.

        :param oracle_prices_dict: Dictionary of oracle prices.
        :param index_token_address: Address of the index token.
        :return: Tuple containing min and max prices.
        """
        min_price = int(oracle_prices_dict[index_token_address]["minPriceFull"])
        max_price = int(oracle_prices_dict[index_token_address]["maxPriceFull"])
        return min_price, max_price

    def _get_precision_factor(self, market_key: str) -> int:
        """
        Get the precision factor for the given market key.

        :param market_key: Key representing the market.
        :return: Precision factor as an integer.
        """
        try:
            if self.markets.is_synthetic(market_key):
                decimal_factor = self.markets.get_decimal_factor(market_key)
            else:
                decimal_factor = self.markets.get_decimal_factor(market_key, long=True)
        except KeyError:
            decimal_factor = self.markets.get_decimal_factor(market_key, long=True)

        oracle_factor = 30 - decimal_factor
        return 10 ** (decimal_factor + oracle_factor)

    @staticmethod
    def _execute_multithreading(*args: list) -> tuple[list, ...]:
        """
        Execute multithreading for long/short open interest and PnL calculations.

        :param args: Lists of web3 uncalled functions to execute in threads.
        :return: Threaded output for all lists.
        """
        outputs: list[list] = []
        for output_list in args:
            threaded_output = execute_threading(output_list)
            time.sleep(0.5)  # Delay to prevent rate limiting
            outputs.append(threaded_output)
        return tuple(outputs)

    def _process_results(
        self,
        mapper: list[str],
        long_oi_output: list,
        short_oi_output: list,
        long_pnl_output: list,
        short_pnl_output: list,
        precision_list: list[int],
    ) -> None:
        """
        Process and log the results for long/short open interest and PnL.

        :param mapper: List of market symbols.
        :param long_oi_output: List of long open interest threaded outputs.
        :param short_oi_output: List of short open interest threaded outputs.
        :param long_pnl_output: List of long PnL threaded outputs.
        :param short_pnl_output: List of short PnL threaded outputs.
        :param precision_list: List of precision factors.
        """
        for market_symbol, long_oi, short_oi, long_pnl, short_pnl, long_precision in zip(
            mapper, long_oi_output, short_oi_output, long_pnl_output, short_pnl_output, precision_list
        ):
            long_value = (long_oi - long_pnl) / long_precision
            short_value = (short_oi - short_pnl) / 10**30

            self.logger.info(f"{market_symbol} Long: ${long_value:,.2}")
            self.logger.info(f"{market_symbol} Short: ${short_value:,.2}")

            self.output["long"][market_symbol] = long_value
            self.output["short"][market_symbol] = short_value

        self.output["parameter"] = "open_interest"
