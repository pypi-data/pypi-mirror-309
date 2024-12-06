import re

import requests

from map_utils_xethhung12.Locator import LatLon


def get_url_from_latlon_object(latlon: LatLon) -> str:
    return get_url_from_latlon(latlon.lat, latlon.lon)

def get_url_from_latlon(lat: float, lon: float) -> str:
    return f"https://www.google.com/maps/@{lat},{lon}"


def get_lat_lon(url: str) -> LatLon | None:
    ps = [
        "^https://.*google.*/maps/place/[^/]+/@([\d.]+),([\d.]+),\d+z/.*$",
        "^https://.*google.*/maps/@([\d.]+),([\d.]+).*$"
    ]

    for s in ps:
        rs = re.compile(s).match(url)
        if rs is not None:
            return LatLon(float(rs[1]), float(rs[2]))
    return None


def get_real_url_of_google_map(url: str):
    response = requests.get(url, allow_redirects=False)
    if response.status_code in [301, 302, 307, 308]:
        return response.headers['Location']
    else:
        return url
