# AsterDex Python SDK

Community Python SDK for the AsterDex V3 API, maintained by [Kairos Lab](https://github.com/Valisthea).

## Installation

```bash
pip install asterdex-sdk
```

Or install from source:

```bash
git clone https://github.com/Valisthea/aster-api-docs.git
cd aster-api-docs/sdk/python
pip install -e .
```

## Quick Start

```python
from asterdex import AsterDexClient

# Public endpoints — no auth needed
client = AsterDexClient()
print(client.get_ticker_price(symbol="BTCUSDT"))

# Authenticated endpoints
client = AsterDexClient(
    user="0xYourMainWallet",
    signer="0xYourAgentWallet",
    private_key="0xYourAgentPrivateKey",
)

# Place a market buy
order = client.place_order(
    symbol="BTCUSDT",
    side="BUY",
    order_type="MARKET",
    quantity="0.01",
)
print(order)

# Get leverage brackets
brackets = client.get_leverage_brackets(symbol="ETHUSDT")
for tier in brackets["brackets"]:
    print(f"  Tier {tier['bracket']}: {tier['initialLeverage']}x up to {tier['notionalCap']} USDT")

# Get open interest (undocumented endpoint)
oi = client.get_open_interest(symbol="BTCUSDT")
mark = client.get_mark_price(symbol="BTCUSDT")
oi_usdt = float(oi["openInterest"]) * 2 * float(mark["markPrice"])
print(f"OI (UI-equivalent): ${oi_usdt:,.0f}")
```

## Agent & Builder Management

These operations require `main_private_key` (your main wallet key):

```python
client = AsterDexClient(
    user="0xYourMainWallet",
    signer="0xYourAgentWallet",
    private_key="0xAgentKey",
    main_private_key="0xMainWalletKey",  # needed for agent ops
)

# Create a new agent
client.approve_agent(
    agent_name="my-bot",
    agent_address="0xNewAgentAddress",
    expired=1967945395040,
    can_perp=True,
    can_spot=False,
    can_withdraw=False,
    ip_whitelist="1.2.3.4",
)

# List agents
agents = client.get_agents()
```

## Error Handling

```python
from asterdex import AsterDexClient, AsterDexError, AsterDexRateLimitError

client = AsterDexClient(...)

try:
    order = client.place_order(...)
except AsterDexRateLimitError:
    print("Rate limited — back off")
except AsterDexError as e:
    print(f"API error [{e.code}]: {e.message}")
```

## Testnet

```python
from asterdex.client import AsterDexClient, TESTNET_BASE, CHAIN_ID_TESTNET

client = AsterDexClient(
    base_url=TESTNET_BASE,
    chain_id=CHAIN_ID_TESTNET,
    user="0x...",
    signer="0x...",
    private_key="0x...",
)
```

## License

MIT — Kairos Lab
