import requests
import os

class Client:

    def __init__(self, client):
        api_url_suffix = os.environ.get("API_URL_SUFFIX","http://nohost")
        self.client = client
        self.api_url = f"{api_url_suffix}/{client}"

    def post(self, json: dict):
        url = fr"{self.api_url}/"
        response = requests.post(url=self.api_url, json=json)
        return response

    def get(self):
        response = requests.get(url=self.api_url)
        return response

    def delete(self, json: dict):
        response = requests.delete(url=self.api_url, json=json)
        return response

    def patch(self, json: dict):
        response = requests.patch(url=self.api_url, json=json)
        return response

