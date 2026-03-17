- [General Info](#general-info)
  - [General API Information](#general-api-information)
- [Chain RPC Endpoints](#chain-rpc-endpoints)
  - [Get Balance](#get-balance)
  - [Get Open Orders](#get-open-orders)
  - [Get User Fills](#get-user-fills)

# General Info

## General API Information

* All endpoints use JSON-RPC 2.0 protocol via HTTP POST.
* The base endpoint is: **https://tapi.asterdex.com/info**
* All requests must set `Content-Type: application/json`.
* The `blockTag` parameter accepts `"latest"` to query the most recent state.
* All time-related fields are in milliseconds.

> **Note:** The following endpoints only return data when the user has **privacy mode disabled**. If privacy mode is enabled, no data will be returned.

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

**Response Fields:**

Name | Type | Description
---- | ---- | -----------
address | STRING | Wallet address
accountPrivy | STRING | Privacy mode status: `"disabled"` or `"enabled"`
perpAssets | ARRAY | List of perpetual assets and balances
perpAssets[].asset | STRING | Asset name
perpAssets[].walletBalance | DECIMAL | Wallet balance
positions | ARRAY | List of position groups by trading product
positions[].tradingProduct | STRING | Trading product type (e.g. `"perps"`)
positions[].positions[].id | STRING | Position ID
positions[].positions[].symbol | STRING | Trading pair symbol
positions[].positions[].collateral | STRING | Collateral asset
positions[].positions[].positionAmount | STRING | Position size
positions[].positions[].entryPrice | STRING | Average entry price
positions[].positions[].unrealizedProfit | STRING | Unrealized profit/loss
positions[].positions[].notionalValue | STRING | Position notional value
positions[].positions[].markPrice | STRING | Current mark price
positions[].positions[].leverage | INT | Leverage
positions[].positions[].isolated | BOOLEAN | Whether isolated margin mode
positions[].positions[].isolatedWallet | STRING | Isolated wallet balance
positions[].positions[].adl | INT | ADL quantile
positions[].positions[].positionSide | STRING | Position side: `BOTH`, `LONG`, or `SHORT`
positions[].positions[].marginValue | STRING | Margin value


## Get Open Orders

``
POST /info
``

Query all open orders for a given address.

**Method:** `aster_openOrders`

**Weight:**
1

**Parameters (params array):**

Index | Name | Type | Mandatory | Description
----- | ---- | ---- | --------- | -----------
0 | address | STRING | YES | The wallet address to query
1 | symbol | STRING | NO | Trading pair symbol (e.g. `"BTCUSDT"`); pass `""` to query all symbols
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

**Response Fields:**

Name | Type | Description
---- | ---- | -----------
address | STRING | Wallet address
accountPrivy | STRING | Privacy mode status: `"disabled"` or `"enabled"`
openOrders | ARRAY | List of open orders
openOrders[].orderId | STRING | Order ID
openOrders[].symbol | STRING | Trading pair symbol
openOrders[].side | STRING | Order side: `BUY` or `SELL`
openOrders[].type | STRING | Order type: e.g. `LIMIT`, `MARKET`
openOrders[].origQty | STRING | Original order quantity
openOrders[].status | STRING | Order status: e.g. `NEW`


## Get User Fills

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
1 | symbol | STRING | YES | Trading pair symbol (e.g. `"BTCUSDT"`)
2 | from | LONG | YES | Start time in milliseconds
3 | to | LONG | YES | End time in milliseconds
4 | limit | INT | YES | Number of records per page; max `1000` per request
5 | page | INT | YES | Page number, starting from `1`
6 | blockTag | STRING | YES | Block tag, use `"latest"` for the most recent state

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

> **Response:**

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

**Response Fields:**

Name | Type | Description
---- | ---- | -----------
address | STRING | Wallet address
accountPrivy | STRING | Privacy mode status: `"disabled"` or `"enabled"`
startTime | LONG | Query start time in milliseconds
endTime | LONG | Query end time in milliseconds
fills | ARRAY | List of trade fills
fills[].symbol | STRING | Trading pair symbol
fills[].side | STRING | Trade side: `BUY` or `SELL`
fills[].price | STRING | Fill price
fills[].qty | STRING | Fill quantity
fills[].time | LONG | Fill time in milliseconds