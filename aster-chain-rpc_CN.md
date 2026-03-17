- [基本信息](#基本信息)
  - [接口通用说明](#接口通用说明)
- [链上 RPC 接口](#链上-rpc-接口)
  - [查询账户余额](#查询账户余额)
  - [查询当前挂单](#查询当前挂单)
  - [查询用户成交记录](#查询用户成交记录)

# 基本信息

## 接口通用说明

* 所有接口均采用 JSON-RPC 2.0 协议，通过 HTTP POST 方式调用。
* 接口基础地址：**https://tapi.asterdex.com/info**
* 所有请求需设置请求头 `Content-Type: application/json`。
* `blockTag` 参数传入 `"latest"` 表示查询最新状态。
* 所有时间相关字段均为毫秒级时间戳。

> **注意：** 以下接口仅在用户**关闭隐私模式**时返回数据。如果用户开启了隐私模式，接口将不返回任何数据。

---

# 链上 RPC 接口

## 查询账户余额

``
POST /info
``

查询指定地址的账户余额及持仓信息。

**方法名：** `aster_getBalance`

**权重：**
1

**请求参数（params 数组）：**

下标 | 参数名 | 类型 | 是否必填 | 说明
---- | ------ | ---- | -------- | ----
0 | address | STRING | 是 | 要查询的钱包地址
1 | blockTag | STRING | 是 | 区块标签，传入 `"latest"` 表示查询最新状态

> **请求示例：**

```shell
curl -X POST "https://tapi.asterdex.com/info" \
  -H "accept: */*" \
  -H "Content-Type: application/json" \
  -d '{
    "id": {},
    "jsonrpc": "2.0",
    "method": "aster_getBalance",
    "params": [
      "0x690931c*********",
      "latest"
    ]
  }'
```

> **返回结果：**

```javascript
{
  "result": {
    "address": "0x690931c*********",
    "accountPrivy": "disabled",
    "perpAssets": [
      {
        "asset": "USD1",
        "walletBalance": 200.00000000
      },
      {
        "asset": "USDT",
        "walletBalance": 9049204461.84438644
      }
    ],
    "positions": [
      {
        "tradingProduct": "perps",
        "positions": [
          {
            "id": "98000000000389_BTCUSDT_BOTH",
            "symbol": "BTCUSDT",
            "collateral": "USDT",
            "positionAmount": "1.340",
            "entryPrice": "84490.74932115",
            "unrealizedProfit": "-13990.31797537",
            "askNotional": "0",
            "bidNotional": "60",
            "notionalValue": "99227.28611496",
            "markPrice": "74050.21351863",
            "leverage": 1,
            "isolated": false,
            "isolatedWallet": "0",
            "adl": 1,
            "positionSide": "BOTH",
            "marginValue": "99227.28611496"
          }
        ]
      }
    ]
  },
  "id": {},
  "jsonrpc": "2.0"
}
```

**返回字段说明：**

字段名 | 类型 | 说明
------ | ---- | ----
address | STRING | 钱包地址
accountPrivy | STRING | 隐私模式状态：`"disabled"` 已关闭 / `"enabled"` 已开启
perpAssets | ARRAY | 永续合约资产列表
perpAssets[].asset | STRING | 资产名称
perpAssets[].walletBalance | DECIMAL | 钱包余额
positions | ARRAY | 按交易产品分组的持仓列表
positions[].tradingProduct | STRING | 交易产品类型（如 `"perps"`）
positions[].positions[].id | STRING | 持仓 ID
positions[].positions[].symbol | STRING | 交易对名称
positions[].positions[].collateral | STRING | 保证金资产
positions[].positions[].positionAmount | STRING | 持仓数量
positions[].positions[].entryPrice | STRING | 平均开仓价格
positions[].positions[].unrealizedProfit | STRING | 未实现盈亏
positions[].positions[].notionalValue | STRING | 持仓名义价值
positions[].positions[].markPrice | STRING | 当前标记价格
positions[].positions[].leverage | INT | 杠杆倍数
positions[].positions[].isolated | BOOLEAN | 是否逐仓模式
positions[].positions[].isolatedWallet | STRING | 逐仓钱包余额
positions[].positions[].adl | INT | ADL 排队等级
positions[].positions[].positionSide | STRING | 持仓方向：`BOTH`、`LONG` 或 `SHORT`
positions[].positions[].marginValue | STRING | 保证金价值


## 查询当前挂单

``
POST /info
``

查询指定地址的所有当前挂单。

**方法名：** `aster_openOrders`

**权重：**
1

**请求参数（params 数组）：**

下标 | 参数名 | 类型 | 是否必填 | 说明
---- | ------ | ---- | -------- | ----
0 | address | STRING | 是 | 要查询的钱包地址
1 | symbol | STRING | 否 | 交易对名称（如 `"BTCUSDT"`）；传入 `""` 查询所有交易对
2 | blockTag | STRING | 是 | 区块标签，传入 `"latest"` 表示查询最新状态

> **请求示例：**

```shell
curl -X POST "https://tapi.asterdex.com/info" \
  -H "accept: */*" \
  -H "Content-Type: application/json" \
  -d '{
    "id": {},
    "jsonrpc": "2.0",
    "method": "aster_openOrders",
    "params": [
      "0x690931c*********",
      "",
      "latest"
    ]
  }'
```

> **返回结果：**

```javascript
{
  "result": {
    "address": "0x690931c*********",
    "accountPrivy": "disabled",
    "openOrders": [
      {
        "orderId": "web_AD_7jz2xjo0ma4nblniq_98",
        "symbol": "TRUMPUSDT",
        "side": "SELL",
        "type": "LIMIT",
        "origQty": "4.44000000",
        "status": "NEW"
      },
      {
        "orderId": "web_AD_4u1emfjslzt4hqnc5_98",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "LIMIT",
        "origQty": "0.00100000",
        "status": "NEW"
      }
    ]
  },
  "id": {},
  "jsonrpc": "2.0"
}
```

**返回字段说明：**

字段名 | 类型 | 说明
------ | ---- | ----
address | STRING | 钱包地址
accountPrivy | STRING | 隐私模式状态：`"disabled"` 已关闭 / `"enabled"` 已开启
openOrders | ARRAY | 当前挂单列表
openOrders[].orderId | STRING | 订单 ID
openOrders[].symbol | STRING | 交易对名称
openOrders[].side | STRING | 买卖方向：`BUY` 买入 / `SELL` 卖出
openOrders[].type | STRING | 订单类型：如 `LIMIT` 限价单、`MARKET` 市价单
openOrders[].origQty | STRING | 原始委托数量
openOrders[].status | STRING | 订单状态：如 `NEW` 待成交


## 查询用户成交记录

``
POST /info
``

查询指定地址在指定时间范围内的历史成交记录。

**方法名：** `aster_userFills`

**权重：**
1

**请求参数（params 数组）：**

下标 | 参数名 | 类型 | 是否必填 | 说明
---- | ------ | ---- | -------- | ----
0 | address | STRING | 是 | 要查询的钱包地址
1 | symbol | STRING | 是 | 交易对名称（如 `"BTCUSDT"`）
2 | from | LONG | 是 | 查询起始时间（毫秒时间戳）
3 | to | LONG | 是 | 查询结束时间（毫秒时间戳）
4 | limit | INT | 是 | 每页返回条数，每次最多返回 `1000` 条
5 | page | INT | 是 | 页码，从 `1` 开始
6 | blockTag | STRING | 是 | 区块标签，传入 `"latest"` 表示查询最新状态

> **请求示例：**

```shell
curl -X POST "https://tapi.asterdex.com/info" \
  -H "accept: */*" \
  -H "Content-Type: application/json" \
  -d '{
    "id": {},
    "jsonrpc": "2.0",
    "method": "aster_userFills",
    "params": [
      "0x690931c*********",
      "BTCUSDT",
      1772887745000,
      1773146945000,
      2,
      1,
      "latest"
    ]
  }'
```

> **返回结果：**

```javascript
{
  "result": {
    "address": "0x690931c*********",
    "accountPrivy": "disabled",
    "startTime": 1772887745000,
    "endTime": 1783146945000,
    "fills": [
      {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "price": "71087.9",
        "qty": "0.00100000",
        "time": 1773405618000
      },
      {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "price": "71088.1",
        "qty": "0.00100000",
        "time": 1773401493000
      }
    ]
  },
  "id": {},
  "jsonrpc": "2.0"
}
```

**返回字段说明：**

字段名 | 类型 | 说明
------ | ---- | ----
address | STRING | 钱包地址
accountPrivy | STRING | 隐私模式状态：`"disabled"` 已关闭 / `"enabled"` 已开启
startTime | LONG | 查询起始时间（毫秒时间戳）
endTime | LONG | 查询结束时间（毫秒时间戳）
fills | ARRAY | 成交记录列表
fills[].symbol | STRING | 交易对名称
fills[].side | STRING | 成交方向：`BUY` 买入 / `SELL` 卖出
fills[].price | STRING | 成交价格
fills[].qty | STRING | 成交数量
fills[].time | LONG | 成交时间（毫秒时间戳）