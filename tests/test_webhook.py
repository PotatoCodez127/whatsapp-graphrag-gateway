# tests/test_webhook.py

import pytest
import webhook
from webhook import app


@pytest.fixture
def client():
    """Configures the Flask application for strict testing isolation."""
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_webhook_verification_success(client, monkeypatch):
    """
    Verifies that the GET /webhook endpoint successfully responds with the hub.challenge
    when the incoming verification token matches the server configuration.
    """
    # Isolate the verification variable regardless of local system environment variables
    monkeypatch.setattr(webhook, "VERIFY_TOKEN", "secure_mock_token")

    response = client.get(
        "/webhook?hub.mode=subscribe&hub.challenge=challenge_token_1234&hub.verify_token=secure_mock_token"
    )

    assert response.status_code == 200
    assert response.data.decode("utf-8") == "challenge_token_1234"


def test_webhook_verification_mismatch(client, monkeypatch):
    """
    Verifies that a 403 Forbidden status code is generated when an invalid
    verification token is passed to the handshake routing logic.
    """
    monkeypatch.setattr(webhook, "VERIFY_TOKEN", "secure_mock_token")

    response = client.get(
        "/webhook?hub.mode=subscribe&hub.challenge=challenge_token_1234&hub.verify_token=invalid_mismatch_token"
    )

    assert response.status_code == 403
    assert response.data.decode("utf-8") == "Verification token mismatch"