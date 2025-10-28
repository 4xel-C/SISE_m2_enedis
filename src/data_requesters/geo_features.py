from pathlib import Path

import pandas as pd
import requests

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CLIMATE_ZONES_PATH = BASE_DIR / "data" / "climate_zones.csv"

# Read the file for mapping.
df_zones = pd.read_csv(CLIMATE_ZONES_PATH)

# Convert in int.
df_zones["Departement"] = df_zones["Departement"].astype(int)

# Create a dict: zone -> list of department numbers.
CLIMATE_ZONES = df_zones.groupby("Zone climatique")["Departement"].apply(list).to_dict()


def _map_dept_to_zone(dept_int: int) -> str:
    for zone, deps in CLIMATE_ZONES.items():
        if dept_int in deps:
            return zone
    return "Unknown"


def _extract_department_from_feature(props: dict) -> str | None:
    """
    Try robustly to extract the department code from the geo feature properties returned
    by api-adresse.data.gouv.fr. Returns a string dept code (e.g. '13' or '2A') or None.
    """
    # 1) try 'context' first: often "13, Bouches-du-Rhône, Provence..."
    context = props.get("context") or ""
    if context:
        first = context.split(",")[0].strip()
        # often a numeric dept code
        if first.isdigit():
            return first.zfill(2)
        # sometimes context might include '2A'/'2B' or other forms: keep as-is
        if first.upper() in {"2A", "2B"}:
            return first.upper()

    # 2) try postcode (first 2 characters usually department for metropolitan FR)
    postcode = props.get("postcode")
    if postcode:
        # handle special overseas codes beginning with 97/98 -> these are 3-digit dept codes sometimes
        if postcode.startswith(("97", "98")):
            return postcode[:3]
        return postcode[:2]

    # 3) try citycode (INSEE) -> first two digits normally department number,
    # but for Corsica INSEE uses 2A/2B in a different field; citycode is numeric string
    citycode = props.get("citycode")
    if citycode and citycode.isdigit():
        return citycode[:2]

    return None


def get_zone_and_altitude(ville: str | None = None, insee: str | None = None):
    """
    Return {'zone_climatique': 'H1'|'H2'|'H3'|'Unknown', 'altitude_moyenne': float|None, 'dept': str|None, 'lat': float|None, 'lon': float|None}
    Uses api-adresse.data.gouv.fr to find department and coordinates.
    """
    result = {
        "zone_climatique": str,
        "altitude_moyenne": None,
        "dept": None,
        "lat": None,
        "lon": None,
    }

    # If insee provided, we can try to derive dept from it (insee is 5 chars INSEE code)
    if insee:
        try:
            # first two chars of INSEE usually department number (handles '2A'/'2B' if present)
            dept_from_insee = insee[:2]
            result["dept"] = dept_from_insee
        except Exception:
            result["dept"] = None

    # If we don't have dept yet, try geocoding the city
    if not result["dept"] and ville:
        url = "https://api-adresse.data.gouv.fr/search/"
        params = {"q": ville, "limit": 1}
        try:
            r = requests.get(url, params=params, timeout=8)
            r.raise_for_status()
            data = r.json()
            features = data.get("features", [])
            if not features:
                return result
            feat = features[0]
            props = feat.get("properties", {})
            geom = feat.get("geometry", {})
            coords = geom.get("coordinates", [None, None])
            lon, lat = coords[0], coords[1]
            result["lat"], result["lon"] = lat, lon

            dept_code = _extract_department_from_feature(props)
            result["dept"] = dept_code

            # Debug info: keep the raw context if you need to log later
            result["_context"] = props.get("context")
            result["_postcode"] = props.get("postcode")
            result["_citycode"] = props.get("citycode")
        except Exception:
            # network/timeout -> just return partial result
            return result

    # Normalize dept and map to int if possible
    dept = result.get("dept")
    if dept:
        # some dept strings could be e.g. '2A' or '2B' -> handle specially
        try:
            if dept.upper() in {"2A", "2B"}:
                # Corsica: map '2A' -> 20? (depends on your CLIMATE_ZONES mapping expectations)
                # Here we try to convert to numeric 20 to match mapping if needed
                dept_int = 20
            else:
                # sometimes dept may be '971' (overseas) -> allow int conversion
                dept_int = int(dept)
            zone = _map_dept_to_zone(dept_int)
            result["zone_climatique"] = zone
        except Exception:
            result["zone_climatique"] = None

    return result
