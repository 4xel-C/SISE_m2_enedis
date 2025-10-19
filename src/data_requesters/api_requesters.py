from typing import Any

import requests

from src.data_requesters.helper import retry_on_error


class Ademe_API_requester:
    """
    A class to interact with the ADEME API.
    """

    # Class attributes: base URLs for different datasets
    __base_url_existant = (
        "https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/lines"
    )
    __base_url_neuf = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe02neuf/lines"

    def __init__(
        self,
        size: int = 2500,
    ) -> None:
        """Initializes the Ademe_API_requester class.

        Args:
            size (int, optional): The number of results to return per page. Defaults to 2500.
            max_retries (int, optional): The maximum number of retry attempts for API requests. Defaults to 3.
            backoff_factor (int, optional): The backoff factor for retry delays. Defaults to 2.
        """
        self.__params: dict[str, int] = {"size": size}

    @retry_on_error(max_retries=3, backoff_factor=2)
    def __get_data(self, url: str, params: dict[str, Any] | None = None) -> dict | None:
        """Private method to get the crude data from the API passing the base URL and parameters.

        Returns:
            dict: The JSON response from the API or an error message.
        """
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses.
        return response.json()

    def __get_length(self, url: str, params: dict[str, Any] | None = None) -> int:
        """Private method to get the total number of results from the API for monitoring progress.

        Args:
            url (str): The base URL for the API request.
            params (dict[str, Any] | None, optional): The parameters for the API request. Defaults to None.
        """

        # Change the size of the parameter to 1 to speed up the request for total length.
        params = params | {"size": 1} if params else {"size": 1}

        data = self.__get_data(url, params=params)
        length = data.get("total", 0) if data else 0
        return length

    def get_bydepartement(
        self, departement: int, neuf: bool = False
    ) -> list[dict[str, Any]]:
        """Retrieve building data by department.

        Args:
            departement (int): The department code to filter by.
            neuf (bool, optional): Whether to filter for new buildings. Defaults to False.

        Returns:
            list[dict[str, Any]]: A list of dictionaries containing the building data.
        """
        # loggigng
        print(
            f"-- Fetching {'new' if neuf else 'existing'} building data for department: {departement} --"
        )

        # Build the parameter dictionary from the new department argument.
        params = self.__params | {"qs": f"code_departement_ban:{departement}"}

        # Initialize the all_data list to get all the data from the pagination loop.
        all_data: list[dict[str, Any]] = []

        # Initialize the URL to the base URL depending of if we want new or existing buildings.
        url = self.__base_url_existant if not neuf else self.__base_url_neuf

        total_length = self.__get_length(url, params=params)

        if total_length == 0:
            print("No data found for the specified department.")
            return all_data

        print(f"Total records to fetch for department: {total_length}")

        # Pagination loop.
        while url:
            data = self.__get_data(url, params=params)
            all_data.extend(data["results"])
            print(
                f"Fetched {len(data['results'])} records. Total so far: {len(all_data)}/{total_length} ({round(len(all_data) / total_length * 100, 2)}%)"
            )
            url = data.get("next")  # Get the next page URL.
            params = None  # Clear params for subsequent requests.
        # endwhile

        return all_data

    def get_all_data(self, neuf: bool = False) -> list[dict[str, Any]]:
        """Fetch the complete database of existing or new buildings.

        Args:
            neuf (bool, optional): Whether to filter for new buildings. Defaults to False.

        Returns:
            list[dict[str, Any]]: A list of dictionaries containing the building data.
        """
        # loggigng
        print(
            f"-- Fetching {'new' if neuf else 'existing'} building data for all departments --"
        )

        # Initialize the all_data list to get all the data from the pagination loop.
        all_data: list[dict[str, Any]] = []

        # Initialize the URL to the base URL depending of if we want new or existing buildings.
        url = self.__base_url_existant if not neuf else self.__base_url_neuf

        # Local copy of the default parameters (default size of fetched pages).
        params = self.__params.copy()

        total_length = self.__get_length(url, params=params)

        if total_length == 0:
            print("No data found.")
            return all_data

        print(f"Total records to fetch: {total_length}")

        # Pagination loop.
        while url:
            data = self.__get_data(url, params=params)
            all_data.extend(data["results"])
            print(
                f"Fetched {len(data['results'])} records. Total so far: {len(all_data)}/{total_length} ({round(len(all_data) / total_length * 100, 2)}%)"
            )
            url = data.get("next")  # Get the next page URL.
            params = None  # Clear params for subsequent requests.
        # endwhile
        return all_data


class Enedis_API_requester:
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

    @retry_on_error(max_retries=3, backoff_factor=2)
    def __get_data(self, params: dict[str, Any] | None = None) -> dict | None:
        """Private method to get data from the Enedis API.

        Args:
            params (dict[str, Any] | None, optional): The parameters for the API request. Defaults to None.

        Returns:
            dict | None: The JSON response from the API or None if an error occurred.
        """
        response = requests.get(self.__base_url, params=params)
        response.raise_for_status()  # Raise an error for bad responses.
        return response.json()

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
