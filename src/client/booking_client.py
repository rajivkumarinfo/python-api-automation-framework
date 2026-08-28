# Endpoint-specific client for the Restful-Booker API.
#  https://restful-booker.herokuapp.com/apidoc/index.html

from typing import Any, Optional

from requests import Response

from src.client.base_client import BaseAPIClient


class BookingClient(BaseAPIClient):
    # ---- health -----------------------------------------------------
    def ping(self) -> Response:
        return self.get("/ping")

    # ---- auth ---------------------------------------------------------
    def create_token(self, username: str, password: str) -> Response:
        return self.post("/auth", json={"username": username, "password": password})

    # ---- booking: read --------------------------------------------------
    def get_booking_ids(self, **filters: Any) -> Response:
        return self.get("/booking", params=filters or None)

    def get_booking(self, booking_id: int) -> Response:
        return self.get(f"/booking/{booking_id}")

    # ---- booking: write (require auth cookie) ----------------------------
    def create_booking(self, payload: dict) -> Response:
        return self.post("/booking", json=payload)

    def update_booking(self, booking_id: int, payload: dict) -> Response:
        return self.put(f"/booking/{booking_id}", json=payload)

    def partial_update_booking(self, booking_id: int, payload: dict) -> Response:
        return self.patch(f"/booking/{booking_id}", json=payload)

    def delete_booking(self, booking_id: int) -> Response:
        return self.delete(f"/booking/{booking_id}")
