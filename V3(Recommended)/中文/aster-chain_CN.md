# Aster-Chain API 概览

* 本文档所列接口的 Base URL 为：**https://chainapi.asterdex.com**
* 所有接口响应均为 JSON 格式。

---

- [Aster-Chain 账户接口](#aster-chain-账户接口)
  - [查询账户状态 (USER_DATA)](#查询账户状态-user_data)
  - [修改账户状态 (TRADE)](#修改账户状态-trade)
  - [转账至地址 (WITHDRAW)](#转账至地址-withdraw)
- [Aster-Chain 质押接口](#aster-chain-质押接口)
  - [查询质押账户状态 (USER_DATA)](#查询质押账户状态-user_data)
  - [查询我的质押 (USER_DATA)](#查询我的质押-user_data)
  - [查询可领取奖励 (USER_DATA)](#查询可领取奖励-user_data)
  - [创建质押 (TRADE)](#创建质押-trade)
  - [追加质押 (TRADE)](#追加质押-trade)
  - [更新锁定期 (TRADE)](#更新锁定期-trade)
  - [领取奖励 (TRADE)](#领取奖励-trade)
- [Aster-Chain 合约提现与划转接口](#aster-chain-合约提现与划转接口)
  - [合约提现 (WITHDRAW)](#合约提现-withdraw)
  - [合约 Solana 提现 (WITHDRAW)](#合约-solana-提现-withdraw)
  - [查询提现信息 (USER_DATA)](#查询提现信息-user_data)
  - [充提记录 (USER_DATA)](#充提记录-user_data)
  - [钱包划转 (TRADE)](#钱包划转-trade)
- [Aster-Chain 现货提现与划转接口](#aster-chain-现货提现与划转接口)
  - [现货提现 (WITHDRAW)](#现货提现-withdraw)
  - [现货 Solana 提现 (WITHDRAW)](#现货-solana-提现-withdraw)
  - [钱包划转 (TRADE)](#钱包划转-trade-1)
- [Aster-Chain 提现接口](#aster-chain-提现接口)
  - [估算提现手续费 (NONE)](#估算提现手续费-none)

---

# Aster-Chain 账户接口

## 查询账户状态 (USER_DATA)

> **响应:**

```javascript
{
    "status": "PRIVATE" // "PUBLIC" 或 "PRIVATE"
}
```

`GET /aster-chain/v3/account/status`

查询当前账户的隐私状态。

**权重:** 1

**参数:**

无

---

## 修改账户状态 (TRADE)

> **响应:**

```javascript
{
    "status": "PRIVATE" // "PUBLIC" 或 "PRIVATE"
}
```

`POST /aster-chain/v3/account/modify-status`

修改账户隐私状态。更新成功后，变更将广播至 Aster Chain。

**权重:** 5

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| status | STRING | YES | 账户隐私模式：`"PUBLIC"` 或 `"PRIVATE"` |

---

## 转账至地址 (WITHDRAW)

> **响应:**

```javascript
{
    "transferId": "123456789",
    "asset": "USDT",
    "amount": "10.00",
    "toAddress": "0xAbCd1234...",
    "timestamp": 1699900800000,
    "status": "SUCCESS"  // "SUCCESS" 或 "PENDING"
}
```

`POST /aster-chain/v3/transfer`

将资产转账至另一个 Aster Chain 地址。接收地址必须属于已注册的 Aster Chain 用户。

**权重:** 50

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| asset | STRING | YES | 转账资产名称（如 `"USDT"`） |
| amount | DECIMAL | YES | 转账金额，必须大于 0 |
| toAddress | STRING | YES | 接收方的 Aster Chain 钱包地址 |
| clientTranId | STRING | NO | 客户端自定义划转 ID，若未提供则自动生成 |
| nonce | LONG | YES | 微秒时间戳 |
| user | STRING | YES | 发起账户钱包地址 |
| signature | STRING | YES | EIP-712 签名，使用 `user` 账户的钱包私钥签名 |

---

# Aster-Chain 质押接口

## 查询质押账户状态 (USER_DATA)

> **响应:**

```javascript
{
    "stakeAccountStatus": "ACTIVE"  // "ACTIVE"、"INACTIVE" 或 "PENDING"
}
```

`GET /aster-chain/v3/staking/stakeAccountStatus`

查询当前用户的质押账户状态。

**权重:** 1

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| nonce | LONG | YES | 微秒时间戳 |
| signer | STRING | YES | 代理钱包地址（被授权代表账户签名的子钱包） |
| signature | STRING | YES | EIP-712 签名，使用 `signer` 钱包私钥签名 |

---

## 查询我的质押 (USER_DATA)

> **响应:**

```javascript
{
    "validatorAddress": "0x1a2b3c4d...",
    "stakeAmount": "1000.00",
    "periodCode": "90D",
    "startTime": 1699900800000,
    "endTime": 1707676800000,
    "status": "ACTIVE"  // "ACTIVE"、"UNLOCKING" 或 "COMPLETED"
}
```

`GET /aster-chain/v3/staking/myStaking`

查询当前用户的质押仓位详情。

**权重:** 1

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| nonce | LONG | YES | 微秒时间戳 |
| signer | STRING | YES | 代理钱包地址（被授权代表账户签名的子钱包） |
| signature | STRING | YES | EIP-712 签名，使用 `signer` 钱包私钥签名 |

---

## 查询可领取奖励 (USER_DATA)

> **响应:**

```javascript
{
    "claimableAmount": "12.50",
    "asset": "ASTER",
    "accruedRewards": "25.00",
    "lastClaimTime": 1699900800000
}
```

`GET /aster-chain/v3/staking/claimableRewards`

查询当前用户可领取的质押奖励数量。

**权重:** 1

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| nonce | LONG | YES | 微秒时间戳 |
| signer | STRING | YES | 代理钱包地址（被授权代表账户签名的子钱包） |
| signature | STRING | YES | EIP-712 签名，使用 `signer` 钱包私钥签名 |

---

## 创建质押 (TRADE)

> **响应:**

```javascript
{
    "result": "SUCCESS"
}
```

`POST /aster-chain/v3/staking/create`

创建新的质押仓位，将代币委托至指定验证节点。链上操作类型为 `TokenDelegate`（`Stake`）。

**权重:** 5

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| validatorAddress | STRING | YES | 目标验证节点的链上地址 |
| stakeAmount | DECIMAL | YES | 质押代币数量，必须大于 0 |
| periodCode | STRING | YES | 锁定周期代码，可选值：`"26_WEEKS"`、`"52_WEEKS"`、`"104_WEEKS"`、`"156_WEEKS"`、`"208_WEEKS"` |
| nonce | LONG | YES | 微秒时间戳 |
| user | STRING | YES | 发起账户钱包地址 |
| signature | STRING | YES | EIP-712 签名，使用 `user` 账户的钱包私钥签名 |

---

## 追加质押 (TRADE)

> **响应:**

```javascript
{
    "result": "SUCCESS"
}
```

`POST /aster-chain/v3/staking/deposit`

向指定验证节点的已有质押仓位追加代币。链上操作类型为 `TokenDelegate`（`AddStake`）。

**权重:** 5

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| validatorAddress | STRING | YES | 目标验证节点的链上地址 |
| stakeAmount | DECIMAL | YES | 追加质押的代币数量，必须大于 0 |
| nonce | LONG | YES | 微秒时间戳 |
| user | STRING | YES | 发起账户钱包地址 |
| signature | STRING | YES | EIP-712 签名，使用 `user` 账户的钱包私钥签名 |

---

## 更新锁定期 (TRADE)

> **响应:**

```javascript
{
    "result": "SUCCESS"
}
```

`POST /aster-chain/v3/staking/updateLockPeriod`

延长当前质押仓位的锁定周期。链上操作类型为 `TokenDelegate`（`ExtendStakingTime`）。

**权重:** 5

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| periodCode | STRING | YES | 新的锁定周期代码，可选值：`"26_WEEKS"`、`"52_WEEKS"`、`"104_WEEKS"`、`"156_WEEKS"`、`"208_WEEKS"`，须长于当前锁定周期 |
| nonce | LONG | YES | 微秒时间戳 |
| user | STRING | YES | 发起账户钱包地址 |
| signature | STRING | YES | EIP-712 签名，使用 `user` 账户的钱包私钥签名 |

---

## 领取奖励 (TRADE)

> **响应:**

```javascript
{
    "result": "SUCCESS"
}
```

`POST /aster-chain/v3/staking/claimRewards`

领取已累积的质押奖励。链上操作类型为 `TokenDelegate`（`ClaimRewards`）。

**权重:** 5

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| requestedAmount | DECIMAL | YES | 申请领取的奖励数量，必须大于 0 且不超过可领取余额 |
| nonce | LONG | YES | 微秒时间戳 |
| user | STRING | YES | 发起账户钱包地址 |
| signature | STRING | YES | EIP-712 签名，使用 `user` 账户的钱包私钥签名 |

---

# Aster-Chain 合约提现与划转接口

## 合约提现 (WITHDRAW)

> **响应:**

```javascript
{
    "withdrawId": "987654321",
    "hash": "0xabc123..."
}
```

`POST /aster-chain/v3/perp/user-withdraw`

从合约账户提现至链上地址。

**权重:** 5

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| asset | STRING | YES | 资产名称（如 `"USDT"`） |
| chainId | INTEGER | YES | 目标链 ID |
| amount | STRING | YES | 提现金额 |
| fee | STRING | YES | 提现手续费 |
| receiver | STRING | YES | 接收方链上地址 |
| userNonce | STRING | YES | 签名中包含的用户端 nonce |
| userSignature | STRING | YES | 用户对提现参数的签名 |

---

## 合约 Solana 提现 (WITHDRAW)

> **响应:**

```javascript
{
    "withdrawId": "987654321",
    "hash": "0xabc123..."
}
```

`POST /aster-chain/v3/perp/user-solana-withdraw`

从合约账户提现至 Solana 地址。

**权重:** 5

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| asset | STRING | YES | 资产名称（如 `"USDT"`） |
| chainId | INTEGER | YES | 目标链 ID |
| amount | STRING | YES | 提现金额 |
| fee | STRING | YES | 提现手续费 |
| receiver | STRING | YES | 接收方 Solana 地址 |
| userNonce | STRING | YES | 签名中包含的用户端 nonce |
| userSignature | STRING | YES | 用户对提现参数的签名 |

---

## 查询提现信息 (USER_DATA)

> **响应:**

```javascript
{
    "userDailyLimit": "10000",
    "userRemainingDailyLimit": "9500",
    "totalDailyLimit": "100000",
    "totalRemainingDailyLimit": "95000",
    "balances": {
        "USDT": {
            "currency": "USDT",
            "spotTotalWithdrawAmount": "0",
            "perpTotalWithdrawAmount": "500",
            "dailyLimit": "5000",
            "chainBalances": {
                "1": {
                    "chainId": 1,
                    "spotMaxWithdrawAmount": "1000",
                    "perpMaxWithdrawAmount": "4500",
                    "chainLimit": "5000",
                    "withdrawFee": "0.5"
                }
            }
        }
    }
}
```

`GET /aster-chain/v3/perp/user-withdraw-info`

查询当前用户各资产、各链的提现限额及可用余额。

**权重:** 1

**参数:**

无

---

## 充提记录 (USER_DATA)

> **响应:**

```javascript
[
    {
        "id": "12345",
        "type": "WITHDRAW",   // "DEPOSIT" 或 "WITHDRAW"
        "asset": "USDT",
        "amount": "100",
        "state": "COMPLETED",
        "txHash": "0xabc123...",
        "time": 1699900800000,
        "chainId": 1,
        "accountType": "perp"
    }
]
```

`GET /aster-chain/v3/perp/deposit-withdraw-history`

查询当前用户合约账户的充值与提现历史记录。

**权重:** 5

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| chainId | STRING | NO | 按链 ID 过滤记录 |

---

## 钱包划转 (TRADE)

> **响应:**

```javascript
{
    "tranId": 123456789,
    "status": "SUCCESS"
}
```

`POST /aster-chain/v3/perp/wallet/transfer`

在现货钱包与合约账户之间划转资产。

**权重:** 5

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| asset | STRING | YES | 资产名称（如 `"USDT"`） |
| amount | DECIMAL | YES | 划转金额，必须大于 0 |
| clientTranId | STRING | YES | 客户端自定义划转 ID |
| kindType | STRING | YES | 划转方向：`"SPOT_FUTURE"`（现货 → 合约）或 `"FUTURE_SPOT"`（合约 → 现货） |
| nonce | LONG | YES | 微秒时间戳 |
| user | STRING | YES | 发起账户钱包地址 |
| signature | STRING | YES | EIP-712 签名，使用 `user` 账户的钱包私钥签名 |

---

# Aster-Chain 现货提现与划转接口

## 现货提现 (WITHDRAW)

> **响应:**

```javascript
{
    "withdrawId": "987654321",
    "hash": "0xabc123..."
}
```

`POST /aster-chain/v3/spot/user-withdraw`

从现货账户提现至链上地址。

**权重:** 5

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| asset | STRING | YES | 资产名称（如 `"USDT"`） |
| chainId | INTEGER | YES | 目标链 ID |
| amount | STRING | YES | 提现金额 |
| fee | STRING | YES | 提现手续费 |
| receiver | STRING | YES | 接收方链上地址 |
| userNonce | STRING | YES | 签名中包含的用户端 nonce |
| userSignature | STRING | YES | 用户对提现参数的签名 |

---

## 现货 Solana 提现 (WITHDRAW)

> **响应:**

```javascript
{
    "withdrawId": "987654321",
    "hash": "0xabc123..."
}
```

`POST /aster-chain/v3/spot/user-solana-withdraw`

从现货账户提现至 Solana 地址。

**权重:** 5

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| asset | STRING | YES | 资产名称（如 `"USDT"`） |
| chainId | INTEGER | YES | 目标链 ID |
| amount | DECIMAL | YES | 提现金额 |
| fee | DECIMAL | YES | 提现手续费 |
| receiver | STRING | YES | 接收方 Solana 地址 |
| userNonce | STRING | YES | 签名中包含的用户端 nonce |
| userSignature | STRING | YES | 用户对提现参数的签名 |

---

## 钱包划转 (TRADE)

> **响应:**

```javascript
{
    "tranId": 123456789,
    "status": "SUCCESS"
}
```

`POST /aster-chain/v3/spot/wallet/transfer`

在现货钱包与合约账户之间划转资产。

**权重:** 5

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| asset | STRING | YES | 资产名称（如 `"USDT"`） |
| amount | DECIMAL | YES | 划转金额，必须大于 0 |
| clientTranId | STRING | YES | 客户端自定义划转 ID |
| kindType | STRING | YES | 划转方向：`"SPOT_FUTURE"`（现货 → 合约）或 `"FUTURE_SPOT"`（合约 → 现货） |
| nonce | LONG | YES | 微秒时间戳 |
| user | STRING | YES | 发起账户钱包地址 |
| signature | STRING | YES | EIP-712 签名，使用 `user` 账户的钱包私钥签名 |

---

# Aster-Chain 提现接口

## 估算提现手续费 (NONE)

> **响应:**

```javascript
{
    "gasPrice": 1000000000,
    "gasLimit": 21000,
    "nativePrice": "1800.00",
    "tokenPrice": "1.00",
    "gasCost": "0.000021",
    "gasUsdValue": "0.038"
}
```

`GET /aster-chain/v3/withdraw/estimateFee`

估算指定链和资产的提现 Gas 手续费。

**权重:** 1

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| chainId | INTEGER | YES | 目标链 ID |
| asset | STRING | YES | 资产名称（如 `"USDT"`） |
