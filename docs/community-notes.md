# Community Notes — AsterDex API

> Observations, undocumented behaviors, and workarounds collected by the community. These are **not official documentation** — verify against the live API before relying on them in production.

---

## Open Interest

**Endpoint:** `GET /fapi/v3/openInterest`

This endpoint exists and is functional but is **not documented** in the official API docs.

**Parameters:**

| Name | Type | Mandatory | Description |
|---|---|---|---|
| symbol | STRING | YES | e.g., `BTCUSDT` |

**Response:**

```json
{
  "symbol": "BTCUSDT",
  "openInterest": "12345.678",
  "time": 1234567890000
}
```

**Important:** The API returns **one-sided** open interest in base-asset units (e.g., BTC for BTCUSDT). The AsterDex UI shows **both-sides** (long + short) OI displayed in USDT notional.

**To match the UI display:**

```
OI_USDT (UI) ≈ openInterest (API) × 2 × price
```

Use the same price source as the UI (mark price or index price via `GET /fapi/v3/premiumIndex`).

**Weight:** Unknown — assume 1, monitor rate limits.

---

## Rebalance

**Status:** No API endpoint exists for rebalance operations.

Rebalancing (redistributing margin across positions) must be performed through the AsterDex web UI. This has been confirmed by the Aster team as of March 2026.

---

## Builder Fees

**Status:** Per-wallet fee tracking is **not available** via API.

Current limitations:
- Builder Center shows **aggregated daily fees only**
- No endpoint to query fees per individual wallet trading under a builder address
- Feature request has been submitted to the Aster product team (March 2026)

**What you CAN get:**
- Total trade volume per builder via Builder Center UI
- Your own commission rate via `GET /fapi/v3/commissionRate`

**What you CANNOT get via API:**
- Per-wallet trade volume breakdown
- Per-wallet fee breakdown
- Real-time fee accrual per user

---

## Referral Endpoints

The following endpoints are **private** and not accessible via the public API:

- `GET /bapi/futures/v2/private/future/refer/ae/referral-trade-reward`
- `GET /bapi/futures/v2/private/future/refer/ae/referral-summary`

These are used internally by the AsterDex frontend for referral program data. Making them public has been requested but no timeline has been provided.

---

## Agent & Builder Endpoints

These endpoints are functional and present in the official demo code (`demo/aster-code.py`) but are **not documented** in the API reference:

### Approve Agent

```
POST /fapi/v3/approveAgent
```

Creates a new API agent (sub-key) for your account. Uses EIP-712 typed data signing with `primary_type: "ApproveAgent"`.

**Parameters:**

| Name | Type | Mandatory | Description |
|---|---|---|---|
| agentName | STRING | YES | Display name for the agent |
| agentAddress | STRING | YES | Ethereum address of the agent signer |
| ipWhitelist | STRING | NO | Comma-separated IP addresses (empty = no restriction) |
| expired | LONG | YES | Expiration timestamp in milliseconds |
| canSpotTrade | BOOLEAN | YES | Allow spot trading |
| canPerpTrade | BOOLEAN | YES | Allow perpetual futures trading |
| canWithdraw | BOOLEAN | YES | Allow withdrawals |

**Signing:** This endpoint requires `main: true` — it must be signed with the **main account private key**, not the agent key.

### Update Agent

```
POST /fapi/v3/updateAgent
```

Updates permissions and IP whitelist for an existing agent.

**Parameters:**

| Name | Type | Mandatory | Description |
|---|---|---|---|
| agentAddress | STRING | YES | Agent address to update |
| ipWhitelist | STRING | NO | New comma-separated IP list |
| canSpotTrade | BOOLEAN | YES | Updated spot permission |
| canPerpTrade | BOOLEAN | YES | Updated perp permission |
| canWithdraw | BOOLEAN | YES | Updated withdrawal permission |

**Signing:** Requires `main: true`.

### List Agents

```
GET /fapi/v3/agent
```

Returns all agents for the authenticated user. No additional parameters required.

### Delete Agent

```
DELETE /fapi/v3/agent
```

**Parameters:**

| Name | Type | Mandatory | Description |
|---|---|---|---|
| agentAddress | STRING | YES | Agent address to remove |

**Signing:** Requires `main: true`.

### Approve Builder

```
POST /fapi/v3/approveBuilder
```

Registers a builder address for fee sharing.

**Parameters:**

| Name | Type | Mandatory | Description |
|---|---|---|---|
| builder | STRING | YES | Builder Ethereum address |
| maxFeeRate | STRING | YES | Maximum fee rate (e.g., `"0.00001"`) |
| builderName | STRING | YES | Display name for the builder |

**Signing:** Requires `main: true`.

### Update Builder

```
POST /fapi/v3/updateBuilder
```

Updates the fee rate for an existing builder.

**Parameters:**

| Name | Type | Mandatory | Description |
|---|---|---|---|
| builder | STRING | YES | Builder address |
| maxFeeRate | STRING | YES | New fee rate |

**Signing:** Requires `main: true`.

### Delete Builder

```
DELETE /fapi/v3/builder
```

**Parameters:**

| Name | Type | Mandatory | Description |
|---|---|---|---|
| builder | STRING | YES | Builder address to remove |

### List Builders

```
GET /fapi/v3/builder
```

Returns all registered builders for the authenticated user.

---

## Solana Agent Flow

A Solana-based agent authentication flow exists (`fapi3.asterdex.com` base URL), where:
- The `user` field is a Solana public key (base58)
- The `signer` is still an Ethereum address
- Signing uses Ed25519 for the Solana side, ECDSA for the agent side
- Chain ID remains `1666`

This is present in `demo/sol_agent.py` but is **not documented** in the official API reference.

---

## Known Issues

| Issue | Status | Workaround |
|---|---|---|
| API key generation page blank | Intermittent — under maintenance (March 2026) | Wait for fix, use Pro API agent flow instead |
| Pro API signing confusion | Multiple doc links, unclear which is current | Use V3 docs + `demo/aster-code.py` as reference |
| `v3-demo/` folder missing from repo | Broken README link | Demos are in `demo/` folder or `examples/` in this fork |
| TEST* symbols tradeable | Internal testing symbols exposed | Do **not** trade TEST* pairs — no fund recovery guaranteed |

---

*Last updated: April 2026 — contributions welcome via PR.*
