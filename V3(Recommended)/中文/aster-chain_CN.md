# Aster-Chain API 概览

* 本文档所列接口的 Base URL 为：**https://chainapi.asterdex.com**
* 所有接口响应均为 JSON 格式。

---

- [Aster-Chain 账户接口](#aster-chain-账户接口)
  - [查询账户状态 (USER_DATA)](#查询账户状态-user_data)
  - [修改账户状态 (TRADE)](#修改账户状态-trade)

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
