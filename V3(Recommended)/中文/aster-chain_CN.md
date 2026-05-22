# Aster-Chain API 概览

* 本文档所列接口的 Base URL 为：**https://chainapi.asterdex.com**
* 所有接口响应均为 JSON 格式。

---

- [Aster-Chain 账户接口](#aster-chain-账户接口)
  - [查询账户状态 (USER_DATA)](#查询账户状态-user_data)
  - [修改账户状态 (TRADE)](#修改账户状态-trade)
  - [转账至地址 (WITHDRAW)](#转账至地址-withdraw)

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
