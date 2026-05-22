# Aster-Chain API Overview

* This document lists the base URL for the API endpoints: **https://chainapi.asterdex.com**
* All API responses are in JSON format.

---

- [Aster-Chain Account Endpoints](#aster-chain-account-endpoints)
  - [Get Account Status (USER_DATA)](#get-account-status-user_data)
  - [Modify Account Status (TRADE)](#modify-account-status-trade)
  - [Transfer to Address (WITHDRAW)](#transfer-to-address-withdraw)

---

# Aster-Chain Account Endpoints

## Get Account Status (USER_DATA)

> **Response:**

```javascript
{
    "status": "PRIVATE" // "PUBLIC" or "PRIVATE"
}
```

`GET /aster-chain/v3/account/status`

Get the current account's privacy status.

**Weight:** 1

**Parameters:**

None

---

## Modify Account Status (TRADE)

> **Response:**

```javascript
{
    "status": "PRIVATE" // "PUBLIC" or "PRIVATE"
}
```

`POST /aster-chain/v3/account/modify-status`

Modify the account's privacy status. After a successful update, the change is broadcast to the Aster Chain.

**Weight:** 5

**Parameters:**

| Name | Type | Mandatory | Description |
|------|------|-----------|-------------|
| status | STRING | YES | Account privacy mode: `"PUBLIC"` or `"PRIVATE"` |

---

## Transfer to Address (WITHDRAW)

> **Response:**

```javascript
{
    "transferId": "123456789",
    "asset": "USDT",
    "amount": "10.00",
    "toAddress": "0xAbCd1234...",
    "timestamp": 1699900800000,
    "status": "SUCCESS"  // "SUCCESS" or "PENDING"
}
```

`POST /aster-chain/v3/transfer`

Transfer assets to another Aster Chain address. The recipient address must belong to a registered Aster Chain user.

**Weight:** 50

**Parameters:**

| Name | Type | Mandatory | Description |
|------|------|-----------|-------------|
| asset | STRING | YES | Asset name to transfer (e.g. `"USDT"`) |
| amount | DECIMAL | YES | Transfer amount, must be greater than 0 |
| toAddress | STRING | YES | Recipient's Aster Chain wallet address |
| clientTranId | STRING | NO | Client-defined transfer ID; auto-generated if not provided |
| nonce | LONG | YES | Microsecond timestamp |
| user | STRING | YES | Source account wallet address |
| signature | STRING | YES | EIP-712 signature, signed with the `user` account's wallet private key |
