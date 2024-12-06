"""Define the pycarnot library."""

from __future__ import annotations

import sys

import requests

from .const import API_URL
from .exceptions import InvalidAPIResponse, TooManyRequests

if sys.version_info < (3, 11, 0):
    sys.exit("The pyWorxcloud module requires Python 3.11.0 or later")


class Carnot:
    """
    Carnot library

    Used for communication with the Carnot API

    Results are a forecast of electricity prices for the next week
    """

    def __init__(self, email: str, apikey: str, region: str) -> None:
        """Initialize the :class:Carnot class and set default settings and API key."""
        self._apikey = apikey
        self._region = region
        self._email = email

        self.prices: dict = {}

    def update(self) -> None:
        """Get the latest dataset."""
        headers = self._header()
        url = f"?region={self._region.lower()}&energysource=spotprice&daysahead=7"

        price_list: list = []
        price_list_raw: list = self._get_response(headers, url)
        for price in price_list_raw["predictions"]:
            data: dict = {"utc_start": price["utctime"], "price": price["prediction"]}
            price_list.append(data)

        self.prices = price_list

    def _get_response(self, header: dict, path: str) -> dict:
        """Make the request to the API."""

        response = requests.get(f"{API_URL}{path}", timeout=60, headers=header)

        if response.status_code != 200:
            if response.status_code == 429:
                raise TooManyRequests(
                    "Too many requests from this IP, please try again after 15 minutes"
                )
            else:
                raise InvalidAPIResponse(
                    f"Error {response.status_code} received from the API"
                )
        else:
            return response.json()

    def _header(self) -> dict:
        """Create default request header."""
        data = {
            "User-Agent": "HomeAssistant/Custom_Integration/Carnot",
            "Content-Type": "application/json",
            "apikey": self._apikey,
            "username": self._email,
        }
        return data
