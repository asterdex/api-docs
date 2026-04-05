"""
AsterDex Python SDK — Community Edition by Kairos Lab.

Handles V3 EIP-712 authentication, nonce management, and all documented
+ undocumented endpoints.
"""

from __future__ import annotations

import time
from typing import Any
from urllib.parse import urlencode

import requests
from eth_account import Account

# eth_account < 0.13: encode_structured_data(primitive)
# eth_account >= 0.13: encode_typed_data(full_message=...)
_USE_NEW_ETH_ACCOUNT = False
try:
    from eth_account.messages import encode_structured_data as _encode_legacy
except ImportError:
    _USE_NEW_ETH_ACCOUNT = True
    from eth_account.messages import encode_typed_data as _encode_new


def _encode_eip712(typed_data: dict):
    """Compat wrapper for EIP-712 encoding across eth_account versions."""
    if _USE_NEW_ETH_ACCOUNT:
        return _encode_new(full_message=typed_data)
    return _encode_legacy(typed_data)


__version__ = "0.1.0"
__author__ = "Kairos Lab <https://github.com/Valisthea>"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAINNET_BASE = "https://fapi.asterdex.com"
TESTNET_BASE = "https://testnet-fapi.asterdex.com"
MAINNET_WS = "wss://fstream.asterdex.com"
TESTNET_WS = "wss://testnet-fstream.asterdex.com"

CHAIN_ID_MAINNET = 1666
CHAIN_ID_TESTNET = 714

EIP712_DOMAIN = {
    "name": "AsterSignTransaction",
    "version": "1",
    "chainId": CHAIN_ID_MAINNET,
    "verifyingContract": "0x0000000000000000000000000000000000000000",
}

# Primary types that require main account signing
MAIN_SIGNER_TYPES = frozenset(
    {
        "ApproveAgent",
        "UpdateAgent",
        "DelAgent",
        "ApproveBuilder",
        "UpdateBuilder",
        "DelBuilder",
    }
)


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class AsterDexError(Exception):
    """Base exception for AsterDex SDK errors."""

    def __init__(self, code: int, message: str, response: dict | None = None):
        self.code = code
        self.message = message
        self.response = response
        super().__init__(f"[{code}] {message}")


class AsterDexAuthError(AsterDexError):
    """Authentication or signature error."""


class AsterDexRateLimitError(AsterDexError):
    """Rate limit exceeded."""


# ---------------------------------------------------------------------------
# Signing utilities
# ---------------------------------------------------------------------------


def _build_sign_payload(params: dict[str, Any]) -> str:
    """Sort params by ASCII key order and build signing payload string."""
    sorted_keys = sorted(params.keys())
    parts = []
    for key in sorted_keys:
        value = params[key]
        if isinstance(value, bool):
            value = str(value).lower()
        parts.append(f"{key}={value}")
    return "&".join(parts)


def _sign_v3(
    params: dict[str, Any],
    user: str,
    signer: str,
    private_key: str,
    chain_id: int = CHAIN_ID_MAINNET,
    use_main_key: bool = False,
    primary_type: str | None = None,
) -> dict[str, Any]:
    """
    Build and sign a V3 request using EIP-712 typed data.

    Returns the signed parameters dict ready for submission.
    """
    nonce = str(int(time.time() * 1_000_000))  # microseconds
    timestamp = str(int(time.time() * 1_000))  # milliseconds

    sign_params = {**params, "user": user, "signer": signer, "nonce": nonce}
    payload_str = _build_sign_payload(sign_params)

    # Build EIP-712 typed data
    typed_data: dict[str, Any] = {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "Message": [{"name": "msg", "type": "string"}],
        },
        "primaryType": "Message",
        "domain": {
            "name": "AsterSignTransaction",
            "version": "1",
            "chainId": chain_id,
            "verifyingContract": "0x0000000000000000000000000000000000000000",
        },
        "message": {"msg": payload_str},
    }

    # Override primary_type for agent/builder operations
    if primary_type:
        typed_data["primaryType"] = primary_type

    signable = _encode_eip712(typed_data)
    signed = Account.sign_message(signable, private_key=private_key)

    return {
        **params,
        "user": user,
        "signer": signer,
        "nonce": nonce,
        "timestamp": timestamp,
        "signature": signed.signature.hex(),
    }


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------


