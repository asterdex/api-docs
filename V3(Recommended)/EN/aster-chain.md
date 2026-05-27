# Aster-Chain API Overview

* This document lists the base URL for the API endpoints: **https://chainapi.asterdex.com**
* All API responses are in JSON format.

---

- [Aster-Chain Account Endpoints](#aster-chain-account-endpoints)
  - [Get Account Status (USER_DATA)](#get-account-status-user_data)
  - [Modify Account Status (TRADE)](#modify-account-status-trade)
  - [Transfer to Address (WITHDRAW)](#transfer-to-address-withdraw)
- [Aster-Chain Staking Endpoints](#aster-chain-staking-endpoints)
  - [Get Staking Account Status (USER_DATA)](#get-staking-account-status-user_data)
  - [Get My Staking (USER_DATA)](#get-my-staking-user_data)
  - [Get Claimable Rewards (USER_DATA)](#get-claimable-rewards-user_data)
  - [Create Staking (TRADE)](#create-staking-trade)
  - [Deposit Stake (TRADE)](#deposit-stake-trade)
  - [Update Lock Period (TRADE)](#update-lock-period-trade)
  - [Claim Rewards (TRADE)](#claim-rewards-trade)

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

---

# Aster-Chain Staking Endpoints

## Get Staking Account Status (USER_DATA)

> **Response:**

```javascript
{
    "stakeAccountStatus": "ACTIVE"  // "ACTIVE", "INACTIVE", or "PENDING"
}
```

`GET /aster-chain/v3/staking/stakeAccountStatus`

Query the staking account status of the current user.

**Weight:** 1

**Parameters:**

| Name | Type | Mandatory | Description |
|------|------|-----------|-------------|
| nonce | LONG | YES | Microsecond timestamp |
| signer | STRING | YES | Agent wallet address (sub-wallet authorized to sign on behalf of the account) |
| signature | STRING | YES | EIP-712 signature, signed with the `signer` wallet private key |

---

## Get My Staking (USER_DATA)

> **Response:**

```javascript
{
    "validatorAddress": "0x1a2b3c4d...",
    "stakeAmount": "1000.00",
    "periodCode": "90D",
    "startTime": 1699900800000,
    "endTime": 1707676800000,
    "status": "ACTIVE"  // "ACTIVE", "UNLOCKING", or "COMPLETED"
}
```

`GET /aster-chain/v3/staking/myStaking`

Query the current user's staking position details.

**Weight:** 1

**Parameters:**

| Name | Type | Mandatory | Description |
|------|------|-----------|-------------|
| nonce | LONG | YES | Microsecond timestamp |
| signer | STRING | YES | Agent wallet address (sub-wallet authorized to sign on behalf of the account) |
| signature | STRING | YES | EIP-712 signature, signed with the `signer` wallet private key |

---

## Get Claimable Rewards (USER_DATA)

> **Response:**

```javascript
{
    "claimableAmount": "12.50",
    "asset": "ASTER",
    "accruedRewards": "25.00",
    "lastClaimTime": 1699900800000
}
```

`GET /aster-chain/v3/staking/claimableRewards`

Query the amount of staking rewards available to claim for the current user.

**Weight:** 1

**Parameters:**

| Name | Type | Mandatory | Description |
|------|------|-----------|-------------|
| nonce | LONG | YES | Microsecond timestamp |
| signer | STRING | YES | Agent wallet address (sub-wallet authorized to sign on behalf of the account) |
| signature | STRING | YES | EIP-712 signature, signed with the `signer` wallet private key |

---

## Create Staking (TRADE)

> **Response:**

```javascript
{
    "result": "SUCCESS"
}
```

`POST /aster-chain/v3/staking/create`

Create a new staking position by delegating tokens to a validator. The on-chain action type is `TokenDelegate` (`Stake`).

**Weight:** 5

**Parameters:**

| Name | Type | Mandatory | Description |
|------|------|-----------|-------------|
| validatorAddress | STRING | YES | Target validator's on-chain address |
| stakeAmount | DECIMAL | YES | Amount of tokens to stake, must be greater than 0 |
| periodCode | STRING | YES | Lock period code. Allowed values: `"26_WEEKS"`, `"52_WEEKS"`, `"104_WEEKS"`, `"156_WEEKS"`, `"208_WEEKS"` |
| nonce | LONG | YES | Microsecond timestamp |
| user | STRING | YES | Source account wallet address |
| signature | STRING | YES | EIP-712 signature, signed with the `user` account's wallet private key |

---

## Deposit Stake (TRADE)

> **Response:**

```javascript
{
    "result": "SUCCESS"
}
```

`POST /aster-chain/v3/staking/deposit`

Add tokens to an existing staking position on the specified validator. The on-chain action type is `TokenDelegate` (`AddStake`).

**Weight:** 5

**Parameters:**

| Name | Type | Mandatory | Description |
|------|------|-----------|-------------|
| validatorAddress | STRING | YES | Target validator's on-chain address |
| stakeAmount | DECIMAL | YES | Amount of additional tokens to stake, must be greater than 0 |
| nonce | LONG | YES | Microsecond timestamp |
| user | STRING | YES | Source account wallet address |
| signature | STRING | YES | EIP-712 signature, signed with the `user` account's wallet private key |

---

## Update Lock Period (TRADE)

> **Response:**

```javascript
{
    "result": "SUCCESS"
}
```

`POST /aster-chain/v3/staking/updateLockPeriod`

Extend the lock period of the current staking position. The on-chain action type is `TokenDelegate` (`ExtendStakingTime`).

**Weight:** 5

**Parameters:**

| Name | Type | Mandatory | Description |
|------|------|-----------|-------------|
| periodCode | STRING | YES | New lock period code. Allowed values: `"26_WEEKS"`, `"52_WEEKS"`, `"104_WEEKS"`, `"156_WEEKS"`, `"208_WEEKS"`. Must be longer than the current lock period. |
| nonce | LONG | YES | Microsecond timestamp |
| user | STRING | YES | Source account wallet address |
| signature | STRING | YES | EIP-712 signature, signed with the `user` account's wallet private key |

---

## Claim Rewards (TRADE)

> **Response:**

```javascript
{
    "result": "SUCCESS"
}
```

`POST /aster-chain/v3/staking/claimRewards`

Claim accumulated staking rewards. The on-chain action type is `TokenDelegate` (`ClaimRewards`).

**Weight:** 5

**Parameters:**

| Name | Type | Mandatory | Description |
|------|------|-----------|-------------|
| requestedAmount | DECIMAL | YES | Amount of rewards to claim, must be greater than 0 and not exceed the claimable balance |
| nonce | LONG | YES | Microsecond timestamp |
| user | STRING | YES | Source account wallet address |
| signature | STRING | YES | EIP-712 signature, signed with the `user` account's wallet private key |
