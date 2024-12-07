import requests

def get_request_json(url: str, params: dict | None = None):
    if params != None:
        r = requests.get(url, params=params)
    else:
        r = requests.get(url)
    return r.json()
