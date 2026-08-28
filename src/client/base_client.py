#Reusable HTTP client abstraction.Every API-specific client (see booking_client.py) is built on top of this class 
# so that retries, timeouts, headers and request/response logging are implemented once instead of being duplicated in each test.

import json
import logging
from typing import Any, Optional

import allure
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.config import settings

logger = logging.getLogger(__name__)


class BaseAPIClient:
    def __init__(self, base_url: str = settings.BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        self._mount_retry_adapter()

    #Transport-level retries for connection errors and 5xx responses
    def _mount_retry_adapter(self) -> None:
        retry_strategy = Retry(
            total=settings.RETRY_TOTAL,
            backoff_factor=settings.RETRY_BACKOFF_FACTOR,
            status_forcelist=settings.RETRY_STATUS_FORCELIST,
            allowed_methods=("GET", "PUT", "DELETE", "OPTIONS", "HEAD"),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def set_auth_cookie(self, token: str) -> None:
        """Restful-Booker uses a Cookie-based token for write operations."""
        self.session.headers.update({"Cookie": f"token={token}"})

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    @allure.step("HTTP {method} {path}")
    def request(
        self,
        method: str,
        path: str,
        expected_status: Optional[int] = None,
        **kwargs: Any,
    ) -> requests.Response:
        kwargs.setdefault("timeout", settings.REQUEST_TIMEOUT)
        url = self._url(path)

        self._attach("Request", {
            "method": method,
            "url": url,
            "params": kwargs.get("params"),
            "json": kwargs.get("json"),
        })

        response = self.session.request(method, url, **kwargs)

        self._attach("Response", {
            "status_code": response.status_code,
            "body": self._safe_json(response),
        })

        if expected_status is not None and response.status_code != expected_status:
            raise AssertionError(
                f"{method} {url} -> expected HTTP {expected_status}, "
                f"got {response.status_code}. Body: {self._safe_json(response)}"
            )
        return response

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", path, **kwargs)

    @staticmethod
    def _safe_json(response: requests.Response):
        try:
            return response.json()
        except ValueError:
            return response.text

    @staticmethod
    def _attach(name: str, payload: Any) -> None:
        try:
            body = json.dumps(payload, indent=2, default=str)
        except TypeError:
            body = str(payload)
        allure.attach(body, name=name, attachment_type=allure.attachment_type.JSON)
        logger.info("%s: %s", name, body)
