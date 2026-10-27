# Aster-Chain API 概览

* 本文档所列接口的 Base URL 为：**https://chainapi.asterdex.com**
* 所有接口响应均为 JSON 格式。

---

- [Aster-Chain 账户接口](#aster-chain-账户接口)
  - [查询账户状态 (USER_DATA)](#查询账户状态-user_data)
  - [修改账户状态 (TRADE)](#修改账户状态-trade)
  - [转账至地址 (WITHDRAW)](#转账至地址-withdraw)
  - [批量转账至地址 (WITHDRAW)](#批量转账至地址-withdraw)
  - [查询批量转账历史 (USER_DATA)](#查询批量转账历史-user_data)
- [Aster-Chain 质押接口](#aster-chain-质押接口)
  - [查询质押账户状态 (USER_DATA)](#查询质押账户状态-user_data)
  - [查询我的质押 (USER_DATA)](#查询我的质押-user_data)
  - [查询可领取奖励 (USER_DATA)](#查询可领取奖励-user_data)
  - [创建质押 (TRADE)](#创建质押-trade)
  - [追加质押 (TRADE)](#追加质押-trade)
  - [更新锁定期 (TRADE)](#更新锁定期-trade)
  - [领取奖励 (TRADE)](#领取奖励-trade)
  - [查询锁定 Aster 总量 (NONE)](#查询锁定-aster-总量-none)
- [Aster-Chain 充值](#aster-chain-充值)
  - [EVM](#evm)
  - [Solana](#solana)
  - [SUI](#sui)
  - [查询用户充值地址 (USER_DATA)](#查询用户充值地址-user_data)
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

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| nonce | LONG | YES | 微秒时间戳 |
| signer | STRING | YES | 代理钱包地址（被授权代表账户签名的子钱包） |
| signature | STRING | YES | EIP-712 签名，使用 `signer` 钱包私钥签名 |

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
| nonce | LONG | YES | 微秒时间戳 |
| signer | STRING | YES | 代理钱包地址（被授权代表账户签名的子钱包） |
| signature | STRING | YES | EIP-712 签名，使用 `signer` 钱包私钥签名 |
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

## 批量转账至地址 (WITHDRAW)

> **响应:**

```javascript
{
    "clientTranId": "batch-20261026-000000001",
    "status": "I",       // 批次状态，见说明
    "totalCount": 2,
    "items": [
        {
            "toAddress": "0xAbCd1234...",
            "asset": "USDT",
            "transferId": "100001"
        },
        {
            "toAddress": "0xEf567890...",
            "asset": "USDT",
            "transferId": "100002"
        }
    ]
}
```

`POST /aster-chain/v3/batch-transfer`

在一次请求中将当前账户的资产转账至多个 Aster Chain 地址。每个接收地址都必须属于已注册的 Aster Chain 用户。

该接口异步处理：响应仅表示批次已受理。每笔转账的最终结果请通过 [查询批量转账历史 (USER_DATA)](#查询批量转账历史-user_data) 获取。

**示例代码:** [101_batchTransfer.js](https://github.com/asterdex/API-demo/blob/main/futures-v3-demo/101_batchTransfer.js)

**权重:** 50

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| clientTranId | STRING | YES | 客户端自定义批次 ID，长度 20~64。用于幂等：使用相同 `clientTranId` 重复提交时返回已有批次，不会重复创建 |
| items | STRING | YES | 转账明细的 JSON 数组，最多 10 条，字段见下表 |
| nonce | LONG | YES | 微秒时间戳 |
| user | STRING | YES | 发起账户钱包地址 |
| signature | STRING | YES | EIP-712 签名，使用 `user` 账户的钱包私钥签名 |

`items` 中每个元素的字段：

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| toAddress | STRING | YES | 接收方的 Aster Chain 钱包地址 |
| asset | STRING | YES | 资产名称（如 `"USDT"`），不区分大小写 |
| amount | STRING | YES | 转账金额，必须大于 0，最多 8 位小数 |
| transferChainId | INT | NO | 转账资产所在链的 Chain ID |

`items` 示例：

```json
[{"toAddress":"0xAbCd1234...","asset":"USDT","amount":"1.5"},{"toAddress":"0xEf567890...","asset":"USDT","amount":"2"}]
```

**说明:**

* 提交前会校验整个批次，任一条不合法则整批返回错误，不会执行任何转账：
  * `items` 不能为空，且不能超过 10 条。
  * `toAddress` 必须是合法的 EVM 地址，属于已注册的 Aster Chain 用户，且不能是自己的地址。
  * 同一批次中 `toAddress` + `asset` 不能重复。
  * `amount` 必须大于 0，且不超过 8 位小数。
* 账户处于 `PRIVATE` 模式时不可使用（见 [修改账户状态 (TRADE)](#修改账户状态-trade)）。
* 响应中的 `transferId` 为每笔转账的 ID，与历史查询响应中的 `transferId` 对应。

---

## 查询批量转账历史 (USER_DATA)

> **响应:**

```javascript
{
    "total": 1,
    "rows": [
        {
            "clientTranId": "batch-20261026-000000001",
            "status": "M",
            "createTime": 1761000000000,
            "updateTime": 1761000005000,
            "totalCount": 2,
            "successCount": 1,
            "failCount": 1,
            "partialCount": 0,
            "processingCount": 0,
            "failedItems": [
                {
                    "transferId": "100002",
                    "toAddress": "0xEf567890...",
                    "asset": "USDT",
                    "amount": "2",
                    "transferChainId": null,
                    "successAmount": null,
                    "status": "F",
                    "errorCode": "...",
                    "errorMsg": "...",
                    "createTime": 1761000000000,
                    "updateTime": 1761000005000
                }
            ],
            "details": [
                {
                    "transferId": "100001",
                    "toAddress": "0xAbCd1234...",
                    "asset": "USDT",
                    "amount": "1.5",
                    "transferChainId": null,
                    "successAmount": "1.5",
                    "status": "S",
                    "errorCode": null,
                    "errorMsg": null,
                    "createTime": 1761000000000,
                    "updateTime": 1761000003000
                },
                {
                    "transferId": "100002",
                    "toAddress": "0xEf567890...",
                    "asset": "USDT",
                    "amount": "2",
                    "transferChainId": null,
                    "successAmount": null,
                    "status": "F",
                    "errorCode": "...",
                    "errorMsg": "...",
                    "createTime": 1761000000000,
                    "updateTime": 1761000005000
                }
            ]
        }
    ]
}
```

`GET /aster-chain/v3/batch-transfer/history`

查询当前账户提交的批量转账及每笔明细的结果。

**权重:** 5

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| clientTranId | STRING | NO | 批次 ID。仅传 `clientTranId`、不传 `startTime` 和 `endTime` 时，只返回该批次，不受创建时间限制 |
| status | STRING | NO | 批次状态：`I`、`P`、`S`、`F` 或 `M` |
| startTime | LONG | NO | 批次创建时间（毫秒），包含。默认：`endTime` - 7 天 |
| endTime | LONG | NO | 批次创建时间（毫秒），不包含。默认：当前时间 |
| page | INT | NO | 页码，从 1 开始。默认：1 |
| limit | INT | NO | 每页批次数。默认：20，最大：100 |
| nonce | LONG | YES | 微秒时间戳 |
| signer | STRING | YES | 代理钱包地址（被授权代表账户签名的子钱包） |
| signature | STRING | YES | EIP-712 签名，使用 `signer` 钱包私钥签名 |

**说明:**

* 未传 `clientTranId`，或 `clientTranId` 与 `startTime`/`endTime` 一起传时，按批次创建时间查询：
  * `endTime` 必须晚于 `startTime`，且时间跨度不能超过 31 天。
  * `startTime` 和 `endTime` 都未传时，返回最近 7 天的批次。
* 每个批次的 `details` 包含该批次的全部明细，`failedItems` 仅包含失败的明细。
* 批次 / 明细状态：
  * `I`：待执行
  * `P`：执行中
  * `S`：成功
  * `F`：失败
  * `M`：部分成功
* `successAmount` 为该笔实际转账成功的金额。
* 所有时间均为毫秒。

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

## 查询锁定 Aster 总量 (NONE)

> **响应:**

```javascript
{
    "periodCode": "208_WEEKS",
    "totalVolume": 291534089.64644974
}
```

`GET /aster-chain/v3/staking/getLockedAster`

查询全网所有 208 周质押仓位中锁定的 ASTER 代币总量。

**权重:** 20

**参数:**

无

---

# Aster-Chain 充值

充值在源链上完成，不同网络的充值方式不同：

## EVM

EVM 链的充值通过与源链上的 vault 合约直接交互完成，有两种方式：

1. 调用 vault 合约的 `depositFor` 方法，交易链上确认后，资产入账至 `forAddress` 账户。
2. 直接向 vault 合约地址转账，资产入账至转账发起地址。

**主网合约地址：**

| 链 | Chain ID | 合约地址 |
|----|----------|----------|
| ETH | 1 | `0x604DD02d620633Ae427888d41bfd15e38483736E` |
| BSC | 56 | `0x128463A60784c4D3f46c23Af3f65Ed859Ba87974` |
| Arbitrum | 42161 | `0x9E36CB86a159d479cEd94Fa05036f235Ac40E1d5` |

**depositFor：**

```solidity
function depositFor(address currency, address forAddress, uint256 amount, uint256 broker) external payable
```

| 名称 | 类型 | 描述 |
|------|------|------|
| currency | ADDRESS | 代币合约地址；原生币（如 BNB、ETH）传固定占位地址 `0xfdAE1bA7C826aBDc4c99903c8056f82a1A04a615` |
| forAddress | ADDRESS | 接收充值资产的用户地址 |
| amount | UINT256 | 充值数量，使用代币最小单位（wei）；原生币必须与 `msg.value` 一致 |
| broker | UINT256 | 目标账户标识：传 `1000` 充值至**现货**账户，其他值充值至**合约**账户 |

* ERC20 充值需先对 vault 合约 `approve` 授权，且 `msg.value` 必须为 0。
* 原生币充值通过 `msg.value` 转入，金额必须与 `amount` 参数一致。

## Solana

Solana 链上**只能**通过调用以下合约方法充值，直接向 vault 地址转账**不会**入账。

**主网 Program 地址：** `EhUtRgu9iEbZXXRpEvDj6n1wnQRjMi2SERDo3c6bmN2c`

共有两个充值方法，参数均为 `amount`（u64，代币最小单位）：

1. `depositSol`：充值原生代币（SOL）。
2. `depositToken`：充值 SPL 代币（如 USDT）。

**depositSol accounts：**

| 账户 | isSigner | isMut | 描述 |
|------|----------|-------|------|
| signer | true | true | 充值用户的钱包地址，资产入账至该地址 |
| admin | false | false | Admin 账户 |
| solVault | false | true | SOL vault 账户 |
| systemProgram | false | false | 固定值：`11111111111111111111111111111111` |

**depositToken accounts：**

| 账户 | isSigner | isMut | 描述 |
|------|----------|-------|------|
| signer | true | false | 充值用户的钱包地址，资产入账至该地址 |
| admin | false | false | Admin 账户 |
| bank | false | false | 代币对应的 Bank 账户 |
| tokenVaultAuthority | false | false | Token vault authority 账户 |
| tokenVault | false | true | Token vault 账户 |
| depositor | false | true | 充值用户在 `tokenMint` 下的关联代币账户（ATA） |
| tokenMint | false | false | 代币 Mint 地址 |
| tokenProgram | false | false | 固定值：`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` |
| associatedTokenProgram | false | false | 固定值：`ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL` |
| systemProgram | false | false | 固定值：`11111111111111111111111111111111` |

* 目标账户：调用任一方法时，在指令 accounts **最后**追加 `programId` 账户（即 Program 地址）表示充值至**现货**账户；不追加则充值至**合约**账户。

## SUI

SUI 链仅支持**现货**账户。充值通过直接向用户专属充值地址转账完成，无需调用合约：

1. 调用[查询用户充值地址 (USER_DATA)](#查询用户充值地址-user_data) 获取 SUI 链上的充值地址。
2. 直接向该地址转账，交易链上确认后，资产入账至现货账户。

## 查询用户充值地址 (USER_DATA)

> **响应:**

```javascript
{
    "network": "SUI",
    "address": "0x9a40f0119b670fb6b155744b51981f91c4c4c8a20c333441a63853fe7d055c90"
}
```

`GET /aster-chain/v3/spot/user-deposit-address`

查询当前用户在指定网络的专属充值地址。仅支持现货账户。

**权重:** 1

**参数:**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|---------|------|
| network | STRING | NO | 网络类型，默认 `"SUI"` |

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
| signatureType | STRING | NO | 签名类型：`"EOA"` 或 `"SafeWallet"`，默认 `"EOA"`；账户为 Safe 钱包时传 `"SafeWallet"` |
| userSignature | STRING | YES | 用户对提现参数的签名；当 `signatureType=SafeWallet` 时，支持多个签名，以逗号分隔 |

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
| chainId | INTEGER | YES | 资产所属链的 Chain ID |
| signatureChainId | INTEGER | NO | 签名使用的链 ID（即 EIP-712 domain 中的 `chainId` 字段），未传时默认取 `chainId` |
| amount | STRING | YES | 提现金额 |
| fee | STRING | YES | 提现手续费 |
| receiver | STRING | YES | 接收方链上地址 |
| userNonce | STRING | YES | 签名中包含的用户端 nonce |
| signatureType | STRING | NO | 签名类型：`"EOA"` 或 `"SafeWallet"`，默认 `"EOA"`；账户为 Safe 钱包时传 `"SafeWallet"` |
| userSignature | STRING | YES | 用户对提现参数的签名；当 `signatureType=SafeWallet` 时，支持多个签名，以逗号分隔 |

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