class AsterDexClient:
    """
    AsterDex V3 API client.

    Usage::

        client = AsterDexClient(
            user="0xYourMainWallet",
            signer="0xYourAgentWallet",
            private_key="0xAgentPrivateKey",
        )

        # Public endpoint — no auth
        info = client.get_exchange_info()

        # Signed endpoint
        order = client.place_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity="0.01",
        )
    """

    def __init__(
        self,
        user: str = "",
        signer: str = "",
        private_key: str = "",
        main_private_key: str = "",
        base_url: str = MAINNET_BASE,
        chain_id: int = CHAIN_ID_MAINNET,
        timeout: int = 10,
        builder: str = "",
    ):
        self.user = user
        self.signer = signer
        self.private_key = private_key
        self.main_private_key = main_private_key
        self.base_url = base_url.rstrip("/")
        self.chain_id = chain_id
        self.timeout = timeout
        self.builder = builder

        self._session = requests.Session()
        self._session.headers.update(
            {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": f"AsterDexSDK-Python/{__version__}",
            }
        )

    # ------------------------------------------------------------------
    # Internal HTTP helpers
    # ------------------------------------------------------------------

    def _request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        signed: bool = False,
        primary_type: str | None = None,
        use_main_key: bool = False,
    ) -> Any:
        """Execute an API request."""
        url = f"{self.base_url}{path}"
        params = params or {}

        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        if signed:
            key = self.main_private_key if use_main_key else self.private_key
            if not key:
                raise AsterDexAuthError(
                    -1,
                    "Private key required for signed requests. "
                    "Use main_private_key for agent/builder operations.",
                )
            params = _sign_v3(
                params=params,
                user=self.user,
                signer=self.signer,
                private_key=key,
                chain_id=self.chain_id,
                use_main_key=use_main_key,
                primary_type=primary_type,
            )

        try:
            if method == "GET":
                resp = self._session.get(url, params=params, timeout=self.timeout)
            elif method == "POST":
                resp = self._session.post(url, data=urlencode(params), timeout=self.timeout)
            elif method == "DELETE":
                resp = self._session.delete(url, data=urlencode(params), timeout=self.timeout)
            elif method == "PUT":
                resp = self._session.put(url, data=urlencode(params), timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
        except requests.exceptions.RequestException as exc:
            raise AsterDexError(-1, f"Network error: {exc}") from exc

        # Handle HTTP-level errors
        if resp.status_code == 429:
            raise AsterDexRateLimitError(429, "Rate limit exceeded — slow down requests")
        if resp.status_code == 418:
            raise AsterDexRateLimitError(418, "IP banned — continued requests after rate limit")

        try:
            data = resp.json()
        except ValueError as exc:
            if resp.status_code >= 400:
                raise AsterDexError(resp.status_code, resp.text) from exc
            return resp.text

        # Handle API-level errors
        if isinstance(data, dict) and "code" in data and data["code"] != 200:
            code = data.get("code", -1)
            msg = data.get("msg", "Unknown error")
            if code in (-2015, -1022, -1021):
                raise AsterDexAuthError(code, msg, data)
            raise AsterDexError(code, msg, data)

        return data

    def _public(self, path: str, params: dict | None = None) -> Any:
        return self._request("GET", path, params)

    def _signed_get(self, path: str, params: dict | None = None) -> Any:
        return self._request("GET", path, params, signed=True)

    def _signed_post(
        self,
        path: str,
        params: dict | None = None,
        primary_type: str | None = None,
        use_main_key: bool = False,
    ) -> Any:
        return self._request(
            "POST",
            path,
            params,
            signed=True,
            primary_type=primary_type,
            use_main_key=use_main_key,
        )

    def _signed_delete(
        self,
        path: str,
        params: dict | None = None,
        primary_type: str | None = None,
        use_main_key: bool = False,
    ) -> Any:
        return self._request(
            "DELETE",
            path,
            params,
            signed=True,
            primary_type=primary_type,
            use_main_key=use_main_key,
        )

    # ==================================================================
    # PUBLIC ENDPOINTS
    # ==================================================================

    def ping(self) -> dict:
        """Test connectivity."""
        return self._public("/fapi/v3/ping")

    def get_server_time(self) -> dict:
        """Get server time."""
        return self._public("/fapi/v3/time")

    def get_exchange_info(self) -> dict:
        """Get exchange rules, symbol list, and filters."""
        return self._public("/fapi/v3/exchangeInfo")

    def get_order_book(self, symbol: str, limit: int = 500) -> dict:
        """Get order book depth."""
        return self._public("/fapi/v3/depth", {"symbol": symbol, "limit": limit})

    def get_recent_trades(self, symbol: str, limit: int = 500) -> list:
        """Get recent trades."""
        return self._public("/fapi/v3/trades", {"symbol": symbol, "limit": limit})

    def get_historical_trades(
        self, symbol: str, limit: int = 500, from_id: int | None = None
    ) -> list:
        """Get older trades."""
        params: dict[str, Any] = {"symbol": symbol, "limit": limit}
        if from_id is not None:
            params["fromId"] = from_id
        return self._public("/fapi/v3/historicalTrades", params)

    def get_agg_trades(
        self,
        symbol: str,
        from_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list:
        """Get compressed/aggregate trades."""
        params: dict[str, Any] = {"symbol": symbol, "limit": limit}
        if from_id is not None:
            params["fromId"] = from_id
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        return self._public("/fapi/v3/aggTrades", params)

    def get_klines(
        self,
        symbol: str,
        interval: str,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list:
        """Get kline/candlestick data."""
        params: dict[str, Any] = {"symbol": symbol, "interval": interval, "limit": limit}
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        return self._public("/fapi/v3/klines", params)

    def get_mark_price(self, symbol: str | None = None) -> Any:
        """Get mark price and funding rate."""
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self._public("/fapi/v3/premiumIndex", params)

    def get_funding_rate(
        self,
        symbol: str,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 100,
    ) -> list:
        """Get funding rate history."""
        params: dict[str, Any] = {"symbol": symbol, "limit": limit}
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        return self._public("/fapi/v3/fundingRate", params)

    def get_funding_info(self) -> list:
        """Get funding rate configuration for all symbols."""
        return self._public("/fapi/v3/fundingInfo")

    def get_ticker_24hr(self, symbol: str | None = None) -> Any:
        """Get 24hr ticker price change statistics."""
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self._public("/fapi/v3/ticker/24hr", params)

    def get_ticker_price(self, symbol: str | None = None) -> Any:
        """Get latest price for symbol(s)."""
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self._public("/fapi/v3/ticker/price", params)

    def get_book_ticker(self, symbol: str | None = None) -> Any:
        """Get best bid/ask for symbol(s)."""
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self._public("/fapi/v3/ticker/bookTicker", params)

    def get_open_interest(self, symbol: str) -> dict:
        """
        Get open interest (UNDOCUMENTED endpoint).

        Returns one-sided OI in base-asset units.
        To match UI: OI_USDT ≈ openInterest × 2 × price
        """
        return self._public("/fapi/v3/openInterest", {"symbol": symbol})

    def get_index_references(self, symbol: str | None = None) -> Any:
        """Get index price reference data."""
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self._public("/fapi/v3/indexreferences", params)

    # ==================================================================
    # TRADING ENDPOINTS
    # ==================================================================

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: str | None = None,
        price: str | None = None,
        time_in_force: str | None = None,
        reduce_only: bool | None = None,
        new_client_order_id: str | None = None,
        stop_price: str | None = None,
        close_position: bool | None = None,
        activation_price: str | None = None,
        callback_rate: str | None = None,
        working_type: str | None = None,
        new_order_resp_type: str | None = None,
        position_side: str | None = None,
    ) -> dict:
        """Place a new order."""
        params: dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
        }
        optionals = {
            "quantity": quantity,
            "price": price,
            "timeInForce": time_in_force,
            "reduceOnly": reduce_only,
            "newClientOrderId": new_client_order_id,
            "stopPrice": stop_price,
            "closePosition": close_position,
            "activationPrice": activation_price,
            "callbackRate": callback_rate,
            "workingType": working_type,
            "newOrderRespType": new_order_resp_type,
            "positionSide": position_side,
        }
        for k, v in optionals.items():
            if v is not None:
                params[k] = v

        if self.builder:
            params["builder"] = self.builder

        return self._signed_post("/fapi/v3/order", params)

    def place_batch_orders(self, orders: list[dict]) -> list:
        """
        Place multiple orders at once.

        Each order in the list should be a dict with the same params as
        place_order (symbol, side, type, quantity, etc.).
        """
        import json

        return self._signed_post(
            "/fapi/v3/batchOrders",
            {"batchOrders": json.dumps(orders)},
        )

    def cancel_order(
        self,
        symbol: str,
        order_id: int | None = None,
        orig_client_order_id: str | None = None,
    ) -> dict:
        """Cancel an active order."""
        params: dict[str, Any] = {"symbol": symbol}
        if order_id is not None:
            params["orderId"] = order_id
        if orig_client_order_id is not None:
            params["origClientOrderId"] = orig_client_order_id
        return self._signed_delete("/fapi/v3/order", params)

    def cancel_all_orders(self, symbol: str) -> dict:
        """Cancel all open orders on a symbol."""
        return self._signed_delete("/fapi/v3/allOpenOrders", {"symbol": symbol})

    def cancel_batch_orders(
        self,
        symbol: str,
        order_ids: list[int] | None = None,
        client_order_ids: list[str] | None = None,
    ) -> list:
        """Cancel multiple orders."""
        import json

        params: dict[str, Any] = {"symbol": symbol}
        if order_ids:
            params["orderIdList"] = json.dumps(order_ids)
        if client_order_ids:
            params["origClientOrderIdList"] = json.dumps(client_order_ids)
        return self._signed_delete("/fapi/v3/batchOrders", params)

    def set_countdown_cancel(self, symbol: str, countdown_time: int) -> dict:
        """
        Auto-cancel all orders after countdown_time milliseconds.
        Set countdown_time=0 to cancel the countdown.
        """
        return self._signed_post(
            "/fapi/v3/countdownCancelAll",
            {"symbol": symbol, "countdownTime": countdown_time},
        )

    def noop(self) -> dict:
        """
        Send a noop request (used for fast cancel triggering).
        Resets the internal sequence counter.
        """
        return self._signed_post("/fapi/v3/noop")

    # ==================================================================
    # ACCOUNT ENDPOINTS
    # ==================================================================

    def get_order(
        self,
        symbol: str,
        order_id: int | None = None,
        orig_client_order_id: str | None = None,
    ) -> dict:
        """Query a specific order."""
        params: dict[str, Any] = {"symbol": symbol}
        if order_id is not None:
            params["orderId"] = order_id
        if orig_client_order_id:
            params["origClientOrderId"] = orig_client_order_id
        return self._signed_get("/fapi/v3/order", params)

    def get_open_order(
        self,
        symbol: str,
        order_id: int | None = None,
        orig_client_order_id: str | None = None,
    ) -> dict:
        """Query current open order."""
        params: dict[str, Any] = {"symbol": symbol}
        if order_id is not None:
            params["orderId"] = order_id
        if orig_client_order_id:
            params["origClientOrderId"] = orig_client_order_id
        return self._signed_get("/fapi/v3/openOrder", params)

    def get_open_orders(self, symbol: str | None = None) -> list:
        """Get all current open orders."""
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self._signed_get("/fapi/v3/openOrders", params)

    def get_all_orders(
        self,
        symbol: str,
        order_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list:
        """Get all orders (including filled)."""
        params: dict[str, Any] = {"symbol": symbol, "limit": limit}
        if order_id is not None:
            params["orderId"] = order_id
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        return self._signed_get("/fapi/v3/allOrders", params)

    def get_balance(self) -> list:
        """Get futures account balance."""
        return self._signed_get("/fapi/v3/balance")

    def get_account(self) -> dict:
        """Get account information with margin data."""
        return self._signed_get("/fapi/v3/accountWithJoinMargin")

    def get_positions(self, symbol: str | None = None) -> list:
        """Get position information."""
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self._signed_get("/fapi/v3/positionRisk", params)

    def get_user_trades(
        self,
        symbol: str,
        start_time: int | None = None,
        end_time: int | None = None,
        from_id: int | None = None,
        limit: int = 500,
    ) -> list:
        """Get account trade list."""
        params: dict[str, Any] = {"symbol": symbol, "limit": limit}
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if from_id is not None:
            params["fromId"] = from_id
        return self._signed_get("/fapi/v3/userTrades", params)

    def get_income(
        self,
        symbol: str | None = None,
        income_type: str | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 100,
    ) -> list:
        """Get income history."""
        params: dict[str, Any] = {"limit": limit}
        if symbol:
            params["symbol"] = symbol
        if income_type:
            params["incomeType"] = income_type
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        return self._signed_get("/fapi/v3/income", params)

    def get_leverage_brackets(self, symbol: str | None = None) -> Any:
        """
        Get notional and leverage brackets.

        Returns tiered margin model with maxLeverage, notionalCap,
        maintMarginRatio, and cum (offset) for each tier.
        """
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self._signed_get("/fapi/v3/leverageBracket", params)

    def get_adl_quantile(self, symbol: str | None = None) -> Any:
        """Get ADL quantile estimation."""
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self._signed_get("/fapi/v3/adlQuantile", params)

    def get_force_orders(
        self,
        symbol: str | None = None,
        auto_close_type: str | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 50,
    ) -> list:
        """Get forced liquidation orders."""
        params: dict[str, Any] = {"limit": limit}
        if symbol:
            params["symbol"] = symbol
        if auto_close_type:
            params["autoCloseType"] = auto_close_type
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        return self._signed_get("/fapi/v3/forceOrders", params)

    def get_commission_rate(self, symbol: str) -> dict:
        """Get user commission rate for a symbol."""
        return self._signed_get("/fapi/v3/commissionRate", {"symbol": symbol})

    # ==================================================================
    # POSITION & MARGIN
    # ==================================================================

    def change_leverage(self, symbol: str, leverage: int) -> dict:
        """Change initial leverage for a symbol."""
        return self._signed_post(
            "/fapi/v3/leverage",
            {"symbol": symbol, "leverage": leverage},
        )

    def change_margin_type(self, symbol: str, margin_type: str) -> dict:
        """Change margin type (ISOLATED or CROSSED)."""
        return self._signed_post(
            "/fapi/v3/marginType",
            {"symbol": symbol, "marginType": margin_type},
        )

    def modify_position_margin(
        self, symbol: str, amount: str, margin_type: int, position_side: str | None = None
    ) -> dict:
        """
        Modify isolated position margin.
        margin_type: 1 = add, 2 = reduce
        """
        params: dict[str, Any] = {
            "symbol": symbol,
            "amount": amount,
            "type": margin_type,
        }
        if position_side:
            params["positionSide"] = position_side
        return self._signed_post("/fapi/v3/positionMargin", params)

    def change_position_mode(self, dual_side: bool) -> dict:
        """Change position mode. True = Hedge Mode, False = One-way."""
        return self._signed_post(
            "/fapi/v3/positionSide/dual",
            {"dualSidePosition": str(dual_side).lower()},
        )

    def get_position_mode(self) -> dict:
        """Get current position mode."""
        return self._signed_get("/fapi/v3/positionSide/dual")

    def change_multi_assets_mode(self, multi_assets: bool) -> dict:
        """Change multi-assets mode."""
        return self._signed_post(
            "/fapi/v3/multiAssetsMargin",
            {"multiAssetsMargin": str(multi_assets).lower()},
        )

    def get_multi_assets_mode(self) -> dict:
        """Get current multi-assets mode."""
        return self._signed_get("/fapi/v3/multiAssetsMargin")

    # ==================================================================
    # TRANSFER
    # ==================================================================

    def transfer(self, asset: str, amount: str, transfer_type: int) -> dict:
        """
        Transfer between futures and spot.
        transfer_type: 1 = spot→futures, 2 = futures→spot
        """
        return self._signed_post(
            "/fapi/v3/asset/wallet/transfer",
            {"asset": asset, "amount": amount, "type": transfer_type},
        )

    # ==================================================================
    # AGENT & BUILDER (undocumented — from demo code)
    # ==================================================================

    def approve_agent(
        self,
        agent_name: str,
        agent_address: str,
        expired: int,
        can_spot: bool = False,
        can_perp: bool = True,
        can_withdraw: bool = False,
        ip_whitelist: str = "",
    ) -> dict:
        """Approve a new API agent. Requires main_private_key."""
        return self._signed_post(
            "/fapi/v3/approveAgent",
            {
                "agentName": agent_name,
                "agentAddress": agent_address,
                "ipWhitelist": ip_whitelist,
                "expired": expired,
                "canSpotTrade": can_spot,
                "canPerpTrade": can_perp,
                "canWithdraw": can_withdraw,
            },
            primary_type="ApproveAgent",
            use_main_key=True,
        )

    def update_agent(
        self,
        agent_address: str,
        can_spot: bool = False,
        can_perp: bool = True,
        can_withdraw: bool = False,
        ip_whitelist: str = "",
    ) -> dict:
        """Update agent permissions. Requires main_private_key."""
        return self._signed_post(
            "/fapi/v3/updateAgent",
            {
                "agentAddress": agent_address,
                "ipWhitelist": ip_whitelist,
                "canSpotTrade": can_spot,
                "canPerpTrade": can_perp,
                "canWithdraw": can_withdraw,
            },
            primary_type="UpdateAgent",
            use_main_key=True,
        )

    def get_agents(self) -> list:
        """List all agents."""
        return self._signed_get("/fapi/v3/agent")

    def delete_agent(self, agent_address: str) -> dict:
        """Delete an agent. Requires main_private_key."""
        return self._signed_delete(
            "/fapi/v3/agent",
            {"agentAddress": agent_address},
            primary_type="DelAgent",
            use_main_key=True,
        )

    def approve_builder(self, builder_address: str, max_fee_rate: str, builder_name: str) -> dict:
        """Approve a builder address. Requires main_private_key."""
        return self._signed_post(
            "/fapi/v3/approveBuilder",
            {
                "builder": builder_address,
                "maxFeeRate": max_fee_rate,
                "builderName": builder_name,
            },
            primary_type="ApproveBuilder",
            use_main_key=True,
        )

    def get_builders(self) -> list:
        """List all builders."""
        return self._signed_get("/fapi/v3/builder")

    def delete_builder(self, builder_address: str) -> dict:
        """Delete a builder. Requires main_private_key."""
        return self._signed_delete(
            "/fapi/v3/builder",
            {"builder": builder_address},
            primary_type="DelBuilder",
            use_main_key=True,
        )

    # ==================================================================
    # MMP (Market Maker Protection)
    # ==================================================================

    def update_mmp(self, symbol: str, **kwargs) -> dict:
        """Update MMP configuration."""
        params = {"symbol": symbol, **kwargs}
        return self._signed_post("/fapi/v3/mmp", params)

    def get_mmp(self, symbol: str) -> dict:
        """Get MMP configuration."""
        return self._signed_get("/fapi/v3/mmp", {"symbol": symbol})

    def delete_mmp(self, symbol: str) -> dict:
        """Delete MMP configuration."""
        return self._signed_delete("/fapi/v3/mmp", {"symbol": symbol})

    def reset_mmp(self, symbol: str) -> dict:
        """Reset MMP state."""
        return self._signed_post("/fapi/v3/mmpReset", {"symbol": symbol})

    # ==================================================================
    # USER DATA STREAM
    # ==================================================================

    def start_user_stream(self) -> dict:
        """Start a user data stream (returns listenKey)."""
        return self._request("POST", "/fapi/v3/listenKey")

    def keepalive_user_stream(self) -> dict:
        """Keepalive user data stream."""
        return self._request("PUT", "/fapi/v3/listenKey")

    def close_user_stream(self) -> dict:
        """Close user data stream."""
        return self._request("DELETE", "/fapi/v3/listenKey")
