from typing import Optional
import requests


class PyroApiClient:
    def __init__(self, host: str, email: str, apikey: str):
        self.host = host
        self.email = email
        self.apikey = apikey
        self.session = requests.session()
        self.session.headers.update({"Content-Type": "application/json"})
        self._login()

    def _login(self):
        url = f"{self.host}/auth/login"
        body = {"email": self.email, "password": self.apikey}
        resp = self.session.post(url, json=body)
        resp.raise_for_status()

    def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[dict] = None,
        **kwargs,
    ):
        url = f"{self.host}/{endpoint}"
        _kwargs = {**kwargs}

        if data is not None:
            if method.lower() == "post":
                _kwargs["json"] = data
            else:
                _kwargs["params"] = data

        resp = self.session.request(method, url, **_kwargs)
        resp.raise_for_status()
        return resp.json()
