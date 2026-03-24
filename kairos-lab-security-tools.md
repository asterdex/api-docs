# Kairos Lab Security Tools

Third-party security layer for AsterDex V3 API — adds rate limiting, circuit breaking, anomaly detection, and on-chain audit trails to your trading infrastructure.

## `@kairosauth/shield`

Enterprise-grade API protection SDK by [Kairos Lab](https://kairosauth.io). Wraps your AsterDex V3 calls in 4 protection layers before they reach the exchange.

### What it solves

| Problem | Without Shield | With Shield |
|---------|---------------|-------------|
| Rate limit exceeded | 429 → possible IP ban (418) | Shield throttles you before AsterDex does |
| Exchange downtime | Bot hangs on timeouts | Circuit breaker fails fast, auto-retries |
| API key leaked | Attacker executes trades | Anomaly detector blocks unusual patterns |
| Incident forensics | No evidence | On-chain Merkle audit trail of every event |

### Quick Start

```bash
npm install @kairosauth/shield
```

```ts
import { AsterDexShield } from "@kairosauth/shield/adapters/asterdex";

const shield = AsterDexShield.create();

// Before every API call
const check = await shield.protect({
  apiKey: process.env.ASTER_API_KEY,
  endpoint: "/fapi/v3/order",
  method: "POST",
  bodySize: body.length,
});

if (!check.allowed) {
  console.warn(`Blocked: ${check.reason}`);
  return;
}

// Make your AsterDex call normally...
const res = await fetch("https://fapi.asterdex.com/fapi/v3/order", options);

// Report response status to circuit breaker
shield.reportResponse("/fapi/v3/order", res.status);
```

### Pre-configured for AsterDex V3

The `AsterDexShield` adapter comes with limits tuned to AsterDex's documented rate limits:

| Endpoint | Shield Limit | AsterDex Limit | Safety Margin |
|----------|-------------|----------------|---------------|
| `/fapi/v3/order` | 60/min | 1200/min (ORDERS) | 95% headroom |
| `/fapi/v3/batchOrders` | 20/min | — | Conservative |
| Market data | 600/min | 2400/min (WEIGHT) | 75% headroom |
| API key creation | 5/5min | — | Hardened |

All limits are configurable — override anything in the constructor.

### Features

- **Rate Shield** — Sliding window rate limiting, per-endpoint granularity, early warning at 80% usage
- **Circuit Breaker** — CLOSED → OPEN → HALF_OPEN state machine, automatic recovery testing
- **Anomaly Detector** — Payload size limits, endpoint scanning detection, burst spike detection, custom rules
- **On-Chain Audit** — Merkle-tree anchored event log via Kairos Lab infrastructure (optional)
- **Zero overhead** — < 0.1ms evaluation time, fully in-memory, async audit flushing
- **TypeScript** — Full type definitions, CJS + ESM builds

### Links

- **GitHub:** [github.com/Valisthea/kairosauth-shield](https://github.com/Valisthea/kairosauth-shield)
- **Full Examples:** [examples/](https://github.com/Valisthea/kairosauth-shield/tree/main/examples)
- **Kairos Lab:** [kairosauth.io](https://kairosauth.io)
