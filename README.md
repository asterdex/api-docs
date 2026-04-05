# AsterDex API Documentation — Community Enhanced

[![Docs Lint](https://img.shields.io/badge/docs-lint%20passing-brightgreen)](#)
[![SDK Python](https://img.shields.io/badge/SDK-Python%203.9+-blue)](#python-sdk)
[![SDK JavaScript](https://img.shields.io/badge/SDK-Node%2018+-yellow)](#javascript-sdk)
[![License](https://img.shields.io/badge/license-MIT-green)](#license)

> Community-maintained fork with structured navigation, missing endpoint documentation, SDK wrappers, and code examples. Maintained by [Kairos Lab](https://github.com/Valisthea).

---

## Quick Start

| I want to... | Go here |
|---|---|
| **Trade futures (V3)** | [Futures API V3](./docs/aster-finance-futures-api-v3.md) |
| **Trade spot (V3)** | [Spot API V3](./docs/aster-finance-spot-api-v3.md) |
| **Understand V1 → V3 migration** | [V1 vs V3 Comparison](./docs/Difference%20between%20V1%20and%20V3%20interfaces.md) |
| **Use the Python SDK** | [SDK / Python](./sdk/python/) |
| **Use the JavaScript SDK** | [SDK / JavaScript](./sdk/javascript/) |
| **Manage API keys & agents** | [API Key Registration](./docs/aster-api-key-registration.md) |
| **Deposit / Withdraw** | [Deposit & Withdrawal](./docs/aster-deposit-withdrawal.md) |
| **Use Aster Chain RPC** | [Chain RPC](./docs/aster-chain-rpc.md) |
| **Test on testnet** | [Futures Testnet](./docs/aster-finance-futures-api-testnet.md) · [Spot Testnet](./docs/aster-finance-spot-api-testnet.md) |

---

## Futures V3 — Endpoint Index

### Public Endpoints (no auth required)

| Endpoint | Method | Description |
|---|---|---|
| `/fapi/v3/ping` | GET | Test connectivity |
| `/fapi/v3/time` | GET | Server time |
| `/fapi/v3/exchangeInfo` | GET | Exchange rules, symbols, filters |
| `/fapi/v3/depth` | GET | Order book |
| `/fapi/v3/trades` | GET | Recent trades |
| `/fapi/v3/historicalTrades` | GET | Old trades (MARKET_DATA) |
| `/fapi/v3/aggTrades` | GET | Compressed/aggregate trades |
| `/fapi/v3/klines` | GET | Kline/candlestick data |
| `/fapi/v3/indexPriceKlines` | GET | Index price klines |
| `/fapi/v3/markPriceKlines` | GET | Mark price klines |
| `/fapi/v3/premiumIndex` | GET | Mark price & funding rate |
| `/fapi/v3/fundingRate` | GET | Funding rate history |
| `/fapi/v3/fundingInfo` | GET | Funding rate config |
| `/fapi/v3/ticker/24hr` | GET | 24hr ticker statistics |
| `/fapi/v3/ticker/price` | GET | Symbol price ticker |
| `/fapi/v3/ticker/bookTicker` | GET | Best bid/ask price |
| `/fapi/v3/indexreferences` | GET | Index price references |
| `/fapi/v3/openInterest` | GET | Open interest (**undocumented — see [Community Notes](./docs/community-notes.md)**) |

### Trading Endpoints (TRADE — signature required)

| Endpoint | Method | Description |
|---|---|---|
| `/fapi/v3/order` | POST | New order |
| `/fapi/v3/order` | GET | Query order |
| `/fapi/v3/order` | DELETE | Cancel order |
| `/fapi/v3/batchOrders` | POST | Place multiple orders |
| `/fapi/v3/batchOrders` | DELETE | Cancel multiple orders |
| `/fapi/v3/allOpenOrders` | DELETE | Cancel all open orders |
| `/fapi/v3/countdownCancelAll` | POST | Auto-cancel countdown |
| `/fapi/v3/noop` | POST | Noop (fast cancel trigger) |

### Account Endpoints (USER_DATA — signature required)

| Endpoint | Method | Description |
|---|---|---|
| `/fapi/v3/openOrder` | GET | Current open order |
| `/fapi/v3/openOrders` | GET | All open orders |
| `/fapi/v3/allOrders` | GET | All orders (incl. filled) |
| `/fapi/v3/balance` | GET | Futures account balance |
| `/fapi/v3/accountWithJoinMargin` | GET | Account info with margin |
| `/fapi/v3/positionRisk` | GET | Position information |
| `/fapi/v3/userTrades` | GET | Account trade list |
| `/fapi/v3/income` | GET | Income history |
| `/fapi/v3/leverageBracket` | GET | Notional & leverage brackets |
| `/fapi/v3/adlQuantile` | GET | ADL quantile estimation |
| `/fapi/v3/forceOrders` | GET | Force orders (liquidations) |
| `/fapi/v3/commissionRate` | GET | User commission rate |

### Position & Margin Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/fapi/v3/leverage` | POST | Change initial leverage |
| `/fapi/v3/marginType` | POST | Change margin type |
| `/fapi/v3/positionMargin` | POST | Modify isolated position margin |
| `/fapi/v3/positionMargin/history` | GET | Position margin change history |
| `/fapi/v3/positionSide/dual` | POST | Change position mode |
| `/fapi/v3/positionSide/dual` | GET | Get current position mode |
| `/fapi/v3/multiAssetsMargin` | POST | Change multi-assets mode |
| `/fapi/v3/multiAssetsMargin` | GET | Get multi-assets mode |

### Agent & Builder Endpoints (undocumented in official — extracted from demos)

| Endpoint | Method | Description |
|---|---|---|
| `/fapi/v3/approveAgent` | POST | Approve an API agent (EIP-712 signed) |
| `/fapi/v3/updateAgent` | POST | Update agent permissions/IP whitelist |
| `/fapi/v3/agent` | GET | List agents |
| `/fapi/v3/agent` | DELETE | Delete agent |
| `/fapi/v3/approveBuilder` | POST | Approve a builder address |
| `/fapi/v3/updateBuilder` | POST | Update builder fee rate |
| `/fapi/v3/builder` | DELETE | Delete builder |
| `/fapi/v3/builder` | GET | List builders |

### Market Maker Protection (MMP)

| Endpoint | Method | Description |
|---|---|---|
| `/fapi/v3/mmp` | POST | Update MMP config |
| `/fapi/v3/mmp` | GET | Get MMP config |
| `/fapi/v3/mmp` | DELETE | Delete MMP config |
| `/fapi/v3/mmpReset` | POST | Reset MMP state |

### User Data Stream

| Endpoint | Method | Description |
|---|---|---|
| `/fapi/v3/listenKey` | POST | Start user data stream |
| `/fapi/v3/listenKey` | PUT | Keepalive |
| `/fapi/v3/listenKey` | DELETE | Close stream |

### Transfer

| Endpoint | Method | Description |
|---|---|---|
| `/fapi/v3/asset/wallet/transfer` | POST | Transfer between futures & spot |

---

## WebSocket Streams

| Stream | Description |
|---|---|
| `<symbol>@aggTrade` | Aggregate trade |
| `<symbol>@markPrice` / `@markPrice@1s` | Mark price |
| `!markPrice@arr` / `!markPrice@arr@1s` | All market mark prices |
| `<symbol>@kline_<interval>` | Kline/candlestick |
| `<symbol>@miniTicker` | Individual mini ticker |
| `!miniTicker@arr` | All market mini tickers |
| `<symbol>@ticker` | Individual ticker |
| `!ticker@arr` | All market tickers |
| `<symbol>@bookTicker` | Individual book ticker |
| `!bookTicker` | All book tickers |
| `<symbol>@forceOrder` | Individual liquidation |
| `!forceOrder@arr` | All market liquidations |
| `<symbol>@depth<levels>` / `@depth<levels>@<speed>` | Partial book depth |
| `<symbol>@depth` / `@depth@<speed>` | Diff book depth |

Base URL: `wss://fstream.asterdex.com/ws/<listenKey>`

---

## SDK

### Python SDK

```bash
pip install asterdex-sdk  # coming soon — use local install for now
```

```python
from asterdex import AsterDexClient

client = AsterDexClient(
    user="0x...",
    signer="0x...",
    private_key="0x..."
)

# Place a market order
order = client.place_order(
    symbol="BTCUSDT",
    side="BUY",
    order_type="MARKET",
    quantity="0.01"
)

# Get leverage brackets (the endpoint Mouss was looking for)
brackets = client.get_leverage_brackets(symbol="ETHUSDT")
```

→ [Full Python SDK docs](./sdk/python/README.md)

### JavaScript SDK

```bash
npm install @kairoslab/asterdex-sdk  # coming soon
```

```javascript
import { AsterDexClient } from '@kairoslab/asterdex-sdk';

const client = new AsterDexClient({
  user: '0x...',
  signer: '0x...',
  privateKey: '0x...'
});

const order = await client.placeOrder({
  symbol: 'BTCUSDT',
  side: 'BUY',
  type: 'MARKET',
  quantity: '0.01'
});
```

→ [Full JavaScript SDK docs](./sdk/javascript/README.md)

---

## Community Notes

Known gaps and workarounds documented by the community:

- **`/fapi/v3/openInterest`** — Returns one-sided OI in base-asset units. To match the UI: `OI_USDT ≈ openInterest × 2 × price`. [Details](./docs/community-notes.md#open-interest)
- **Rebalance** — No API endpoint exists. Must be done via UI. [Details](./docs/community-notes.md#rebalance)
- **Builder per-wallet fee tracking** — Not yet available via API. Only aggregated daily fees in Builder Center. [Details](./docs/community-notes.md#builder-fees)
- **Referral endpoints** (`/bapi/futures/v2/private/...`) — Currently private, not exposed via public API. [Details](./docs/community-notes.md#referral-endpoints)

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## Security

Found a security issue? See [SECURITY.md](./SECURITY.md).

## License

This community fork is licensed under [MIT](./LICENSE). Original AsterDex documentation is © AsterDex.
