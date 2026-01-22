import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

def geocode_one(address: str):
    """
    回傳 (lat, lon, display_name)
    找不到回傳 (None, None, None)
    """
    params = {"q": address, "format": "json", "limit": 1}
    headers = {"User-Agent": "address-to-latlng-ui/1.0"}  # 必填，避免被擋

    r = requests.get(NOMINATIM_URL, params=params, headers=headers, timeout=15)
    r.raise_for_status()
    data = r.json()

    if not data:
        return None, None, None

    return data[0].get("lat"), data[0].get("lon"), data[0].get("display_name")

