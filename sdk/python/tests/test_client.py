"""Unit tests for asterdex SDK — no network calls required."""

import time
from unittest.mock import MagicMock, patch

import pytest
from eth_account import Account

from asterdex.client import (
    CHAIN_ID_MAINNET,
    CHAIN_ID_TESTNET,
    MAINNET_BASE,
    TESTNET_BASE,
    AsterDexAuthError,
    AsterDexClient,
    AsterDexError,
    AsterDexRateLimitError,
    _build_sign_payload,
    _sign_v3,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

# Generate throwaway test keys at runtime to avoid GitHub secret scanning alerts.
# These keys are ephemeral and NEVER used on any real network.
_test_account = Account.create()
TEST_USER = "0x014c85ffb0fF2F2972237AA950B452f92C69Ae1D"  # placeholder address
TEST_SIGNER = _test_account.address
TEST_PRIVKEY = _test_account.key.hex()


@pytest.fixture
def public_client():
    """Client with no auth — for public endpoints only."""
    return AsterDexClient()


@pytest.fixture
def signed_client():
    """Client with test credentials."""
    return AsterDexClient(
        user=TEST_USER,
        signer=TEST_SIGNER,
        private_key=TEST_PRIVKEY,
        main_private_key=TEST_PRIVKEY,
    )


# ---------------------------------------------------------------------------
# Signing tests
# ---------------------------------------------------------------------------


class TestSignPayload:
    def test_sorts_keys_ascii(self):
        params = {"z": "3", "a": "1", "m": "2"}
        result = _build_sign_payload(params)
        assert result == "a=1&m=2&z=3"

    def test_boolean_lowercase(self):
        params = {"canSpotTrade": True, "canWithdraw": False}
        result = _build_sign_payload(params)
        assert "canSpotTrade=true" in result
        assert "canWithdraw=false" in result

    def test_empty_params(self):
        assert _build_sign_payload({}) == ""

    def test_single_param(self):
        assert _build_sign_payload({"symbol": "BTCUSDT"}) == "symbol=BTCUSDT"

    def test_numeric_values(self):
        params = {"leverage": 20, "quantity": "0.01"}
        result = _build_sign_payload(params)
        assert "leverage=20" in result
        assert "quantity=0.01" in result


class TestSignV3:
    def test_returns_required_fields(self):
        signed = _sign_v3(
            params={"symbol": "BTCUSDT"},
            user=TEST_USER,
            signer=TEST_SIGNER,
            private_key=TEST_PRIVKEY,
        )
        assert "user" in signed
        assert "signer" in signed
        assert "nonce" in signed
        assert "timestamp" in signed
        assert "signature" in signed
        assert "symbol" in signed

    def test_nonce_is_microseconds(self):
        signed = _sign_v3(
            params={},
            user=TEST_USER,
            signer=TEST_SIGNER,
            private_key=TEST_PRIVKEY,
        )
        nonce = int(signed["nonce"])
        now_us = int(time.time() * 1_000_000)
        # Nonce should be within 2 seconds of now
        assert abs(nonce - now_us) < 2_000_000

    def test_timestamp_is_milliseconds(self):
        signed = _sign_v3(
            params={},
            user=TEST_USER,
            signer=TEST_SIGNER,
            private_key=TEST_PRIVKEY,
        )
        ts = int(signed["timestamp"])
        now_ms = int(time.time() * 1_000)
        assert abs(ts - now_ms) < 2_000

    def test_signature_is_hex(self):
        signed = _sign_v3(
            params={"symbol": "BTCUSDT"},
            user=TEST_USER,
            signer=TEST_SIGNER,
            private_key=TEST_PRIVKEY,
        )
        sig = signed["signature"]
        # Should be valid hex (with or without 0x prefix)
        int(sig, 16)

    def test_preserves_original_params(self):
        signed = _sign_v3(
            params={"symbol": "ETHUSDT", "side": "BUY"},
            user=TEST_USER,
            signer=TEST_SIGNER,
            private_key=TEST_PRIVKEY,
        )
        assert signed["symbol"] == "ETHUSDT"
        assert signed["side"] == "BUY"

    def test_different_params_different_signature(self):
        sig1 = _sign_v3(
            params={"symbol": "BTCUSDT"},
            user=TEST_USER,
            signer=TEST_SIGNER,
            private_key=TEST_PRIVKEY,
        )["signature"]

        sig2 = _sign_v3(
            params={"symbol": "ETHUSDT"},
            user=TEST_USER,
            signer=TEST_SIGNER,
            private_key=TEST_PRIVKEY,
        )["signature"]

        assert sig1 != sig2


# ---------------------------------------------------------------------------
# Client initialization tests
# ---------------------------------------------------------------------------


class TestClientInit:
    def test_default_base_url(self, public_client):
        assert public_client.base_url == MAINNET_BASE

    def test_custom_base_url(self):
        client = AsterDexClient(base_url=TESTNET_BASE)
        assert client.base_url == TESTNET_BASE

    def test_trailing_slash_stripped(self):
        client = AsterDexClient(base_url="https://example.com/")
        assert client.base_url == "https://example.com"

    def test_chain_id_default(self, public_client):
        assert public_client.chain_id == CHAIN_ID_MAINNET

    def test_testnet_chain_id(self):
        client = AsterDexClient(chain_id=CHAIN_ID_TESTNET)
        assert client.chain_id == CHAIN_ID_TESTNET

    def test_user_agent_header(self, public_client):
        ua = public_client._session.headers.get("User-Agent", "")
        assert "AsterDexSDK-Python" in ua


# ---------------------------------------------------------------------------
# Error handling tests (mocked HTTP)
# ---------------------------------------------------------------------------


class TestErrorHandling:
    def _mock_response(self, status_code=200, json_data=None, text=""):
        mock = MagicMock()
        mock.status_code = status_code
        mock.text = text
        if json_data is not None:
            mock.json.return_value = json_data
        else:
            mock.json.side_effect = ValueError("No JSON")
        return mock

    @patch("asterdex.client.requests.Session.get")
    def test_rate_limit_429(self, mock_get, public_client):
        mock_get.return_value = self._mock_response(429)
        with pytest.raises(AsterDexRateLimitError) as exc_info:
            public_client.ping()
        assert exc_info.value.code == 429

    @patch("asterdex.client.requests.Session.get")
    def test_ip_banned_418(self, mock_get, public_client):
        mock_get.return_value = self._mock_response(418)
        with pytest.raises(AsterDexRateLimitError) as exc_info:
            public_client.ping()
        assert exc_info.value.code == 418

    @patch("asterdex.client.requests.Session.get")
    def test_api_error_code(self, mock_get, public_client):
        mock_get.return_value = self._mock_response(200, {"code": -1121, "msg": "Invalid symbol."})
        with pytest.raises(AsterDexError) as exc_info:
            public_client.get_ticker_price(symbol="FAKECOIN")
        assert exc_info.value.code == -1121

    @patch("asterdex.client.requests.Session.get")
    def test_auth_error(self, mock_get, public_client):
        mock_get.return_value = self._mock_response(
            200, {"code": -2015, "msg": "Invalid API-key, IP, or permissions for action."}
        )
        with pytest.raises(AsterDexAuthError):
            public_client.ping()

    @patch("asterdex.client.requests.Session.get")
    def test_success_returns_data(self, mock_get, public_client):
        expected = {"serverTime": 1234567890000}
        mock_get.return_value = self._mock_response(200, expected)
        result = public_client.get_server_time()
        assert result == expected

    def test_signed_request_without_key_raises(self, public_client):
        with pytest.raises(AsterDexAuthError):
            public_client.get_balance()


# ---------------------------------------------------------------------------
# Method parameter tests (no network)
# ---------------------------------------------------------------------------


class TestMethodParams:
    @patch("asterdex.client.requests.Session.get")
    def test_get_order_book_default_limit(self, mock_get, public_client):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=MagicMock(return_value={"bids": [], "asks": []}),
        )
        public_client.get_order_book("BTCUSDT")
        call_kwargs = mock_get.call_args
        params = call_kwargs.kwargs.get("params") or call_kwargs[1].get("params", {})
        assert params["limit"] == 500

    @patch("asterdex.client.requests.Session.get")
    def test_optional_symbol_none(self, mock_get, public_client):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=MagicMock(return_value=[]),
        )
        public_client.get_ticker_price()
        call_kwargs = mock_get.call_args
        params = call_kwargs.kwargs.get("params") or call_kwargs[1].get("params", {})
        assert "symbol" not in params

    @patch("asterdex.client.requests.Session.get")
    def test_optional_symbol_set(self, mock_get, public_client):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=MagicMock(return_value={"symbol": "BTCUSDT", "price": "50000"}),
        )
        public_client.get_ticker_price(symbol="BTCUSDT")
        call_kwargs = mock_get.call_args
        params = call_kwargs.kwargs.get("params") or call_kwargs[1].get("params", {})
        assert params["symbol"] == "BTCUSDT"
