import allure
import pytest

from src.client.booking_client import BookingClient
from src.schemas.booking_schema import (
    BOOKING_ID_LIST_SCHEMA,
    BOOKING_SCHEMA,
    CREATE_BOOKING_RESPONSE_SCHEMA,
)
from src.utils.retry import retry_on_assertion
from src.utils.schema_validator import assert_matches_schema


@allure.epic("Restful-Booker")
@allure.feature("Booking CRUD")
class TestBookingCrud:
    @pytest.mark.crud
    def test_create_booking(
        self, authenticated_client: BookingClient, booking_payload: dict
    ):
        response = authenticated_client.create_booking(booking_payload)

        assert response.status_code == 200
        body = response.json()
        assert_matches_schema(body, CREATE_BOOKING_RESPONSE_SCHEMA)
        assert body["booking"]["firstname"] == booking_payload["firstname"]

        # cleanup — this test creates its own booking rather than using the
        # `created_booking` fixture, on purpose, to demonstrate raw create()
        authenticated_client.delete_booking(body["bookingid"])

    @pytest.mark.crud
    def test_get_booking_by_id(
        self, authenticated_client: BookingClient, created_booking: dict
    ):
        response = authenticated_client.get_booking(created_booking["id"])

        assert response.status_code == 200
        assert_matches_schema(response.json(), BOOKING_SCHEMA)
        assert response.json()["firstname"] == created_booking["payload"]["firstname"]

    @pytest.mark.crud
    def test_update_booking(
        self,
        authenticated_client: BookingClient,
        created_booking: dict,
        booking_payload_factory,
    ):
        updated_payload = booking_payload_factory(lastname="UpdatedLastName")

        response = authenticated_client.update_booking(
            created_booking["id"], updated_payload
        )

        assert response.status_code == 200
        assert response.json()["lastname"] == "UpdatedLastName"

    @pytest.mark.crud
    def test_partial_update_booking(
        self, authenticated_client: BookingClient, created_booking: dict
    ):
        response = authenticated_client.partial_update_booking(
            created_booking["id"], {"firstname": "Patched"}
        )

        assert response.status_code == 200
        assert response.json()["firstname"] == "Patched"

    @pytest.mark.crud
    def test_delete_booking(
        self, authenticated_client: BookingClient, booking_payload: dict
    ):
        create_response = authenticated_client.create_booking(booking_payload)
        booking_id = create_response.json()["bookingid"]

        delete_response = authenticated_client.delete_booking(booking_id)
        assert delete_response.status_code in (200, 201)

        # Restful-Booker's demo backend is eventually consistent right after
        # a delete, so the follow-up read is wrapped with an app-level retry.
        _assert_booking_gone(authenticated_client, booking_id)

    @pytest.mark.regression
    def test_get_nonexistent_booking_returns_404(
        self, authenticated_client: BookingClient
    ):
        response = authenticated_client.get_booking(999_999_999)
        assert response.status_code == 404

    @pytest.mark.regression
    def test_get_booking_ids_supports_filtering(
        self, authenticated_client: BookingClient, created_booking: dict
    ):
        response = authenticated_client.get_booking_ids(
            firstname=created_booking["payload"]["firstname"],
            lastname=created_booking["payload"]["lastname"],
        )

        assert response.status_code == 200
        assert_matches_schema(response.json(), BOOKING_ID_LIST_SCHEMA)
        ids = [item["bookingid"] for item in response.json()]
        assert created_booking["id"] in ids


@retry_on_assertion
def _assert_booking_gone(client: BookingClient, booking_id: int) -> None:
    response = client.get_booking(booking_id)
    assert response.status_code == 404, "Deleted booking should 404"
