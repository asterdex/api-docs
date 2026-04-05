# AsterDex JavaScript SDK

Community JavaScript SDK for the AsterDex V3 API, maintained by [Kairos Lab](https://github.com/Valisthea).

## Installation

```bash
npm install @kairoslab/asterdex-sdk
```

## Quick Start

```javascript
import { AsterDexClient } from '@kairoslab/asterdex-sdk';

// Public endpoints — no auth
const client = new AsterDexClient();
const price = await client.getTickerPrice('BTCUSDT');
console.log(price);

// Authenticated
const authClient = new AsterDexClient({
  user: '0xYourMainWallet',
  signer: '0xYourAgentWallet',
  privateKey: '0xYourAgentPrivateKey',
});

const order = await authClient.placeOrder({
  symbol: 'BTCUSDT',
  side: 'BUY',
  type: 'MARKET',
  quantity: '0.01',
});
```

## Error Handling

```javascript
import { AsterDexClient, AsterDexRateLimitError, AsterDexError } from '@kairoslab/asterdex-sdk';

try {
  await client.placeOrder({ ... });
} catch (err) {
  if (err instanceof AsterDexRateLimitError) {
    console.log('Rate limited — backing off');
  } else if (err instanceof AsterDexError) {
    console.log(`API error [${err.code}]: ${err.message}`);
  }
}
```

## Testnet

```javascript
import { AsterDexClient, TESTNET_BASE, CHAIN_ID_TESTNET } from '@kairoslab/asterdex-sdk';

const client = new AsterDexClient({
  baseUrl: TESTNET_BASE,
  chainId: CHAIN_ID_TESTNET,
  user: '0x...',
  signer: '0x...',
  privateKey: '0x...',
});
```

## License

MIT — Kairos Lab
