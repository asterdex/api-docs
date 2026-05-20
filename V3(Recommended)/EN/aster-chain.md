# Aster-Chain API Overview

* This document lists the base URL for the API endpoints: **https://chainapi.asterdex.com**
* All API responses are in JSON format.

---

- [Aster-Chain Account Endpoints](#aster-chain-account-endpoints)
  - [Get Account Status (USER_DATA)](#get-account-status-user_data)
  - [Modify Account Status (TRADE)](#modify-account-status-trade)

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
