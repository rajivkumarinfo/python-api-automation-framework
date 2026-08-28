import allure
import pytest

from src.client.booking_client import BookingClient
from src.config import settings
from src.schemas.booking_schema import AUTH_TOKEN_SCHEMA
from src.utils.schema_validator import assert_matches_schema


@allure.epic("Restful-Booker")
@allure.feature("Auth")
@pytest.mark.smoke
def test_create_token_with_valid_credentials(api_client: BookingClient):
    response = api_client.create_token(
        settings.AUTH_USERNAME, settings.AUTH_PASSWORD
    )

    assert response.status_code == 200
    assert_matches_schema(response.json(), AUTH_TOKEN_SCHEMA)


@allure.epic("Restful-Booker")
@allure.feature("Auth")
@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password",
    [
        pytest.param("wrong_user", "wrong_pass", id="invalid_both"),
        pytest.param(settings.AUTH_USERNAME, "wrong_pass", id="invalid_password"),
        pytest.param("", "", id="empty_credentials"),
    ],
)
def test_create_token_with_invalid_credentials(
    api_client: BookingClient, username: str, password: str
):
    response = api_client.create_token(username, password)

    assert response.status_code == 200, "Restful-Booker returns 200 with a reason field"
    body = response.json()
    assert "token" not in body
    assert body.get("reason") == "Bad credentials"
