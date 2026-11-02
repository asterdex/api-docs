- [General Info](#general-info)
  - [General API Information](#general-api-information)
  - [Rate Limits](#rate-limits)
  - [Error Codes](#error-codes)
- [Chain RPC Endpoints](#chain-rpc-endpoints)
  - [Get Balance](#get-balance)
  - [Get Open Orders](#get-open-orders)
  - [Get User Futures Fills](#get-user-futures-fills)
  - [Get Spot Open Orders](#get-spot-open-orders)
  - [Get User Spot Fills](#get-user-spot-fills)

# General Info

## General API Information

* All endpoints use JSON-RPC 2.0 protocol via HTTP POST.
* The base endpoint is: **https://tapi.asterdex.com/info**
* All requests must set `Content-Type: application/json`.
* Only single requests are supported; batch requests (a JSON array of request objects) are rejected. `params` must be a JSON array.
* The `id` you send (number, string or object) is echoed back unchanged in the response.
* The `blockTag` parameter accepts `"latest"` to query the most recent state. Only the latest state is currently served; pass `"latest"`.
* All time-related fields and parameters are in milliseconds, and time parameters must be sent as JSON numbers (not strings).
* Symbols are case-sensitive and must be upper case, e.g. `"BTCUSDT"`.
* Fields with no data are omitted from the response rather than returned as empty arrays (e.g. `perpAssets`, `openOrders`, `fills`).

> **Note:** In the Open Orders and Fills endpoints, account privacy enabled only applies to new orders placed after it is enabled; orders completed when account privacy is disabled remain visible as usual.

## Rate Limits

* Every method has a weight of 1.
* Requests are rate-limited per client IP.
* When the limit is exceeded the endpoint returns HTTP `429 Too Many Requests`. Back off for at least 1 second before retrying.

## Error Codes

Errors follow the JSON-RPC 2.0 format and are returned with HTTP status `200`:

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

Code | Message | When
---- | ------- | ----
-32601 | `Method not found` | `method` is missing or not one of the methods below
-32603 | `Internal error: Invalid params` | `params` is empty, or `address` is missing / not a string
-32603 | `Internal error: Time range exceeds 7 days` | `to - from` is greater than 7 days (exactly 7 days is allowed)
-32603 | `Internal error: ...` | The address has no Aster account
-32603 | `Internal error: ...` | Other invalid input (e.g. a futures `symbol` that does not exist, a parameter of the wrong JSON type) or an internal failure

Requests that are not valid JSON-RPC at the HTTP level (malformed JSON, a batch array, or `params` sent as an object) are rejected with HTTP `400`.

---

# Chain RPC Endpoints

## Get Balance

``
POST /info
``

Query the account balance and position information for a given address.

**Method:** `aster_getBalance`

**Weight:**
1

**Parameters (params array):**

Index | Name | Type | Mandatory | Description
----- | ---- | ---- | --------- | -----------
0 | address | STRING | YES | The wallet address to query
1 | blockTag | STRING | YES | Block tag, use `"latest"` for the most recent state

> **Request Example:**

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

> **Response:**

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

**Response Fields:**

Name | Type | Description
---- | ---- | -----------
address | STRING | Wallet address
accountPrivacy | STRING | Privacy mode status: `"disabled"` or `"enabled"`
perpAssets | ARRAY | Perpetual (futures) wallet assets; only non-zero assets are listed, omitted when there are none
perpAssets[].asset | STRING | Asset name
perpAssets[].walletBalance | NUMBER | Wallet balance (JSON number; very small values may be serialized in exponent form, e.g. `1.274e-05`)
spotAssets | ARRAY | Spot wallet assets; only non-zero assets are listed, omitted when there are none
spotAssets[].asset | STRING | Asset name
spotAssets[].walletBalance | NUMBER | Wallet balance
positions | ARRAY | Position groups by trading product; omitted when the address has no open position
positions[].tradingProduct | STRING | `"perps"` (Pro mode futures) or `"shieldmode"` (Shield mode)
staking | OBJECT | Staking summary. Each amount field is `null` when it is 0. The whole object is omitted if the staking summary cannot be loaded.
staking.totalStakedAmount | STRING | Total staked ASTER (8 decimals)
staking.totalUnclaimedRewards | ARRAY | Unclaimed rewards, `null` when 0
staking.totalUnclaimedRewards[].asset | STRING | Reward asset (currently `ASTER`)
staking.totalUnclaimedRewards[].amount | STRING | Unclaimed reward amount (8 decimals)
staking.totalPendingStakeAmount | STRING | Total pending stake (8 decimals)
staking.totalPendingUnstakeAmount | STRING | Total pending unstake (8 decimals)

**Position fields when `tradingProduct` is `"perps"`:**

Name | Type | Description
---- | ---- | -----------
id | STRING | Position ID, `{userId}_{symbol}_{positionSide}`
symbol | STRING | Trading pair symbol
positionAmount | STRING | Position size (negative for short in one-way mode)
positionSide | STRING | Position side: `BOTH`, `LONG`, or `SHORT`
notionalValue | STRING | Position notional value
unrealizedProfit | STRING | Unrealized profit/loss
cumRealized | STRING | Cumulative realized profit/loss of the position

**Position fields when `tradingProduct` is `"shieldmode"`:**

Name | Type | Description
---- | ---- | -----------
positionId | STRING | Position ID
symbol | STRING | Trading pair symbol
isLong | BOOLEAN | `true` for long, `false` for short
leverage | INT | Leverage
marginAsset | STRING | Margin asset
margin | STRING | Margin
entryPrice | STRING | Entry price
liqPrice | STRING | Liquidation price
qty | STRING | Position size
tp | STRING | Take-profit price
sl | STRING | Stop-loss price
cumFundingFee | STRING | Cumulative funding fee
pnl2usdt | STRING | Unrealized PnL in USDT
pnlPercentage | STRING | Unrealized PnL percentage
createTime | STRING | Open time in milliseconds
feeMode | STRING | Fee mode
openChainHash | STRING | On-chain hash of the opening transaction

> **Note:** When account privacy is enabled, `result` contains only `address` and `accountPrivacy` (`"enabled"`); assets, positions and staking are not returned.

## Get Open Orders

``
POST /info
``

Query futures open orders for a given address.

> **Note:** Only open orders created at or after block 1 genesis time (`1772678119418`) are returned. Orders are sorted by creation time, newest first; at most the latest **1000** orders are returned.

**Method:** `aster_openOrders`

**Weight:**
1

**Parameters (params array):**

Index | Name | Type | Mandatory | Description
----- | ---- | ---- | --------- | -----------
0 | address | STRING | YES | The wallet address to query
1 | symbol | STRING | NO | Trading pair symbol (e.g. `"BTCUSDT"`); pass `null` or `""` to query all symbols. A symbol that does not exist returns error `-32603`.
2 | blockTag | STRING | YES | Block tag, use `"latest"` for the most recent state

> **Request Example:**

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

> **Response:**

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

**Response Fields:**

Name | Type | Description
---- | ---- | -----------
address | STRING | Wallet address
accountPrivacy | STRING | Privacy mode status: `"disabled"` or `"enabled"`
openOrders | ARRAY | List of open orders; omitted when there are none
openOrders[].orderId | STRING | Client order ID
openOrders[].symbol | STRING | Trading pair symbol
openOrders[].side | STRING | Order side: `BUY` or `SELL`
openOrders[].type | STRING | Order type, e.g. `LIMIT`, `STOP`, `TAKE_PROFIT`, `STOP_MARKET`, `TAKE_PROFIT_MARKET`
openOrders[].origQty | STRING | Original order quantity
openOrders[].price | STRING | Order price for `LIMIT`, `STOP` and `TAKE_PROFIT` orders; the literal string `"market"` for all other types


## Get User Futures Fills

``
POST /info
``

Query the trade fill history for a given address within a specified time range.

**Method:** `aster_userFills`

**Weight:**
1

**Parameters (params array):**

Index | Name | Type | Mandatory | Description
----- | ---- | ---- | --------- | -----------
0 | address | STRING | YES | The wallet address to query
1 | symbol | STRING | NO | Trading pair symbol (e.g. `"BTCUSDT"`); pass `null` or `""` to query all symbols
2 | from | LONG | NO | Start time in milliseconds. If omitted and `to` is provided, defaults to `to - 7 days`. If both are omitted, defaults to 7 days before current time. If `from` is earlier than `1772678119418` (block 1 genesis) it is raised to `1772678119418`, and the returned `startTime` shows the adjusted value.
3 | to | LONG | NO | End time in milliseconds. If omitted and `from` is provided, defaults to `from + 7 days`. If both are omitted, defaults to current time. `to - from` must not exceed 7 days (`604800000` ms), otherwise error `-32603` is returned. If `to` is at or before `1772678119418`, the result contains only `address` and `accountPrivacy`.
4 | blockTag | STRING | YES | Block tag, use `"latest"` for the most recent state

> **Request Example:**

```shell
curl -X POST "https://tapi.asterdex.com/info" \
  -H "accept: */*" \
  -H "Content-Type: application/json" \
  -d '{
    "id": {},
    "jsonrpc": "2.0",
    "method": "aster_userFills",
    "params": [
      "0x87EC27*********************",
      null,
      null,
      null,
      "latest"
    ]
  }'
```

> **Response:**

```javascript
{
  "result": {
    "address": "0x87EC27*********************",
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

**Response Fields:**

Name | Type | Description
---- | ---- | -----------
address | STRING | Wallet address
accountPrivacy | STRING | Privacy mode status: `"disabled"` or `"enabled"`
startTime | LONG | Actual query start time in milliseconds
endTime | LONG | Actual query end time in milliseconds
fills | ARRAY | Trade fills in the time range, sorted by time, newest first; at most the latest `1000` records. Omitted when there are none.
fills[].symbol | STRING | Trading pair symbol
fills[].side | STRING | Trade side: `BUY` or `SELL`
fills[].price | STRING | Fill price
fills[].qty | STRING | Fill quantity
fills[].time | LONG | Fill time in milliseconds

> **Note:** This endpoint only returns futures trade fill data.


## Get Spot Open Orders

``
POST /info
``

Query spot open orders for a given address.

> **Note:** Only open orders created at or after block 1 genesis time (`1772678119418`) are returned. Orders are sorted by creation time, newest first; at most the latest **1000** orders are returned.

**Method:** `aster_spotOpenOrders`

**Weight:**
1

**Parameters (params array):**

Index | Name | Type | Mandatory | Description
----- | ---- | ---- | --------- | -----------
0 | address | STRING | YES | The wallet address to query
1 | symbol | STRING | NO | Trading pair symbol (e.g. `"ASTCUSDT"`); pass `null` or `""` to query all symbols. A symbol that does not exist returns an empty result.
2 | blockTag | STRING | YES | Block tag, use `"latest"` for the most recent state

> **Request Example:**

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

> **Response:**

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

**Response Fields:**

Name | Type | Description
---- | ---- | -----------
address | STRING | Wallet address
accountPrivacy | STRING | Privacy mode status: `"disabled"` or `"enabled"`
openOrders | ARRAY | List of open orders; omitted when there are none
openOrders[].orderId | STRING | Client order ID
openOrders[].symbol | STRING | Trading pair symbol
openOrders[].side | STRING | Order side: `BUY` or `SELL`
openOrders[].type | STRING | Order type, e.g. `LIMIT`, `STOP`, `TAKE_PROFIT`, `STOP_MARKET`, `TAKE_PROFIT_MARKET`
openOrders[].origQty | STRING | Original order quantity
openOrders[].price | STRING | Order price for `LIMIT`, `STOP` and `TAKE_PROFIT` orders; the literal string `"market"` for all other types


## Get User Spot Fills

``
POST /info
``

Query the spot trade fill history for a given address within a specified time range.

**Method:** `aster_spotUserFills`

**Weight:**
1

**Parameters (params array):**

Index | Name | Type | Mandatory | Description
----- | ---- | ---- | --------- | -----------
0 | address | STRING | YES | The wallet address to query
1 | symbol | STRING | NO | Trading pair symbol (e.g. `"ASTCUSDT"`); pass `null` or `""` to query all symbols
2 | from | LONG | NO | Start time in milliseconds. If omitted and `to` is provided, defaults to `to - 7 days`. If both are omitted, defaults to 7 days before current time. If `from` is earlier than `1772678119418` (block 1 genesis) it is raised to `1772678119418`, and the returned `startTime` shows the adjusted value.
3 | to | LONG | NO | End time in milliseconds. If omitted and `from` is provided, defaults to `from + 7 days`. If both are omitted, defaults to current time. `to - from` must not exceed 7 days (`604800000` ms), otherwise error `-32603` is returned. If `to` is at or before `1772678119418`, the result contains only `address` and `accountPrivacy`.
4 | blockTag | STRING | YES | Block tag, use `"latest"` for the most recent state

> **Request Example:**

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

> **Response:**

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

**Response Fields:**

Name | Type | Description
---- | ---- | -----------
address | STRING | Wallet address
accountPrivacy | STRING | Privacy mode status: `"disabled"` or `"enabled"`
startTime | LONG | Actual query start time in milliseconds
endTime | LONG | Actual query end time in milliseconds
fills | ARRAY | Trade fills in the time range, sorted by time, newest first; at most the latest `1000` records. Omitted when there are none.
fills[].symbol | STRING | Trading pair symbol
fills[].side | STRING | Trade side: `BUY` or `SELL`
fills[].price | STRING | Fill price
fills[].qty | STRING | Fill quantity
fills[].time | LONG | Fill time in milliseconds

> **Note:** This endpoint only returns spot trade fill data.
