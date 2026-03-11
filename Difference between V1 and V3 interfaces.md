# Aster API V1 vs V3

This page provides a quick comparison between Aster `V1` and `V3`, focusing on authentication, endpoint structure, capability coverage, and the most important architectural value behind V3.

> **Key takeaways**
>
> 1. Authentication moves from `API Key + HMAC` to `API Wallet / Agent + Web3-style signing`
> 2. The futures structure is upgraded on top of `Aster L1`, giving `V3` stronger `Take Order` performance while consolidating the main paths into `/fapi/v3/*`

---

## Overview

### How To Understand It

- `V1` is the standard API Key model.
- `V3` introduces the API Wallet / Agent model, and its authentication flow is closer to on-chain signing.
- `V3` futures are built on top of `Aster L1`, which gives stronger `Take Order` performance.
- `V3` goes through the blockchain, which makes historical trades traceable in the future, with stronger security and visibility.
- `V3` uses `nonce` to prevent replay attacks, making requests more secure.
- `V3` supports `Noop`, which can cancel orders faster.
- Most business capabilities still exist in both versions.
- The biggest change is not order semantics, but the authentication layer.

---

## Authentication

### V1

In `V1`, authentication follows the typical `API Key + Secret` model:

- Send `X-MBX-APIKEY` in the request header
- Include `timestamp` in request parameters
- Optionally include `recvWindow`
- Generate `signature` using `HMAC SHA256`

The signing payload is usually based on request parameters, which means `query string + request body`.

### V3

In `V3`, authentication is no longer centered only around `apiSecret`.

In addition to business parameters, requests also include:

- `user`: main account wallet address
- `signer`: API wallet address
- `nonce`: microsecond timestamp
- `signature`: signed by the API wallet private key
- `timestamp`

The signing flow can be understood as:

1. Convert all business parameters into strings
2. Sort them by ASCII key order
3. Encode them together with `user`, `signer`, and `nonce`
4. Generate a Keccak hash
5. Sign it with ECDSA using the API wallet private key

`nonce` also plays an important role in V3, because it prevents replay attacks and makes requests more secure.

> **Why this matters**
>
> `V1` is well suited to the standard API Key integration model.
> `V3` is built around signer identity and is better aligned with the Aster L1 architecture.

### Core Value Of V3

- `V3` futures are built on top of `Aster L1`, giving stronger `Take Order` performance.
- `V3` goes through the blockchain, so historical trades can be traced in the future, with stronger security and visibility.
- `V3` uses `nonce` to prevent replay and make requests more secure.
- `V3` supports `Noop`, which can cancel orders faster.

## Migration Notes

A practical migration order is:

1. Build a dedicated signing module first
2. Centralize the authentication context:
   - `user`
   - `signer`
   - `signerPrivateKey`
   - `timestamp`
   - `nonce`
3. Get one simple order or query flow working first
4. Validate the signing logic with a simple trade flow
5. Then move to batch and fund-related operations

### Common Mistakes

The most common issues during V3 migration are:

- incorrect parameter sorting
- mixing milliseconds and microseconds
- forgetting `user` or `signer`
- assuming V3 is still plain HMAC
- relying too much on endpoint titles instead of the authentication section

---

- `V1` is fundamentally the standard `API Key` model.
- `V3` introduces the `API Wallet / Agent` model, and its authentication flow is closer to on-chain signing.
- The two versions remain broadly aligned in business capability, with the main difference concentrated in the authentication layer.
- On futures, `V3` is built on top of `Aster L1`, which gives it stronger `Take Order` performance and a more unified endpoint structure.
- `V3` goes through the blockchain, making future historical trade traceability possible with stronger security and visibility.
- `V3` uses `nonce` to prevent replay and improve request security.
- `V3` supports `Noop`, which can cancel orders faster.
- Fund-related APIs still require extra attention because they often involve additional wallet-based signing.
