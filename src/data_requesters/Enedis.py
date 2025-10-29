from typing import Any

import requests

from src.data_requesters.base_api import BaseAPIRequester


class Enedis_API_requester(BaseAPIRequester):
    """
    A class to interact with the Enedis API.
    """

    __base_url = "https://data.enedis.fr/api/explore/v2.1/catalog/datasets/consommation-annuelle-residentielle-par-adresse/records"

    def __init__(self, limit: int = 100) -> None:
        """Initializes the Enedis_API_requester class.

        Args:
            limit (int, optional): The number of results to return per page. Defaults to 100.
        """
        self.__params: dict[str, int] = {"limit": limit}
        self.__all_iris_codes: list[str] = []

    def __get_length(self, params: dict[str, Any] | None = None) -> int:
        """Private method to get the total number of results from the API for monitoring progress.

        Args:
            params (dict[str, Any] | None, optional): The parameters for the API request. Defaults to None.
        """

        # Change the limit of the parameter to 1 to speed up the request for total length.
        params = params | {"limit": 0} if params else {"limit": 0}

        response = requests.get(self.__base_url, params=params)
        response.raise_for_status()  # Raise an error for bad responses.
        length = response.json().get("total_count", 0)
        return length
