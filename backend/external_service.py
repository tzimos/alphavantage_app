from typing import (
    Dict,
    List,
    Union,
)

import requests
from requests import RequestException

from backend.constants import (
    BASE_URL,
    SYMBOL_SEARCH,
)


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


processing_mapping = {
    SYMBOL_SEARCH: get_symbol_search_data
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
        return {
            "error": "An error has occured during"
                     " proccessing your request. Please try again."
        }
    return processing_mapping.get(function)(response.json(), **kwargs)
