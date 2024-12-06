import json
import re

import requests

from map_utils_xethhung12.Locator import LatLon


class Geocode:
    def __init__(self, key):
        self.key = key

    def geocode_api_by_address(self, address: str, key: str)->dict:
        LocationParams = {'address': address, key: key}
        LocationURL = 'http://maps.googleapis.com/maps/api/geocode/json'
        r = requests.get(LocationURL, params=LocationParams)
        responseJson = json.loads(r.text)
        self.res = responseJson
        return self.res

    def get_size_of_result(self):
        return len(self.res)

    def get_lat_lon_obj(self, i=0)->LatLon:
        lat = float(self.res.get('results')[i]['geometry']['location']['lat'])
        lng = float(self.res.get('results')[i]['geometry']['location']['lng'])
        return LatLon(lat, lng)

    def get_address(self, i=0) -> str:
        return self.res.get('results')[i]['formatted_address']


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
