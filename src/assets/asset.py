import time
from typing import Final
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()


class PriceGenerator:
    """
    Generates prices for cryptocurrency assets using CoinGecko API
    """

    DATE_FORMAT: Final = "yyyy-mm-dd"

    _TICKERS_TO_COINGECKO_ID: Final = {
        "ada": "cardano",
        "algo": "algorand",
        "atom": "cosmos",
        "avax": "avalanche-2",
        "boson": "boson-protocol",
        "bnb": "binancecoin",
        "btc": "bitcoin",
        "busd": "binance-usd",
        "ckb": "nervos-network",
        "cos": "contentos",
        "cro": "crypto-com-chain",
        "dot": "polkadot",
        "elon": "dogelon-mars",
        "eth": "ethereum",
        "link": "chainlink",
        "lrc": "loopring",
        "luna": "terra-luna",
        "matic": "matic-network",
        "mir": "mirror-protocol",
        "nano": "nano",
        "one": "harmony",
        "ping": "sonar",
        "skill": "cryptoblades",
        "uni": "uniswap",
        "usdc": "usd-coin",
        "usdt": "tether",
        "vet": "vechain",
        "vvs": "vvs-finance",
        "xlm": "stellar",
        "xno": "nano"
    }

    _STABLECOINS: Final = {
        "usdt", "tether",
        "usdc", "usd-coin",
        "busd", "binance-usd"
    }

    _NATIONAL_CURRENCIES: Final = {
        "cad": "canadian-dollars",
        "usd": "american-dollars"
    }

    MONTHS: Final = {
        "jan": "01",
        "feb": "02",
        "mar": "03",
        "apr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "aug": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dec": "12"
    }

    def get_price(self, ticker, calculation_date, fiat_currency="cad", parse_date=True):
        """
        Obtains the daily opening price of a cryptocurrency for any day
        If the ticker is not loaded into the program, the program terminates

        Attributes:
            ticker - The ticker of the cryptocurrency
            calculation_date - The date to obtain the price in the format yyyy-mm-dd
            fiat_currency - The local currency to receive the price in
        """
        if ticker.lower() == "none":
            return 0
        if parse_date:
            calculation_date = self._format_date(calculation_date)
        print("Ticker: {}".format(ticker))
        if ticker.lower() in PriceGenerator._NATIONAL_CURRENCIES:
            return self._get_national_currency_price(ticker, calculation_date, fiat_currency)
        coingecko_id = PriceGenerator._TICKERS_TO_COINGECKO_ID.get(
            ticker.lower())
        coin_data = cg.get_coin_history_by_id(
            id=coingecko_id, date=calculation_date, localization=False)
        price = coin_data["market_data"]["current_price"][fiat_currency]
        # Pause for 1.5 seconds to stay within coingecko rate limit of 50 calls/minute
        time.sleep(1.5)
        return price

    def _get_national_currency_price(self, starting_currency, formatted_date, target_currency):
        """
        Obtains the value of a national currency in terms of another currency

        Attributes:
            starting_currency - The currency in which the value of the target currency is being measured
            formatted_date - The date to obtain the price in the format dd-mm-yyyy
            target_currency - The currency to receive the value of

        Returns - The value of the target currency in terms of the starting currency
        """
        if starting_currency.lower() == target_currency.lower():  # Same currency
            return 1.0
        bitcoin_id = PriceGenerator._TICKERS_TO_COINGECKO_ID.get("btc")
        bitcoin_data = cg.get_coin_history_by_id(
            id=bitcoin_id, date=formatted_date, localization=False)
        target_currency_price = bitcoin_data["market_data"]["current_price"][target_currency.lower(
        )]
        starting_currency_price = bitcoin_data["market_data"]["current_price"][starting_currency.lower(
        )]
        # Pause for 1.5 seconds to stay within coingecko rate limit of 50 calls/minute
        time.sleep(1.5)
        return target_currency_price / starting_currency_price

    def _format_date(self, date):
        """
        Formats date from yyyy-mm-dd to dd-mm-yyyy
        """
        date = str(date)
        #print("Date: {}".format(date))
        components = date.split("-")
        year = components[0]
        month = components[1]
        day = components[2]
        return "-".join([day, month, year])

    @staticmethod
    def can_parse_tickers(tickers):
        """
        Determines if the program can parse the specified tickers and prints a message informing the user of the result

        Attributes:
            tickers - List of all tickers which will be parsed

        Returns: True if all assets can be parsed, False otherwise
        """
        unparsable_tickers = []
        for ticker in tickers:
            print("Ticker: {}".format(ticker))
            if (not (ticker.lower() in PriceGenerator._TICKERS_TO_COINGECKO_ID
                     or ticker.lower() in PriceGenerator._NATIONAL_CURRENCIES)):
                unparsable_tickers.append(ticker)
        if len(unparsable_tickers) == 0:
            print("All assets can be parsed\n")
            return True
        else:
            print("The following assets can not currently be parsed:")
            for ticker in unparsable_tickers:
                print(ticker)
            return False
