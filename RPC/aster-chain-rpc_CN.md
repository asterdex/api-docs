- [基本信息](#基本信息)
  - [接口通用说明](#接口通用说明)
  - [访问限制](#访问限制)
  - [错误码](#错误码)
- [链上 RPC 接口](#链上-rpc-接口)
  - [查询账户余额](#查询账户余额)
  - [查询当前挂单](#查询当前挂单)
  - [查询用户期货成交记录](#查询用户期货成交记录)
  - [查询用户现货当前挂单](#查询用户现货当前挂单)
  - [查询用户现货成交记录](#查询用户现货成交记录)

# 基本信息

## 接口通用说明

* 所有接口均采用 JSON-RPC 2.0 协议，通过 HTTP POST 方式调用。
* 接口基础地址：**https://tapi.asterdex.com/info**
* 所有请求需设置请求头 `Content-Type: application/json`。
* 仅支持单个请求，不支持批量请求（由多个请求对象组成的 JSON 数组）。`params` 必须为 JSON 数组。
* 请求中的 `id`（数字、字符串或对象）会在响应中原样返回。
* `blockTag` 参数传入 `"latest"` 表示查询最新状态。目前仅支持查询最新状态，请传入 `"latest"`。
* 所有时间相关字段和参数均为毫秒级时间戳，时间参数必须以 JSON 数字（而非字符串）传入。
* 交易对名称区分大小写，必须为大写，如 `"BTCUSDT"`。
* 无数据的字段会直接从响应中省略，而不是返回空数组（如 `perpAssets`、`openOrders`、`fills`）。

> **注意：** 在 Open Orders 和 Fills 接口中，隐私模式仅影响开启后的新订单；非隐私模式下完成的历史订单仍按正常规则展示。

## 访问限制

* 每个方法的权重均为 1。
* 按客户端 IP 限流。
* 超出限制时接口返回 HTTP `429 Too Many Requests`，请至少等待 1 秒后再重试。

## 错误码

错误遵循 JSON-RPC 2.0 格式，HTTP 状态码为 `200`：

```javascript
{
  "id": 1,
  "jsonrpc": "2.0",
  "error": {
    "code": -32603,
    "message": "Internal error: Time range exceeds 7 days"
  }
}
```

错误码 | 错误信息 | 触发场景
------ | -------- | --------
-32601 | `Method not found` | 缺少 `method`，或 `method` 不是以下任一方法
-32603 | `Internal error: Invalid params` | `params` 为空，或 `address` 缺失 / 不是字符串
-32603 | `Internal error: Time range exceeds 7 days` | `to - from` 大于 7 天（恰好 7 天是允许的）
-32603 | `Internal error: ...` | 该地址没有 Aster 账户
-32603 | `Internal error: ...` | 其他非法输入（如不存在的期货 `symbol`、参数 JSON 类型错误）或内部错误

在 HTTP 层面不是合法 JSON-RPC 的请求（JSON 格式错误、批量数组，或 `params` 以对象形式传入）会返回 HTTP `400`。

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
    "accountPrivacy": "disabled",
    "perpAssets": [
      {
        "asset": "ASTER",
        "walletBalance": 4812.0
      },
      {
        "asset": "USDT",
        "walletBalance": 99999998.977696
      }
    ],
    "spotAssets": [
      {
        "asset": "ASTER",
        "walletBalance": 29.9772
      },
      {
        "asset": "USDT",
        "walletBalance": 1000.5
      }
    ],
    "positions": [
      {
        "tradingProduct": "perps",
        "positions": [
          {
            "id": "98000000379377_ASTERUSDT_BOTH",
            "symbol": "ASTERUSDT",
            "positionAmount": "40.00",
            "positionSide": "BOTH",
            "notionalValue": "27.8688792000",
            "unrealizedProfit": "-0.0111208000",
            "cumRealized": "0.20000000"
          }
        ]
      }
    ],
    "staking": {
      "totalStakedAmount": "125000.00000000",
      "totalUnclaimedRewards": [
        {
          "asset": "ASTER",
          "amount": "3820.45120000"
        }
      ],
      "totalPendingStakeAmount": "50.00000000",
      "totalPendingUnstakeAmount": "100.00000000"
    }
  },
  "id": {},
  "jsonrpc": "2.0"
}
```

**返回字段说明：**

字段名 | 类型 | 说明
------ | ---- | ----
address | STRING | 钱包地址
accountPrivacy | STRING | 隐私模式状态：`"disabled"` 已关闭 / `"enabled"` 已开启
perpAssets | ARRAY | 永续合约（期货）钱包资产列表；仅列出非零资产，无资产时省略
perpAssets[].asset | STRING | 资产名称
perpAssets[].walletBalance | NUMBER | 钱包余额（JSON 数字；极小的值可能以指数形式表示，如 `1.274e-05`）
spotAssets | ARRAY | 现货钱包资产列表；仅列出非零资产，无资产时省略
spotAssets[].asset | STRING | 资产名称
spotAssets[].walletBalance | NUMBER | 钱包余额
positions | ARRAY | 按交易产品分组的持仓列表；该地址无持仓时省略
positions[].tradingProduct | STRING | `"perps"`（Pro 模式期货）或 `"shieldmode"`（Shield 模式）
staking | OBJECT | 质押信息。各金额字段为 0 时返回 `null`；质押信息无法加载时整个对象省略。
staking.totalStakedAmount | STRING | 当前质押 ASTER 总额（8 位小数）
staking.totalUnclaimedRewards | ARRAY | 未领取奖励列表，为 0 时返回 `null`
staking.totalUnclaimedRewards[].asset | STRING | 奖励资产（当前为 `ASTER`）
staking.totalUnclaimedRewards[].amount | STRING | 未领取奖励数量（8 位小数）
staking.totalPendingStakeAmount | STRING | 待处理质押总额（8 位小数）
staking.totalPendingUnstakeAmount | STRING | 待处理解押总额（8 位小数）

**`tradingProduct` 为 `"perps"` 时的持仓字段：**

字段名 | 类型 | 说明
------ | ---- | ----
id | STRING | 持仓 ID，格式为 `{userId}_{symbol}_{positionSide}`
symbol | STRING | 交易对名称
positionAmount | STRING | 持仓数量（单向持仓模式下空仓为负数）
positionSide | STRING | 持仓方向：`BOTH`、`LONG` 或 `SHORT`
notionalValue | STRING | 持仓名义价值
unrealizedProfit | STRING | 未实现盈亏
cumRealized | STRING | 该持仓的累计已实现盈亏

**`tradingProduct` 为 `"shieldmode"` 时的持仓字段：**

字段名 | 类型 | 说明
------ | ---- | ----
positionId | STRING | 持仓 ID
symbol | STRING | 交易对名称
isLong | BOOLEAN | `true` 为多仓，`false` 为空仓
leverage | INT | 杠杆倍数
marginAsset | STRING | 保证金资产
margin | STRING | 保证金
entryPrice | STRING | 开仓价格
liqPrice | STRING | 强平价格
qty | STRING | 持仓数量
tp | STRING | 止盈价格
sl | STRING | 止损价格
cumFundingFee | STRING | 累计资金费
pnl2usdt | STRING | 以 USDT 计的未实现盈亏
pnlPercentage | STRING | 未实现盈亏百分比
createTime | STRING | 开仓时间（毫秒时间戳）
feeMode | STRING | 手续费模式
openChainHash | STRING | 开仓交易的链上哈希

> **注意：** 隐私模式开启时，`result` 中仅包含 `address` 和 `accountPrivacy`（`"enabled"`），不返回资产、持仓和质押信息。

## 查询当前挂单

``
POST /info
``

查询指定地址的期货当前挂单。

> **说明：** 仅返回创建时间不早于 block 1 创世时间（`1772678119418`）的挂单。按创建时间倒序排列（最新在前），最多返回最新的 **1000** 条。

**方法名：** `aster_openOrders`

**权重：**
1

**请求参数（params 数组）：**

下标 | 参数名 | 类型 | 是否必填 | 说明
---- | ------ | ---- | -------- | ----
0 | address | STRING | 是 | 要查询的钱包地址
1 | symbol | STRING | 否 | 交易对名称（如 `"BTCUSDT"`）；传 `null` 或 `""` 查询所有交易对。传入不存在的交易对会返回错误 `-32603`。
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
    "accountPrivacy": "disabled",
    "openOrders": [
      {
        "orderId": "web_AD_7jz2xjo0ma4nblniq_98",
        "symbol": "TRUMPUSDT",
        "side": "SELL",
        "type": "LIMIT",
        "origQty": "4.44000000",
        "price": "10.00000000"
      },
      {
        "orderId": "web_AD_4u1emfjslzt4hqnc5_98",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "LIMIT",
        "origQty": "0.00100000",
        "price": "95000.00000000"
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
accountPrivacy | STRING | 隐私模式状态：`"disabled"` 已关闭 / `"enabled"` 已开启
openOrders | ARRAY | 当前挂单列表；无挂单时省略
openOrders[].orderId | STRING | 客户端订单 ID
openOrders[].symbol | STRING | 交易对名称
openOrders[].side | STRING | 买卖方向：`BUY` 买入 / `SELL` 卖出
openOrders[].type | STRING | 订单类型，如 `LIMIT`、`STOP`、`TAKE_PROFIT`、`STOP_MARKET`、`TAKE_PROFIT_MARKET`
openOrders[].origQty | STRING | 原始委托数量
openOrders[].price | STRING | `LIMIT`、`STOP`、`TAKE_PROFIT` 订单返回委托价格；其他类型返回字符串 `"market"`


## 查询用户期货成交记录

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
1 | symbol | STRING | 否 | 交易对名称（如 `"BTCUSDT"`）；传 `null` 或 `""` 查询所有交易对
2 | from | LONG | 否 | 查询起始时间（毫秒时间戳）。若不填且填了 `to`，则默认为 `to - 7天`；若两者均不填，则默认为当前时间往前 7 天。若 `from` 早于 `1772678119418`（block 1 创世时间），则会被调整为 `1772678119418`，返回的 `startTime` 为调整后的值。
3 | to | LONG | 否 | 查询结束时间（毫秒时间戳）。若不填且填了 `from`，则默认为 `from + 7天`；若两者均不填，则默认为当前时间。`to - from` 不得超过 7 天（`604800000` 毫秒），否则返回错误 `-32603`。若 `to` 不晚于 `1772678119418`，`result` 中仅包含 `address` 和 `accountPrivacy`。
4 | blockTag | STRING | 是 | 区块标签，传入 `"latest"` 表示查询最新状态

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
      "0x1c3C4*************",
      null,
      null,
      null,
      "latest"
    ]
  }'
```

> **返回结果：**

```javascript
{
  "result": {
    "address": "0x1c3C4*************",
    "accountPrivacy": "disabled",
    "startTime": 1773916057398,
    "endTime": 1774520857398,
    "fills": [
      {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "price": "69999",
        "qty": "0.001",
        "time": 1774233564000
      },
      {
        "symbol": "BTCUSDT",
        "side": "SELL",
        "price": "70658.6",
        "qty": "0.001",
        "time": 1774084612000
      },
      {
        "symbol": "ETHUSDT",
        "side": "BUY",
        "price": "1971",
        "qty": "0.013",
        "time": 1774084518000
      },
      {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "price": "70676.7",
        "qty": "0.001",
        "time": 1774084489000
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
accountPrivacy | STRING | 隐私模式状态：`"disabled"` 已关闭 / `"enabled"` 已开启
startTime | LONG | 实际查询起始时间（毫秒时间戳）
endTime | LONG | 实际查询结束时间（毫秒时间戳）
fills | ARRAY | 时间范围内的成交记录，按时间倒序排列（最新在前），最多返回最新的 `1000` 条；无成交时省略
fills[].symbol | STRING | 交易对名称
fills[].side | STRING | 成交方向：`BUY` 买入 / `SELL` 卖出
fills[].price | STRING | 成交价格
fills[].qty | STRING | 成交数量
fills[].time | LONG | 成交时间（毫秒时间戳）

> **注意：** 该接口仅返回期货成交数据。


## 查询用户现货当前挂单

``
POST /info
``

查询指定地址的现货当前挂单。

> **说明：** 仅返回创建时间不早于 block 1 创世时间（`1772678119418`）的挂单。按创建时间倒序排列（最新在前），最多返回最新的 **1000** 条。

**方法名：** `aster_spotOpenOrders`

**权重：**
1

**请求参数（params 数组）：**

下标 | 参数名 | 类型 | 是否必填 | 说明
---- | ------ | ---- | -------- | ----
0 | address | STRING | 是 | 要查询的钱包地址
1 | symbol | STRING | 否 | 交易对名称（如 `"ASTCUSDT"`）；传 `null` 或 `""` 查询所有交易对。传入不存在的交易对返回空结果。
2 | blockTag | STRING | 是 | 区块标签，传入 `"latest"` 表示查询最新状态

> **请求示例：**

```shell
curl -X POST "https://tapi.asterdex.com/info" \
  -H "accept: */*" \
  -H "Content-Type: application/json" \
  -d '{
    "id": {},
    "jsonrpc": "2.0",
    "method": "aster_spotOpenOrders",
    "params": [
      "0x90B8DE626a8*****************",
      null,
      "latest"
    ]
  }'
```

> **返回结果：**

```javascript
{
  "result": {
    "address": "0x90B8DE626a8***************",
    "accountPrivacy": "enabled",
    "openOrders": [
      {
        "orderId": "web_rgXtfO0hXb3EbaagJYLe",
        "symbol": "ASTCUSDT",
        "side": "BUY",
        "type": "LIMIT",
        "origQty": "0.00600000",
        "price": "19000.00000000"
      },
      {
        "orderId": "web_iXqhwgrotPEFZ7hpw1vq",
        "symbol": "ASTCUSDC",
        "side": "SELL",
        "type": "LIMIT",
        "origQty": "0.00420000",
        "price": "49000.00000000"
      },
      {
        "orderId": "web_dUdf2dUyFfvp4mqauXKg",
        "symbol": "ADOGUSDT",
        "side": "BUY",
        "type": "LIMIT",
        "origQty": "1000.00000000",
        "price": "4.20000000"
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
accountPrivacy | STRING | 隐私模式状态：`"disabled"` 已关闭 / `"enabled"` 已开启
openOrders | ARRAY | 当前挂单列表；无挂单时省略
openOrders[].orderId | STRING | 客户端订单 ID
openOrders[].symbol | STRING | 交易对名称
openOrders[].side | STRING | 买卖方向：`BUY` 买入 / `SELL` 卖出
openOrders[].type | STRING | 订单类型，如 `LIMIT`、`STOP`、`TAKE_PROFIT`、`STOP_MARKET`、`TAKE_PROFIT_MARKET`
openOrders[].origQty | STRING | 原始委托数量
openOrders[].price | STRING | `LIMIT`、`STOP`、`TAKE_PROFIT` 订单返回委托价格；其他类型返回字符串 `"market"`


## 查询用户现货成交记录

``
POST /info
``

查询指定地址在指定时间范围内的现货历史成交记录。

**方法名：** `aster_spotUserFills`

**权重：**
1

**请求参数（params 数组）：**

下标 | 参数名 | 类型 | 是否必填 | 说明
---- | ------ | ---- | -------- | ----
0 | address | STRING | 是 | 要查询的钱包地址
1 | symbol | STRING | 否 | 交易对名称（如 `"ASTCUSDT"`）；传 `null` 或 `""` 查询所有交易对
2 | from | LONG | 否 | 查询起始时间（毫秒时间戳）。若不填且填了 `to`，则默认为 `to - 7天`；若两者均不填，则默认为当前时间往前 7 天。若 `from` 早于 `1772678119418`（block 1 创世时间），则会被调整为 `1772678119418`，返回的 `startTime` 为调整后的值。
3 | to | LONG | 否 | 查询结束时间（毫秒时间戳）。若不填且填了 `from`，则默认为 `from + 7天`；若两者均不填，则默认为当前时间。`to - from` 不得超过 7 天（`604800000` 毫秒），否则返回错误 `-32603`。若 `to` 不晚于 `1772678119418`，`result` 中仅包含 `address` 和 `accountPrivacy`。
4 | blockTag | STRING | 是 | 区块标签，传入 `"latest"` 表示查询最新状态

> **请求示例：**

```shell
curl -X POST "https://tapi.asterdex.com/info" \
  -H "accept: */*" \
  -H "Content-Type: application/json" \
  -d '{
    "id": {},
    "jsonrpc": "2.0",
    "method": "aster_spotUserFills",
    "params": [
      "0x90B8DE626a8*****************",
      null,
      null,
      null,
      "latest"
    ]
  }'
```

> **返回结果：**

```javascript
{
  "result": {
    "address": "0x90B8DE626a8***************",
    "accountPrivacy": "enabled",
    "startTime": 1776410901599,
    "endTime": 1777015701599,
    "fills": [
      {
        "symbol": "ASTCUSDT",
        "side": "BUY",
        "price": "21000",
        "qty": "0.00170000",
        "time": 1777000095000
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
accountPrivacy | STRING | 隐私模式状态：`"disabled"` 已关闭 / `"enabled"` 已开启
startTime | LONG | 实际查询起始时间（毫秒时间戳）
endTime | LONG | 实际查询结束时间（毫秒时间戳）
fills | ARRAY | 时间范围内的成交记录，按时间倒序排列（最新在前），最多返回最新的 `1000` 条；无成交时省略
fills[].symbol | STRING | 交易对名称
fills[].side | STRING | 成交方向：`BUY` 买入 / `SELL` 卖出
fills[].price | STRING | 成交价格
fills[].qty | STRING | 成交数量
fills[].time | LONG | 成交时间（毫秒时间戳）

> **注意：** 该接口仅返回现货成交数据。