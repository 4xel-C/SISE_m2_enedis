from typing import Any, Callable, Optional

from src.data_requesters.base_api import BaseAPIRequester


class Ademe_API_requester(BaseAPIRequester):
    """
    A class to interact with the ADEME API.
    """

    # Class attributes: base URLs for different datasets
    __base_url_existant = (
        "https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant"
    )

    __base_url_neuf = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe02neuf"

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
        self.__size: int = size

    def __get_length(self, url: str, params: dict[str, Any] | None = None) -> int:
        """Private method to get the total number of results from the API for monitoring progress.

        Args:
            url (str): The base URL for the API request.
            params (dict[str, Any] | None, optional): The parameters for the API request. Defaults to None.
        """

        # Change the size of the parameter to 1 to speed up the request for total length.
        params = params | {"size": 1} if params else {"size": 1}

        data = self._get_data(url, params=params)
        length = data.get("total", 0) if data else 0
        return length

    def custom_lines_request(
        self,
        neuf: bool = False,
        limit: int | None = None,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        **kwargs
    ) -> list[dict[str, Any]]:
        """Make a custom request to the lines endpoint with additional parameters, while handling the looping requests for pagination.

        Args:
            neuf (bool, optional): Whether to request for new houses. Defaults to False.
            limit (int | None, optional): The number of results we want to limit the request to. Defaults to None.
            progress_callback (Optional[Callable[[int, int], None]], optional): A callback function to report progress. Defaults to None.
            **kwargs: Additional parameters to include in the request.

        Returns:
            dict: The response from the API.
        """
        # Initialize the URL to the base URL depending of if we want new or existing buildings.
        url = self.__base_url_existant if not neuf else self.__base_url_neuf
        url += "/lines"  # Endpoint for lines data.

        # Setting the parameters for the request.
        params = {"size": self.__size} | kwargs

        # Initialize the all_data list to get all the data from the pagination loop.
        all_data: list[dict[str, Any]] = []

        total_length = self.__get_length(url, params=params)
        if limit is not None and limit < total_length:
            total_length = limit

        if progress_callback:
            progress_callback(0, total_length)

        if total_length == 0:
            print("No data found for the specified department.")
            return all_data

        print(f"Total records to fetch: {total_length}")

        # Pagination loop.
        while url:
            # Break the loop if we reached the limit.
            if limit is not None and len(all_data) >= limit:
                break

            data = self._get_data(url, params=params)
            all_data.extend(data["results"])

            if progress_callback:
                progress_callback(len(all_data), total_length)

            print(
                f"Fetched {len(data['results'])} records. Total so far: {len(all_data)}/{total_length} ({round(len(all_data) / total_length * 100, 2)}%)"
            )
            url = data.get("next")  # Get the next page URL.
            params = None  # Clear params for subsequent requests.
        # endwhile

        return all_data

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
        params = {"size": self.__size} | {"qs": f"code_departement_ban:{departement}"}

        # Initialize the all_data list to get all the data from the pagination loop.
        all_data: list[dict[str, Any]] = []

        # Initialize the URL to the base URL depending of if we want new or existing buildings.
        url = self.__base_url_existant if not neuf else self.__base_url_neuf
        url += "/lines"  # Endpoint for lines data.

        total_length = self.__get_length(url, params=params)

        if total_length == 0:
            print("No data found for the specified department.")
            return all_data

        print(f"Total records to fetch for department: {total_length}")

        # Pagination loop.
        while url:
            data = self._get_data(url, params=params)
            all_data.extend(data["results"])
            print(
                f"Fetched {len(data['results'])} records. Total so far: {len(all_data)}/{total_length} ({round(len(all_data) / total_length * 100, 2)}%)"
            )
            url = data.get("next")  # Get the next page URL.
            params = None  # Clear params for subsequent requests.
        # endwhile

        return all_data

    def get_all_departments_count(self, neuf: bool = False) -> list:
        """Fetch the aggregated count of all departments.

        Args:
            neuf (bool, optional): Whether to request for new houses. Defaults to False.

        Returns:
            list: A list containing the count for each department.
        """
        # Initialize the URL to the base URL depending of if we want new or existing buildings.
        url = self.__base_url_existant if not neuf else self.__base_url_neuf
        url += "/values_agg"  # Endpoint for values aggregation.

        data = self._get_data(
            url, params={"agg_size": 400, "field": "code_departement_ban"}
        )

        return data.get("aggs", []) if data else []

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
        url += "/lines"  # Endpoint for lines data.

        # Default size parameter.
        params = {"size": self.__size}

        total_length = self.__get_length(url, params=params)

        if total_length == 0:
            print("No data found.")
            return all_data

        print(f"Total records to fetch: {total_length}")

        # Pagination loop.
        while url:
            data = self._get_data(url, params=params)
            all_data.extend(data["results"])
            print(
                f"Fetched {len(data['results'])} records. Total so far: {len(all_data)}/{total_length} ({round(len(all_data) / total_length * 100, 2)}%)"
            )
            url = data.get("next")  # Get the next page URL.
            params = None  # Clear params for subsequent requests.
        # endwhile
        return all_data
