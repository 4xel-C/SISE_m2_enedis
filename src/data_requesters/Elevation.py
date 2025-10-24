import time

import requests

from src.data_requesters.helper import retry_on_error


class Elevation_API_requester:
    """
    A class to interact with the Elevation API to get the altitude from geographical coordinates.
    """

    __base_url = "https://api.elevationapi.com/api/Elevation"

    @retry_on_error()
    def get_elevation(self, lat: float, lon: float, delay=0) -> float | None:
        """Get elevation data for given locations. Exemple request: https://api.elevationapi.com/api/Elevation?lat=12&lon=32

        Args:
            lat (float): The latitude of the location.
            lon (float): The longitude of the location.

        Returns:
            float | None: The elevation data or None if an error occurred.
        """

        if not lat or not lon:
            return None

        # Prepare the paramaters
        params = {"lat": lat, "lon": lon}

        if delay:
            time.sleep(delay)

        response = requests.get(self.__base_url, params=params)
        response.raise_for_status()  # Raise an error for bad responses.
        data = response.json()
        print("data recuperated")

        if data["resultCount"] == 0:
            return None
        else:
            return data["geoPoints"][0]["elevation"]
