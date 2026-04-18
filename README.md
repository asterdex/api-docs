# Aster API Documentation

Official API documentation for [AsterDEX](https://www.asterdex.com) — Futures, Spot, and Aster Chain.

## Quick start

### 1. Choose your API version

| Version | Auth method | Status | Best for |
|---------|------------|--------|----------|
| **V3 (recommended)** | EIP-712 signature | Active | New integrations |
| V1 | HMAC SHA-256 | Deprecated (existing keys still work) | Legacy bots |

> Since March 25, 2026, new V1 API keys can no longer be created. Use V3 for all new projects.

### 2. Create your API wallet (V3)

1. Go to [asterdex.com/en/api-wallet](https://www.asterdex.com/en/api-wallet)
2. Connect your main wallet (MetaMask)
3. Click **"Authorize new API wallet"**
4. Sign the transaction
5. **Save both values immediately** — the private key is shown only once

You now have 3 values needed for all V3 requests:

| Value | What it is | Where to find it |
|-------|-----------|-----------------|
| `user` | Your main wallet address | MetaMask — the wallet you deposited with |
| `signer` | Agent/API wallet address | Shown after creation at [/api-wallet](https://www.asterdex.com/en/api-wallet) |
| `private_key` | Agent wallet's private key | Shown **once** at creation — save it immediately |

> **Note:** A wallet named `@aster-desktop` also appears on the page. This is the internal agent used by the AsterDEX web UI — ignore it for API purposes.

### 3. Sign your first request

V3 uses EIP-712 typed data signatures. The signing flow:

1. Build a `msg` string from your request parameters (strict key ordering for trade endpoints)
2. Hash it with the EIP-712 domain `{name: "AsterSignTransaction", version: "1", chainId: 1666}`
3. Sign the hash with your **agent private key** (not your main wallet key)
4. Include `user`, `signer`, `nonce` (microseconds), and `signature` (0x-prefixed) in the request body

See working example: [Python demo](demo/aster-code.py)

### 4. Common signature errors

If you get `{"code": -1000, "msg": "Signature check failed"}`:

| Check | Fix |
|-------|-----|
| Wrong key | Sign with the **agent** private key, not your main wallet key |
| Signer mismatch | The `signer` field must match the address derived from your private key |
| Agent not approved | Verify agent is listed and active at [/api-wallet](https://www.asterdex.com/en/api-wallet) |
| Clock drift | Nonce must be within 10 seconds of server time (microsecond precision) |
| Param ordering | Trade endpoints use strict key order: `symbol, side, type, quantity, price, timeInForce, leverage, orderId` |

---

## API documentation

### Overview

- [Aster API Overview](./Aster%20API%20Overview.md)

### Futures

| Document | Language |
|----------|----------|
| [Futures API V3](V3(Recommended)/EN/aster-finance-futures-api-v3.md) | English |
| [Futures API V3 文档](V3(Recommended)/中文/aster-finance-futures-api-v3_CN.md) | 中文 |
| [Futures Testnet API V3](V3(Recommended)/EN/aster-finance-futures-api-testnet.md) | English |
| [Futures Testnet API V3 文档](V3(Recommended)/中文/aster-finance-futures-api-testnet_CN.md) | 中文 |
| [Futures API V1](V1(Legacy)/EN/aster-finance-futures-api.md) | English |
| [Futures API V1 文档](V1(Legacy)/中文/aster-finance-futures-api_CN.md) | 中文 |

### Spot

| Document | Language |
|----------|----------|
| [Spot API V3](V3(Recommended)/EN/aster-finance-spot-api-v3.md) | English |
| [Spot API V3 文档](V3(Recommended)/中文/aster-finance-spot-api_CN-v3.md) | 中文 |
| [Spot Testnet API V3](V3(Recommended)/EN/aster-finance-spot-api-testnet.md) | English |
| [Spot Testnet API V3 文档](V3(Recommended)/中文/aster-finance-spot-api-testnet_CN.md) | 中文 |
| [Spot API V1](V1(Legacy)/EN/aster-finance-spot-api.md) | English |
| [Spot API V1 文档](V1(Legacy)/中文/aster-finance-spot-api_CN.md) | 中文 |

### RPC

| Document | Language |
|----------|----------|
| [Aster Chain RPC](RPC/aster-chain-rpc.md) | English |
| [Aster Chain RPC 文档](RPC/aster-chain-rpc_CN.md) | 中文 |

### Account & operations

| Document | Description |
|----------|-------------|
| [API key registration](demo/aster-api-key-registration.md) | How to create API keys |
| [Deposit & withdrawal](demo/aster-deposit-withdrawal.md) | Deposit and withdrawal guide |
| [Spot asset consolidation](demo/consolidation.js) | Asset consolidation script example |

---

## Code examples

### Official demos

| Language | File | Description |
|----------|------|-------------|
| Python | [demo/aster-code.py](demo/aster-code.py) | V3 EIP-712 signing — Futures |
| Python | [demo/sol_agent.py](demo/sol_agent.py) | Solana wallet agent demo |
| JavaScript | [demo/consolidation.js](demo/consolidation.js) | Spot asset consolidation |
| JavaScript | [demo/create-apikey-for-others.js](demo/create-apikey-for-others.js) | Create API keys for sub-accounts |

### Official tools

| Tool | Description | Link |
|------|-------------|------|
| aster-connector-python | Lightweight Python connector | [github.com/asterdex/aster-connector-python](https://github.com/asterdex/aster-connector-python) |
| aster-mcp | MCP server for Cursor/Claude | [github.com/asterdex/aster-mcp](https://github.com/asterdex/aster-mcp) |
| aster-skills-hub | Agent skills for OpenClaw | [github.com/asterdex/aster-skills-hub](https://github.com/asterdex/aster-skills-hub) |

### Community tools

| Tool | Description | Link |
|------|-------------|------|
| kairos-aster-sdk | Full Python SDK — Futures, Spot & WebSocket V3 with EIP-712 abstraction | [github.com/Valisthea/kairos-aster-sdk-V3](https://github.com/Valisthea/kairos-aster-sdk-V3) |

---

## API endpoints

| API | REST base URL | WebSocket |
|-----|--------------|-----------|
| Futures V3 | `https://fapi.asterdex.com/fapi/v3/` | `wss://fstream.asterdex.com` |
| Futures V1 | `https://fapi.asterdex.com/fapi/v1/` | `wss://fstream.asterdex.com` |
| Spot | `https://sapi.asterdex.com` | `wss://sstream.asterdex.com` |
| Futures testnet | `https://fapi.asterdex-testnet.com/fapi/v3/` | `wss://fstream.asterdex-testnet.com` |
| Spot testnet | `https://sapi.asterdex-testnet.com` | `wss://sstream.asterdex-testnet.com` |

---

## Additional resources

- [API website with full endpoint docs](https://asterdex.github.io/aster-api-website/futures-v3/general-info/)
- [Aster Code (builder integration)](https://asterdex.github.io/aster-api-website/asterCode/integration-flow/)
- [Error codes reference](https://asterdex.github.io/aster-api-website/futures-v3/error-codes/)
- [Official docs](https://docs.asterdex.com/for-developers/aster-api)
- [API wallet management](https://www.asterdex.com/en/api-wallet)
