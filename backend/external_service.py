from collections import OrderedDict
from typing import (
    Dict,
    List,
    Union,
)

import requests
from requests import RequestException

from backend.constants import (
    BASE_URL,
    GLOBAL_QUOTE,
    TIME_SERIES_DAILY,
    TIME_SERIES_INTRADAY,
    SYMBOL_SEARCH,
    TIME_SERIES_MONTHLY,
    TIME_SERIES_WEEKLY,
)

REQUEST_EXCEPTION = (
    "An error has occurred during processing your request. "
    "Please try entering again your api or try a new stock."
)

RATE_LIMITING_MESSAGE = (
    "Exceeded the maximum of 5 calls per minute or 500 calls per day. "
    "Please try again later."
)

TIME_SERIES_MAPPING = {
    TIME_SERIES_INTRADAY: "Time Series ({interval})",
    TIME_SERIES_DAILY: "Time Series (Daily)",
    TIME_SERIES_WEEKLY: "Weekly Time Series",
    TIME_SERIES_MONTHLY: "Monthly Time Series",
}


def get_symbol_search_data(data: Dict, **kwargs: Dict) -> List[Dict[str, str]]:
    """Return the symbol core data."""
    exact_match = kwargs.get("exact_match")
    matches = data.get("bestMatches")
    ret_data = []
    if not matches:
        matches = data
    if not isinstance(matches, list):
        return []

    for match in matches:
        if exact_match:
            if match["1. symbol"] != exact_match:
                continue
        ret_data.append({
            "symbol": match["1. symbol"],
            "name": match["2. name"],
            "type": match["3. type"],
            "region": match["4. region"],
            "marketOpen": match["5. marketOpen"],
            "marketClose": match["6. marketClose"],
            "timezone": match["7. timezone"],
            "currency": match["8. currency"],
            "matchScore": match["9. matchScore"],
        })
    return ret_data


def get_historical_data(data: Dict, **kwargs: Dict):
    """Return historical data for a given period and symbol."""
    metadata = data["Meta Data"]
    function = kwargs.get("function")
    time_series_key = TIME_SERIES_MAPPING.get(function)
    if function == TIME_SERIES_INTRADAY:
        time_series_key = time_series_key.format(interval=kwargs["interval"])
    time_series = data[time_series_key]
    data = {
        "labels": [],
        "open": [],
        "close": [],
        "high": [],
        "low": [],
    }
    time_series = OrderedDict(sorted(time_series.items()))
    for dt, price in time_series.items():
        data["labels"].append(dt)
        data["open"].append(price["1. open"])
        data["high"].append(price["2. high"])
        data["low"].append(price["3. low"])
        data["close"].append(price["4. close"])
    meta = {
        "meta": {
            "information": metadata["1. Information"],
            "symbol": metadata["2. Symbol"],
            "last_refreshed": metadata["3. Last Refreshed"],
        },
        **data,
    }
    if function == TIME_SERIES_INTRADAY:
        meta["meta"]["interval"] = metadata["4. Interval"]
    return meta


def get_current_quote_data(data: Dict, **kwargs):
    """Return the current quote for the given symbol."""
    content = data["Global Quote"]
    return {
        "symbol": content["01. symbol"],
        "open": content["02. open"],
        "high": content["03. high"],
        "low": content["04. low"],
        "price": content["05. price"],
        "volume": content["06. volume"],
        "latestTradingDay": content["07. latest trading day"],
        "previousClose": content["08. previous close"],
        "change": content["09. change"],
        "changePercent": content["10. change percent"],

    }


processing_mapping = {
    SYMBOL_SEARCH: get_symbol_search_data,
    TIME_SERIES_INTRADAY: get_historical_data,
    TIME_SERIES_DAILY: get_historical_data,
    TIME_SERIES_WEEKLY: get_historical_data,
    TIME_SERIES_MONTHLY: get_historical_data,
    GLOBAL_QUOTE: get_current_quote_data
}


def perform_request(
        apikey: str,
        function: str,
        **kwargs: Dict
) -> Union[List[Dict], Dict]:
    """Return the processed data for the given function."""
    params = {
        "function": function,
        "apikey": apikey,
        **kwargs
    }
    try:
        response = requests.get(url=BASE_URL, params=params)
    except RequestException:
        return {"error": REQUEST_EXCEPTION}
    resp_content = response.json()
    if resp_content.get("error") or resp_content.get("Error Message"):
        return {"error": REQUEST_EXCEPTION}
    if resp_content.get("Note"):
        return {"error": RATE_LIMITING_MESSAGE}
    return processing_mapping.get(function)(response.json(), **params)
