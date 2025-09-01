# General Info
## General API Information

* The base endpoint is: **https://sapi.asterdex.com**
* All endpoints return either a JSON object or array.
* All time and timestamp related fields are in **milliseconds**.

## API Key Setup

* Some endpoints will require an API Key. 
* Once API key is created, it is recommended to set IP restrictions on the key for security reasons.
* **Never share your API key/secret key to ANYONE.**

<aside class="warning">
If the API keys were accidentally shared, please delete them immediately and create a new key.
</aside>

### Attention
* TESTUSDT or any other symbols starting with TEST are symbols used for Aster’s INTERNAL TESTING ONLY. Please DO NOT trade on these symbols starting with TEST. Aster does not hold any accountability for loss of funds due to trading on these symbols. However, if you run into issues, you may contact support about this any time, we will try to help you recover your funds.



### HTTP Return Codes
* HTTP `4XX` return codes are used for malformed requests;
  the issue is on the sender's side.
* HTTP `403` return code is used when the WAF Limit (Web Application Firewall) has been violated.
* HTTP `429` return code is used when breaking a request rate limit.
* HTTP `418` return code is used when an IP has been auto-banned for continuing to send requests after receiving `429` codes.
* HTTP `5XX` return codes are used for internal errors; the issue is on Aster's side.
  It is important to **NOT** treat this as a failure operation; the execution status is
  **UNKNOWN** and could have been a success.

### Error Codes and Messages

* If there is an error, the API will return an error with a message of the reason.

> The error payload on API is as follows:
 
```javascript
{
  "code": -1121,
  "msg": "Invalid symbol."
}
```

### General Information on Endpoints

* For `GET` endpoints, parameters must be sent as a `query string`.
* For `POST`, `PUT`, and `DELETE` endpoints, the parameters may be sent as a
  `query string` or in the `request body` with content type
  `application/x-www-form-urlencoded`.
* Parameters may be sent in any order.

---
## LIMITS

### General Info on Limits
* The `/api/v1/exchangeInfo` `rateLimits` array contains objects related to the exchange's `REQUEST_WEIGHT`, and `ORDERS` rate limits. These are further defined in the `ENUM definitions` section under `Rate limiters (rateLimitType)`.
* A 429 will be returned when either rate limit is violated.

### IP Limits
* Every request will contain `X-MBX-USED-WEIGHT-(intervalNum)(intervalLetter)` in the response headers which has the current used weight for the IP for all request rate limiters defined.
* Each route has a `weight` which determines for the number of requests each endpoint counts for. Heavier endpoints and endpoints that do operations on multiple symbols will have a heavier `weight`.
* When a 429 is received, it's your obligation as an API to back off and not spam the API.
* **Repeatedly violating rate limits and/or failing to back off after receiving 429s will result in an automated IP ban (HTTP status 418).**
* IP bans are tracked and **scale in duration** for repeat offenders, **from 2 minutes to 3 days**.
* A `Retry-After` header is sent with a 418 or 429 responses and will give the **number of seconds** required to wait, in the case of a 429, to prevent a ban, or, in the case of a 418, until the ban is over.
* **The limits on the API are based on the IPs, not the API keys.**

<aside class="notice">
We recommend using the websocket for getting data as much as possible, as this will not count to the request rate limit.
</aside>

### Order Rate Limits
* Every successful order response will contain a `X-MBX-ORDER-COUNT-(intervalNum)(intervalLetter)` header which has the current order count for the account for all order rate limiters defined.
* Rejected/unsuccessful orders are not guaranteed to have `X-MBX-ORDER-COUNT-**` headers in the response.
* **The order rate limit is counted against each account**.

### Websocket Limits
* WebSocket connections have a limit of 5 incoming messages per second. A message is considered:
    * A PING frame
    * A PONG frame
    * A JSON controlled message (e.g. subscribe, unsubscribe)
* A connection that goes beyond the limit will be disconnected; IPs that are repeatedly disconnected may be banned.
* A single connection can listen to a maximum of 1024 streams.

---

## Endpoint security type
* Each endpoint has a security type that determines how you will
  interact with it. This is stated next to the NAME of the endpoint.
    * If no security type is stated, assume the security type is NONE.
* API-keys are passed into the Rest API via the `X-MBX-APIKEY`
  header.
* API-keys and secret-keys **are case sensitive**.
* API-keys can be configured to only access certain types of secure endpoints.
* By default, API-keys can access all secure routes.

Security Type | Description
------------ | ------------
NONE | Endpoint can be accessed freely.
TRADE | Endpoint requires sending a valid API-Key and signature.
USER_DATA | Endpoint requires sending a valid API-Key and signature.
USER_STREAM | Endpoint requires sending a valid API-Key.
MARKET_DATA | Endpoint requires sending a valid API-Key.

* `TRADE` and `USER_DATA` endpoints are `SIGNED` endpoints.

## SIGNED (TRADE AND USER_DATA) Endpoint security
* `SIGNED` endpoints require an additional parameter, `signature`, to be
  sent in the  `query string` or `request body`.
* Endpoints use `HMAC SHA256` signatures. The `HMAC SHA256 signature` is a keyed `HMAC SHA256` operation.
  Use your `secretKey` as the key and `totalParams` as the value for the HMAC operation.
* The `signature` is **not case sensitive**.
* `totalParams` is defined as the `query string` concatenated with the
  `request body`.

### Timing security
* A `SIGNED` endpoint also requires a parameter, `timestamp`, to be sent which
  should be the millisecond timestamp of when the request was created and sent.
* An additional parameter, `recvWindow`, may be sent to specify the number of
  milliseconds after `timestamp` the request is valid for. If `recvWindow`
  is not sent, **it defaults to 5000**.

> The logic is as follows:
```javascript
  if (timestamp < (serverTime + 1000) && (serverTime - timestamp) <= recvWindow)
  {
    // process request
  } 
  else 
  {
    // reject request
  }
```

**Serious trading is about timing.** Networks can be unstable and unreliable,
which can lead to requests taking varying amounts of time to reach the
servers. With `recvWindow`, you can specify that the request must be
processed within a certain number of milliseconds or be rejected by the
server.

<aside class="notice">
It is recommended to use a small recvWindow of 5000 or less! The max cannot go beyond 60,000!
</aside>

### SIGNED Endpoint Examples for POST /api/v1/order
Here is a step-by-step example of how to send a vaild signed payload from the
Linux command line using `echo`, `openssl`, and `curl`.

Key | Value
------------ | ------------
apiKey | 4452d7e2ed4da80b74105e02d06328c71a34488c9fdd60a5a0900d42d584b795
secretKey | fdde510a2b71fa43a43bff3e3cf7819c8c66df34633d338050f4f59664b3b313

Parameter | Value
------------ | ------------
symbol | BNBUSDT
side | BUY
type | LIMIT
timeInForce | GTC
quantity | 5
price | 1.1
recvWindow | 5000
timestamp | 1756187806000


#### Example 1: As a request body


> **Example 1**
> **HMAC SHA256 signature:**
```shell
    $ echo -n "symbol=BNBUSDT&side=BUY&type=LIMIT&timeInForce=GTC&quantity=5&price=1.1&recvWindow=5000&timestamp=1756187806000" | openssl dgst -sha256 -hmac "fdde510a2b71fa43a43bff3e3cf7819c8c66df34633d338050f4f59664b3b313"
    (stdin)= e09169bf6c02ec4b29fa1bdc3a967f92c8c6cfcde0551ba1d477b2d3cf4c51b0
```


> **curl command:**
```shell
    (HMAC SHA256)
    $ curl -H "X-MBX-APIKEY: 4452d7e2ed4da80b74105e02d06328c71a34488c9fdd60a5a0900d42d584b795" -X POST 'https://sapi.asterdex.com/api/v1/order' -d 'symbol=BNBUSDT&side=BUY&type=LIMIT&timeInForce=GTC&quantity=5&price=1.1&recvWindow=5000&timestamp=1756187806000&signature=e09169bf6c02ec4b29fa1bdc3a967f92c8c6cfcde0551ba1d477b2d3cf4c51b0'
```

* **requestBody:** 

symbol=BNBUSDT   
&side=BUY   
&type=LIMIT   
&timeInForce=GTC   
&quantity=5   
&price=1.1   
&recvWindow=5000   
&timestamp=1756187806000


#### Example 2: As a query string

> **Example 2**
> **HMAC SHA256 signature:**
```shell
     $ echo -n "symbol=BNBUSDT&side=BUY&type=LIMIT&timeInForce=GTC&quantity=5&price=1.1&recvWindow=5000&timestamp=1756187806000" | openssl dgst -sha256 -hmac "fdde510a2b71fa43a43bff3e3cf7819c8c66df34633d338050f4f59664b3b313"
    (stdin)= e09169bf6c02ec4b29fa1bdc3a967f92c8c6cfcde0551ba1d477b2d3cf4c51b0
```

> **curl command:**
```shell
    (HMAC SHA256)
   $ curl -H "X-MBX-APIKEY: 4452d7e2ed4da80b74105e02d06328c71a34488c9fdd60a5a0900d42d584b795" -X POST 'https://sapi.asterdex.com/api/v1/order?symbol=BNBUSDT&side=BUY&type=LIMIT&timeInForce=GTC&quantity=5&price=1.1&recvWindow=5000&timestamp=1756187806000&signature=e09169bf6c02ec4b29fa1bdc3a967f92c8c6cfcde0551ba1d477b2d3cf4c51b0'
```

*  **queryString:** 

symbol=BNBUSDT   
&side=BUY   
&type=LIMIT   
&timeInForce=GTC   
&quantity=5   
&price=1.1   
&recvWindow=5000   
&timestamp=1756187806000

---

## Public API Definitions
### Terminology

These terms will be used throughout the documentation, so it is recommended especially for new users to read to help their understanding of the API.

* `base asset` refers to the asset that is the `quantity` of a symbol. For the symbol BTCUSDT, BTC would be the `base asset.`
* `quote asset` refers to the asset that is the `price` of a symbol. For the symbol BTCUSDT, USDT would be the `quote asset`.

### ENUM definitions
**Symbol status (status):**

* TRADING


**Order status (status):**

Status | Description
-----------| --------------
`NEW` | The order has been accepted by the engine.
`PARTIALLY_FILLED`| A part of the order has been filled.
`FILLED` | The order has been completed.
`CANCELED` | The order has been canceled by the user.
`REJECTED`       | The order was not accepted by the engine and not processed.
`EXPIRED` | The order was canceled according to the order type's rules (e.g. LIMIT FOK orders with no fill, LIMIT IOC or MARKET orders that partially fill) or by the exchange, (e.g. orders canceled during maintenance)


**Order types (orderTypes, type):**

* LIMIT
* MARKET
* STOP
* TAKE_PROFIT
* STOP_MARKET 
* TAKE_PROFIT_MARKET

**Order Response Type (newOrderRespType):**

* ACK
* RESULT
* FULL

**Order side (side):**

* BUY
* SELL

**Time in force (timeInForce):**

This sets how long an order will be active before expiration.

Status | Description
-----------| --------------
`GTC` | Good Till Canceled <br> An order will be on the book unless the order is canceled. 
`IOC` | Immediate Or Cancel <br> An order will try to fill the order as much as it can before the order expires.
`FOK`| Fill or Kill <br> An order will expire if the full order cannot be filled upon execution.
`GTX`| Good Till Crossing <br>  Post only order

**Kline/Candlestick chart intervals:**

m -> minutes; h -> hours; d -> days; w -> weeks; M -> months

* 1m
* 3m
* 5m
* 15m
* 30m
* 1h
* 2h
* 4h
* 6h
* 8h
* 12h
* 1d
* 3d
* 1w
* 1M

**Rate limiters (rateLimitType)**

> REQUEST_WEIGHT
```json
    {
      "rateLimitType": "REQUEST_WEIGHT",
      "interval": "MINUTE",
      "intervalNum": 1,
      "limit": 1200
    }
```

> ORDERS
```json
    {
      "rateLimitType": "ORDERS",
      "interval": "MINUTE",
      "intervalNum": 1,
      "limit": 100
    }
```

* REQUEST_WEIGHT

* ORDERS

**Rate limit intervals (interval)**

* MINUTE

---
## Filters
Filters define trading rules on a symbol or an exchange.
Filters come in two forms: `symbol filters` and `exchange filters`. Currently only `symbol filters` is used.

### Symbol Filters

#### PRICE_FILTER

> **ExchangeInfo format:**
```javascript    
  {                     
	"minPrice": "556.72",
    "maxPrice": "4529764",
    "filterType": "PRICE_FILTER",
    "tickSize": "0.01"   
  }  
```

The `PRICE_FILTER` defines the `price` rules for a symbol. There are 3 parts:

* `minPrice` defines the minimum `price`/`stopPrice` allowed; disabled on `minPrice` == 0.
* `maxPrice` defines the maximum `price`/`stopPrice` allowed; disabled on `maxPrice` == 0.
* `tickSize` defines the intervals that a `price`/`stopPrice` can be increased/decreased by; disabled on `tickSize` == 0.

Any of the above variables can be set to 0, which disables that rule in the `price filter`. In order to pass the `price filter`, the following must be true for `price`/`stopPrice` of the enabled rules:

* `price` >= `minPrice` 
* `price` <= `maxPrice`
* (`price`-`minPrice`) % `tickSize` == 0


#### PERCENT_PRICE

> **ExchangeInfo format:**
```javascript    
  {                    
	"multiplierDown": "0.9500",
	"multiplierUp": "1.0500",
	"multiplierDecimal": "4",
	"filterType": "PERCENT_PRICE"
  }  
```

The `PERCENT_PRICE` filter defines valid range for a price based on the index price.

In order to pass the `percent price`, the following must be true for `price`:  

* `price` <=`indexPrice` *`multiplierUp`
* `price`> =`indexPrice` *`multiplierDown`    


#### LOT_SIZE

> **ExchangeInfo format:**
```javascript    
  {
    "stepSize": "0.00100000",
    "filterType": "LOT_SIZE",
    "maxQty": "100000.00000000",
    "minQty": "0.00100000"
  }  
```

The `LOT_SIZE` filter defines the `quantity` (aka "lots" in auction terms) rules for a symbol. There are 3 parts:

* `minQty` defines the minimum `quantity` allowed.
* `maxQty` defines the maximum `quantity` allowed.
* `stepSize` defines the intervals that a `quantity` can be increased/decreased by.

In order to pass the `lot size`, the following must be true for `quantity`:

* `quantity` >= `minQty`
* `quantity` <= `maxQty`
* (`quantity`-`minQty`) % `stepSize` == 0




#### MARKET_LOT_SIZE

> **ExchangeInfo format:**
```javascript
  {      
	"stepSize": "0.00100000",
  "filterType": "MARKET_LOT_SIZE"
	"maxQty": "100000.00000000",
	"minQty": "0.00100000"    
  }
```


The `MARKET_LOT_SIZE` filter defines the `quantity` (aka "lots" in auction terms) rules for `MARKET` orders on a symbol. There are 3 parts:

* `minQty` defines the minimum `quantity` allowed.
* `maxQty` defines the maximum `quantity` allowed.
* `stepSize` defines the intervals that a `quantity` can be increased/decreased by.

In order to pass the `market lot size`, the following must be true for `quantity`:

* `quantity` >= `minQty`
* `quantity` <= `maxQty`
* (`quantity`-`minQty`) % `stepSize` == 0












# Market Data Endpoints

## Test Connectivity



> **Response:**
```javascript
{}
```

``
GET /api/v1/ping
``

Test connectivity to the Rest API.

**Weight:**
1

**Parameters:**

NONE

## Check Server Time


> **Response:**
```javascript
{
  "serverTime": 1499827319559
}
```

``
GET /api/v1/time
``

Test connectivity to the Rest API and get the current server time.

**Weight:**
1

**Parameters:**

NONE


## Exchange Information

> **Response:** 

```javascript  
{
	"timezone": "UTC",
	"serverTime": 1756197279679,
	"rateLimits": [{
			"rateLimitType": "REQUEST_WEIGHT",
			"interval": "MINUTE",
			"intervalNum": 1,
			"limit": 6000
		},
		{
			"rateLimitType": "ORDERS",
			"interval": "MINUTE",
			"intervalNum": 1,
			"limit": 6000
		},
		{
			"rateLimitType": "ORDERS",
			"interval": "SECOND",
			"intervalNum": 10,
			"limit": 300
		}
	],
	"exchangeFilters": [],
	"assets": [{
			"asset": "USD"
		}, {
			"asset": "USDT"
		},
		{
			"asset": "BNB"
		}
	],
	"symbols": [{
		"status": "TRADING",
		"baseAsset": "BNB",
		"quoteAsset": "USDT",
		"pricePrecision": 8,
		"quantityPrecision": 8,
		"baseAssetPrecision": 8,
		"quotePrecision": 8,
		"filters": [{
				"minPrice": "0.01000000",
				"maxPrice": "100000",
				"filterType": "PRICE_FILTER",
				"tickSize": "0.01000000"
			},
			{
				"stepSize": "0.00100000",
				"filterType": "LOT_SIZE",
				"maxQty": "1000",
				"minQty": "1"
			},
			{
				"stepSize": "0.00100000",
				"filterType": "MARKET_LOT_SIZE",
				"maxQty": "900000",
				"minQty": "0.00100000"
			},
			{
				"limit": 200,
				"filterType": "MAX_NUM_ORDERS"
			},
			{
				"minNotional": "5",
				"filterType": "MIN_NOTIONAL"
			},
			{
				"maxNotional": "100",
				"filterType": "MAX_NOTIONAL"
			},
			{
				"maxNotional": "100",
				"minNotional": "5",
				"avgPriceMins": 5,
				"applyMinToMarket": true,
				"filterType": "NOTIONAL",
				"applyMaxToMarket": true
			},
			{
				"multiplierDown": "0",
				"multiplierUp": "5",
				"multiplierDecimal": "0",
				"filterType": "PERCENT_PRICE"
			},
			{
				"bidMultiplierUp": "5",
				"askMultiplierUp": "5",
				"bidMultiplierDown": "0",
				"avgPriceMins": 5,
				"multiplierDecimal": "0",
				"filterType": "PERCENT_PRICE_BY_SIDE",
				"askMultiplierDown": "0"
			}
		],
		"orderTypes": [
			"LIMIT",
			"MARKET",
			"STOP",
			"STOP_MARKET",
			"TAKE_PROFIT",
			"TAKE_PROFIT_MARKET"
		],
		"timeInForce": [
			"GTC",
			"IOC",
			"FOK",
			"GTX"
		],
		"symbol": "BNBUSDT",
		"ocoAllowed": false
	}]
}
```

``
GET /api/v1/exchangeInfo
``

Current exchange trading rules and symbol information

**Weight:**
1

**Parameters:**
NONE


## Order Book


> **Response:**
```javascript
{
  "lastUpdateId": 1027024,
  "E": 1589436922972,   // Message output time
  "T": 1589436922959,   // Transaction time
  "bids": [
    [
      "4.00000000",     // PRICE
      "431.00000000"    // QTY
    ]
  ],
  "asks": [
    [
      "4.00000200",
      "12.00000000"
    ]
  ]
}
```

``
GET /api/v1/depth
``

**Weight(IP):**

Adjusted based on the limit:


Limit | Weight
------------ | ------------ 
5, 10, 20, 50 | 2
100 | 5
500 | 10
1000 | 20
   
**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
limit | INT | NO | Default 100. Valid limits:[5, 10, 20, 50, 100, 500, 1000]


## Recent Trades List


> **Response:**
```javascript
[
 {
    "id": 657,
    "price": "1.01000000",
    "qty": "5.00000000",
    "baseQty": "4.95049505",
    "time": 1755156533943,
    "isBuyerMaker": false
  }
]
```

``
GET /api/v1/trades
``

Get recent trades.

**Weight:**
1

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
limit | INT | NO | Default 500；max 1000


## Old Trade Lookup (MARKET_DATA)

> **Response:**

```javascript
[
 {
    "id": 1140,
    "price": "1.10000000",
    "qty": "7.27200000",
    "baseQty": "6.61090909",
    "time": 1756094288700,
    "isBuyerMaker": false
 }
]
```

``
GET /api/v1/historicalTrades
``

Get older market trades.

**Weight:**
20

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
limit | INT | NO | Default 500; max 1000.
fromId | LONG | NO | Trade id to fetch from. Default gets most recent trades.


## Compressed/Aggregate Trades List


> **Response:**
```javascript
[
  {
    "a": 26129,         // Aggregate tradeId
    "p": "0.01633102",  // Price
    "q": "4.70443515",  // Quantity
    "f": 27781,         // First tradeId
    "l": 27781,         // Last tradeId
    "T": 1498793709153, // Timestamp
    "m": true,          // Was the buyer the maker?
  }
]
```

``
GET /api/v1/aggTrades
``

Get compressed, aggregate trades. Trades that fill at the time, from the same
order, with the same price will have the quantity aggregated.

**Weight:**
20

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
fromId | LONG | NO | id to get aggregate trades from INCLUSIVE.
startTime | LONG | NO | Timestamp in ms to get aggregate trades from INCLUSIVE.
endTime | LONG | NO | Timestamp in ms to get aggregate trades until INCLUSIVE.
limit | INT | NO | Default 500; max 1000.

* If startTime and endTime are sent, time between startTime and endTime must be less than 1 hour.
* If fromId, startTime, and endTime are not sent, the most recent aggregate trades will be returned.


## Kline/Candlestick Data


> **Response:**
```javascript
[
  [
    1499040000000,      // Open time
    "0.01634790",       // Open
    "0.80000000",       // High
    "0.01575800",       // Low
    "0.01577100",       // Close
    "148976.11427815",  // Volume
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "17928899.62484339" // Ignore.
  ]
]
```

``
GET /api/v1/klines
``

Kline/candlestick bars for a symbol.   
Klines are uniquely identified by their open time.


**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
interval | ENUM | YES |
startTime | LONG | NO |
endTime | LONG | NO |
limit | INT | NO | Default 500; max 1500.

* If startTime and endTime are not sent, the most recent klines are returned.


## 24hr Ticker Price Change Statistics

> **Response:**

```javascript 
{
  "symbol": "BTCUSDT",
  "priceChange": "-94.99999800",    //price change
  "priceChangePercent": "-95.960",  //price change percent
  "weightedAvgPrice": "0.29628482", //weighted avgPrice
  "prevClosePrice": "3.89000000",   //prev close price
  "lastPrice": "4.00000200",        //last price
  "lastQty": "200.00000000",        //last qty
  "bidPrice": "866.66000000",       //first bid price
  "bidQty": "72.05100000",          //first bid qty
  "askPrice": "866.73000000",       //first ask price
  "askQty": "1.21700000",           //first ask qty
  "openPrice": "99.00000000",       //open price
  "highPrice": "100.00000000",      //high price
  "lowPrice": "0.10000000",         //low price
  "volume": "8913.30000000",        //volume
  "quoteVolume": "15.30000000",     //quote volume
  "openTime": 1499783499040,        //open time
  "closeTime": 1499869899040,       //close time
  "firstId": 28385,   // first id
  "lastId": 28460,    // last id
  "count": 76         // count
}
```

``
GET /api/v1/ticker/24hr
``

24 hour rolling window price change statistics. 
**Careful** when accessing this with no symbol.

**Weight:**

1 for a single symbol;    
**40** when the symbol parameter is omitted;

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
symbol | STRING | NO |

* If the symbol is not sent, tickers for all symbols will be returned in an array.   


## 最新价格

> **Response**

```javascript    
{
   "symbol": "ADAUSDT",
   "price": "1.30000000",
   "time": 1649666690902
}  
```

> OR

```javascript
[     
  {
     "symbol": "ADAUSDT",
     "price": "1.30000000",
     "time": 1649666690902
  }
]
```

``
GET /api/v1/ticker/price
``  

Latest price for a symbol or symbols.

**Weight:**
1 for a single symbol;
2 when the symbol parameter is omitted

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
symbol | STRING | NO |

* If the symbol is not sent, prices for all symbols will be returned in an array.


## Symbol Order Book Ticker     

> **Response** 
```javascript
{
  "symbol": "LTCBTC",
  "bidPrice": "4.00000000",
  "bidQty": "431.00000000",
  "askPrice": "4.00000200",
  "askQty": "9.00000000"
  "time": 1589437530011   
}
```

> OR

```javascript
[
  {
    "symbol": "LTCBTC",
    "bidPrice": "4.00000000",
    "bidQty": "431.00000000",
    "askPrice": "4.00000200",
    "askQty": "9.00000000",
    "time": 1589437530011  
  }
]
```

``
GET /api/v1/ticker/bookTicker
``  

Best price/qty on the order book for a symbol or symbols.

**Weight:**
1 for a single symbol;
2 when the symbol parameter is omitted

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
symbol | STRING | NO |

* If the symbol is not sent, prices for all symbols will be returned in an array.


## Symbol Commmission Fee

> **Response:**

```javascript
{
   "symbol": "APXUSDT",
   "makerCommission": "0.000200",    
   "takerCommission": "0.000700"
}
```

``
GET /api/v1/commissionRate
``

Get symbol commission fee.

**Weight:**
20

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
symbol | STRING | YES | 
recvWindow | LONG | NO |
timestamp | LONG | YES |




# Spot Account/Trade

## New Order (TRADE)

> **Response:**
```javascript 
{
  "symbol": "BTCUSDT", 
  "orderId": 28, 
  "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP", 
  "updateTime": 1507725176595, 
  "price": "0.00000000", 
  "avgPrice": "0.0000000000000000", 
  "origQty": "10.00000000", 
  "cumQty": "0",          
  "executedQty": "10.00000000", 
  "cumQuote": "10.00000000",
  "status": "FILLED",
  "timeInForce": "GTC", 
  "stopPrice": "0",    
  "origType": "LIMIT",  
  "type": "LIMIT", 
  "side": "SELL", 
}
```

``
POST /api/v1/order (HMAC SHA256)
``

Send in a new order.

**Weight:**
1

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
side | ENUM | YES |
type | ENUM | YES |
timeInForce | ENUM | NO |
quantity | DECIMAL | NO |
quoteOrderQty|DECIMAL|NO|
price | DECIMAL | NO |
newClientOrderId | STRING | NO | A unique id among open orders. Automatically generated if not sent.
stopPrice | DECIMAL | NO | Used with `STOP`, `STOP_MARKET`,`TAKE_PROFIT`, `TAKE_PROFIT_MARKET` orders.
recvWindow | LONG | NO |The value cannot be greater than ```60000```
timestamp | LONG | YES |

Additional mandatory parameters based on `type`:

Type | Additional mandatory parameters
------------ | ------------ 
`LIMIT` | `timeInForce`, `quantity`, `price`
`MARKET` | `quantity` or `quoteOrderQty`
`STOP`和`TAKE_PROFIT` | `quantity`,  `price`, `stopPrice`  
`STOP_MARKET`和`TAKE_PROFIT_MARKET` | `quantity`, `stopPrice`


Other info:

* `MARKET` `SELL` orders using the `quantity` field specifies the amount of the `base asset` the user wants to sell at the market price.
 * For example, sending a `MARKET` `SELL` order on BTCUSDT will specify how much BTC the user is selling.
* `MARKET` `BUY` orders using `quoteOrderQty` specifies the amount the user wants to spend the `quote` asset; the correct `quantity` will be determined based on the market liquidity and `quoteOrderQty`.
 * For example, sending a `MARKET` `BUY` order on BTCUSDT specify how much USDT the user is using to buy. The order will buy as many BTC as `quoteOrderQty` USDT can.
* `MARKET` orders using `quoteOrderQty` will not break `LOT_SIZE` filter rules; the order will execute a `quantity` that will have the notional value as close as possible to `quoteOrderQty`.
* same `newClientOrderId` can be accepted only when the previous one is filled, otherwise the order will be rejected.
   

## Cancel Order (TRADE)

> **Response:**
```javascript 
{
  "symbol": "BTCUSDT", 
  "orderId": 28, 
  "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP", 
  "updateTime": 1507725176595, 
  "price": "0.00000000", 
  "avgPrice": "0.0000000000000000", 
  "origQty": "10.00000000", 
  "cumQty": "0",            
  "executedQty": "10.00000000", 
  "cumQuote": "10.00000000", 
  "status": "CANCELED", 
  "timeInForce": "GTC", 
  "stopPrice": "0",    
  "origType": "LIMIT",  
  "type": "LIMIT", 
  "side": "SELL",
}
```

``
DELETE /api/v1/order (HMAC SHA256)
``

Cancel an active order.

**Weight:**
1

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
orderId | LONG | NO |
origClientOrderId | STRING | NO |
recvWindow | LONG | NO |
timestamp | LONG | YES |

Either `orderId` or `origClientOrderId` must be sent.  


## Query Order (USER_DATA)

> **Response:**

```javascript 
{
    "orderId": 38,
    "symbol": "ADA25SLP25",
    "status": "FILLED",
    "clientOrderId": "afMd4GBQyHkHpGWdiy34Li",
    "price": "20",
    "avgPrice": "12.0000000000000000",
    "origQty": "10",
    "executedQty": "10",
    "cumQuote": "120",
    "timeInForce": "GTC",
    "type": "LIMIT",
    "side": "BUY",
    "stopPrice": "0",
    "origType": "LIMIT",
    "time": 1649913186270,
    "updateTime": 1649913186297
} 
```

``
GET /api/v1/order (HMAC SHA256)
``

Check an order's status.  

**Weight:**
1

* These orders will not be found:
	* order status is `CANCELED` or `EXPIRED`, **AND** 
	* order has NO filled trade, **AND**
	* created time + 7 days < current time  

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
orderId | LONG | NO |
origClientOrderId | STRING | NO |
recvWindow | LONG | NO | 
timestamp | LONG | YES |

Notes:

* Either `orderId` or `origClientOrderId` must be sent.


## current one opne order (USER_DATA)

> **Response:**
```javascript
{
    "orderId": 38, 
    "symbol": "ADA25SLP25", 
    "status": "NEW", 
    "clientOrderId": "afMd4GBQyHkHpGWdiy34Li", 
    "price": "20", 
    "avgPrice": "12.0000000000000000", 
    "origQty": "10", 
    "executedQty": "10", 
    "cumQuote": "120",
    "timeInForce": "GTC",
    "type": "LIMIT",
    "side": "BUY", 
    "stopPrice": "0",
    "origType": "LIMIT", 
    "time": 1649913186270, 
    "updateTime": 1649913186297 
}
```

``
GET /api/v1/openOrder (HMAC SHA256)
``

get one current  opne order

**Weight:** 
1

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
orderId | LONG | NO |
origClientOrderId | STRING | NO |
recvWindow | LONG | NO |  
timestamp | LONG | YES |

**Notes:**

Either `orderId` or `origClientOrderId` must be sent. 


## Current Open Orders (USER_DATA)

> **Response:**
```javascript 
[     
    {
        "orderId": 349661, 
        "symbol": "BNBUSDT", 
        "status": "NEW", 
        "clientOrderId": "LzypgiMwkf3TQ8wwvLo8RA", 
        "price": "1.10000000", 
        "avgPrice": "0.0000000000000000", 
        "origQty": "5",  
        "executedQty": "0", 
        "cumQuote": "0", 
        "timeInForce": "GTC",
        "type": "LIMIT", 
        "side": "BUY",   
        "stopPrice": "0", 
        "origType": "LIMIT", 
        "time": 1756252940207, 
        "updateTime": 1756252940207, 
    }
] 
```

``
GET /api/v1/openOrders (HMAC SHA256)
``

Get all open orders on a symbol. **Careful** when accessing this with no symbol.

**Weight:** 
1 for a single symbol; **40** when the symbol parameter is omitted
 
**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
symbol | STRING | NO |
recvWindow | LONG | NO | 
timestamp | LONG | YES |

* If the symbol is not sent, orders for all symbols will be returned in an array.



## cancel all open order (USER_DATA)

> **Response:**

```javascript
{
    "code": 200,
    "msg": "The operation of cancel all open order is done."
}
```

``
DEL /api/v1/allOpenOrders  (HMAC SHA256)
``

**Weight:**
- ***1***

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
orderIdList | STRING | NO | id array
origClientOrderIdList | STRING | NO | clientOrderId array
recvWindow | LONG | NO |
timestamp | LONG | YES |



## All Orders (USER_DATA)

> **Response:**

```javascript
[
    {
        "orderId": 349661, 
        "symbol": "BNBUSDT", 
        "status": "NEW", 
        "clientOrderId": "LzypgiMwkf3TQ8wwvLo8RA", 
        "price": "1.10000000", 
        "avgPrice": "0.0000000000000000", 
        "origQty": "5",  
        "executedQty": "0", 
        "cumQuote": "0", 
        "timeInForce": "GTC", 
        "type": "LIMIT", 
        "side": "BUY",   
        "stopPrice": "0", 
        "origType": "LIMIT", 
        "time": 1756252940207, 
        "updateTime": 1756252940207, 
    }
]
```

``
GET /api/v1/allOrders (HMAC SHA256)
``

Get all account orders; active, canceled, or filled.

* These orders will not be found:
	* created time + 7 days < current time

**Weight:**
5

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
orderId | LONG | NO |
startTime | LONG | NO |
endTime | LONG | NO |
limit | INT | NO | Default 500; max 1000.
recvWindow | LONG | NO | 
timestamp | LONG | YES |  

**Notes:**

* If `orderId` is set, it will get orders >= that `orderId`. Otherwise most recent orders are returned.
* The query time period must be less then 7 days( default as the recent 7 days).  ## Account Information (USER_DATA)


## Swap Between Futures and Spot (TRADE)

> **Response:**

```javascript
{
    "tranId": 21841, 
    "status": "SUCCESS" 
}
```

``
POST /api/v1/asset/transfer  (HMAC SHA256)
``

**Weight:**
5

**Parameters:**


Name | Type | Mandatory | Description
---------------- | ------- | -------- | ----
amount |	DECIMAL | 	YES |	
asset |	STRING | 	YES |	
clientTranId |	STRING | 	YES |
kindType |	STRING | 	YES |	
recvWindow | LONG | NO | 
timestamp	| LONG | YES	|

**Notes:**
* kindType FUTURE_SPOT(future to spot)/SPOT_FUTURE(spot to future)

## transfer asset to other address (TRADE)

> **Response:**

```javascript
{
    "tranId": 21841, 
    "status": "SUCCESS" 
}
```

``
POST /api/v1/asset/sendToAddress  (HMAC SHA256)
``

**Weight:**
5

**Parameters:**


Name | Type | Mandatory | Description
---------------- | ------- | -------- | ----
amount |	DECIMAL | 	YES |	
asset |	STRING | 	YES |	
toAddress |	STRING | 	YES |	
clientTranId |	STRING | 	NO |	 
recvWindow | LONG | NO | 
timestamp	| LONG | YES	|	

**Notes:**
* The target address must be a valid existing account and must not be the same as the sender’s account.
* The toAddress must be an EVM address.
* If clientTranId is provided, its length must be at least 20 characters.


## get withdraw fee (USER_DATA)
> **Response:**
```javascript
{
  "tokenPrice": 1.00019000,
   "gasCost": 0.5000,
  "gasUsdValue": 0.5
}
```

``
GET /api/v1/aster/withdraw/estimateFee (HMAC SHA256)
``

**Weight:**
1

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
chainId | STRING | YES | 
asset | STRING | YES | 

**Notes:**
* chainId: 1(ETH),56(BSC),42161(Arbi)
* gasCost: The minimum fee required for a withdrawal

## withdraw (USER_DATA)
> **Response:**
```javascript
{
  "withdrawId": "1014729574755487744",
  "hash":"0xa6d1e617a3f69211df276fdd8097ac8f12b6ad9c7a49ba75bbb24f002df0ebb"
}
```

``
POST /api/v1/aster/user-withdraw (HMAC SHA256)
``

**Weight:**
1

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
chainId | STRING | YES | 1(ETH),56(BSC),42161(Arbi)
asset | STRING | YES |
amount | STRING | YES |
fee | STRING | YES |
receiver | STRING | YES |  The address of the current account
nonce | STRING | YES |  The current time in microseconds 
userSignature | STRING | YES | 
recvWindow | LONG | NO | 
timestamp | LONG | YES | 


**Notes:** 
* chainId: 1(ETH),56(BSC),42161(Arbi)
* receiver: The address of the current account
* If the futures account balance is insufficient, funds will be transferred from the spot account to the futures account for the withdrawal.
* userSignature demo

```shell
const domain = {
    name: 'Aster',
    version: '1',
    chainId: 56,
    verifyingContract: ethers.ZeroAddress,
  }

const currentTime = Date.now() * 1000
 
const types = {
    Action: [
        {name: "type", type: "string"},
        {name: "destination", type: "address"},
        {name: "destination Chain", type: "string"},
        {name: "token", type: "string"},
        {name: "amount", type: "string"},
        {name: "fee", type: "string"},
        {name: "nonce", type: "uint256"},
        {name: "aster chain", type: "string"},
    ],
  }
  const value = {
    'type': 'Withdraw',
    'destination': '0xD9cA6952F1b1349d27f91E4fa6FB8ef67b89F02d',
    'destination Chain': 'BSC',
    'token': 'USDT',
    'amount': '10.123400',
    'fee': '1.234567891',
    'nonce': currentTime,
    'aster chain': 'Mainnet',
  }


const signature = await signer.signTypedData(domain, types, value)
```

## get user create apikey nonce (NONE)

> **Response:**
```javascript

111111

```

``
POST /api/v1/getNonce 
``

**Weight:**
1

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
address | STRING | YES |
userOperationType | STRING | YES | CREATE_API_KEY
network | STRING | NO | 

**Notes:**
* userOperationType : CREATE_API_KEY
* network : For the Solana network, SOL must be provided; otherwise, this field is ignored.

## create apikey (NONE)

> **Response:**
```javascript
{
    "apiKey": "bb3b24d0a3dec88cb06be58a257e4575cb0b1bb256ad6fd90ae8fd0ee1d102ae",
    "apiSecret": "9fe8f5642ae1961674ea0cb7f957fa99dc8e0421b607c985a963ad2ced90ae1c"
}
```

``
POST /api/v1/createApiKey
``

**Weight:**
1

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
address | STRING | YES |
userOperationType | STRING | YES | CREATE_API_KEY
network | STRING | NO | 
userSignature | STRING | YES | 
apikeyIP | STRING | NO | 
desc | STRING | YES | 
recvWindow | LONG | NO | 
timestamp | LONG | YES | 

**Notes:**
* userOperationType : CREATE_API_KEY
* network : For the Solana network, SOL must be provided; otherwise, this field is ignored.
* desc: The same account cannot be duplicated, and the length must not exceed 20 characters.
* apikeyIP An array of IP addresses, separated by commas.
* Rate limit: 60 requests per minute per IP
* userSignature evm demo

```shell
const nonce = 111111
const message = 'You are signing into Astherus ${nonce}';
const signature = await signer.signMessage(message);
```


## Account Information (USER_DATA)

> **Response:**
```javascript
{   
   "feeTier": 0,
   "canTrade": true,
   "canDeposit": true,
   "canWithdraw": true,
   "canBurnAsset": true,
   "updateTime": 0,   
   "balances": [
    {
      "asset": "BTC",
      "free": "4723846.89208129",
      "locked": "0.00000000"
    },
    {
      "asset": "LTC",
      "free": "4763368.68006011",
      "locked": "0.00000000"
    }
  ]
}
```

``
GET /api/v1/account (HMAC SHA256)
``

Get current account information.

**Weight:**
5

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
recvWindow | LONG | NO | 
timestamp | LONG | YES |


## Account Trade List (USER_DATA)

> **Response:**
```javascript  
[ 
  {
    "symbol": "BNBUSDT",
    "id": 1002,
    "orderId": 266358,
    "side": "BUY",
    "price": "1",
    "qty": "2",
    "quoteQty": "2",
    "commission": "0.00105000",
    "commissionAsset": "BNB",
    "time": 1755656788798,
    "counterpartyId": 19,
    "createUpdateId": null,
    "maker": false,
    "buyer": true
  }
] 
```

``
GET /api/v1/userTrades (HMAC SHA256)
``

Get trades for a specific account and symbol.

**Weight:**
5

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
symbol | STRING | NO |
orderId|LONG|NO| This can only be used in combination with `symbol`.
startTime | LONG | NO |
endTime | LONG | NO |
fromId | LONG | NO | TradeId to fetch from. Default gets most recent trades.
limit | INT | NO | Default 500; max 1000.
recvWindow | LONG | NO |
timestamp | LONG | YES |   

* If `startTime` and `endTime` are both not sent, then the last 7 days' data will be returned.
* The time between `startTime` and `endTime` cannot be longer than 7 days.
* The parameter `fromId` cannot be sent with `startTime` or `endTime`.     








---
# Websocket Market Streams

* The base endpoint is: **wss://sstream.asterdex.com**
* Streams can be accessed either in a single raw stream or in a combined stream
* Raw streams are accessed at **/ws/\<streamName\>**
* Combined streams are accessed at **/stream?streams=\<streamName1\>/\<streamName2\>/\<streamName3\>**
* Combined stream events are wrapped as follows: **{"stream":"\<streamName\>","data":\<rawPayload\>}**
* All symbols for streams are **lowercase**
* A single connection to **sstream.asterdex.com** is only valid for 24 hours; expect to be disconnected at the 24 hour mark
* The websocket server will send a `ping frame` every 3 minutes. If the websocket server does not receive a `pong frame` back from the connection within a 10 minute period, the connection will be disconnected. Unsolicited `pong frames` are allowed.

## Live Subscribing/Unsubscribing to streams

* The following data can be sent through the websocket instance in order to subscribe/unsubscribe from streams. Examples can be seen below.
* The `id` used in the JSON payloads is an unsigned INT used as an identifier to uniquely identify the messages going back and forth.
* In the response, if the `result` received is `null` this means the request sent was a success.

### Subscribe to a stream

> **Response**
  ```javascript
  {
    "result": null,  
    "id": 1
  }
  ```

* **Request**

  	{    
    	"method": "SUBSCRIBE",    
    	"params":     
    	[   
      	"btcusdt@aggTrade",    
      	"btcusdt@depth"     
    	],    
    	"id": 1   
  	}



### Unsubscribe to a stream

> **Response**
  
  ```javascript
  {
    "result": null,
    "id": 312
  }
  ```


* **Request**

  {   
    "method": "UNSUBSCRIBE",    
    "params":     
    [    
      "btcusdt@depth"   
    ],    
    "id": 312   
  }



### Listing Subscriptions

> **Response**
  
  ```javascript
  {
    "result": [
      "btcusdt@aggTrade"
    ],
    "id": 3
  }
  ```


* **Request**

  {   
    "method": "LIST_SUBSCRIPTIONS",    
    "id": 3   
  }     
 


### Setting Properties
Currently, the only property can be set is to set whether `combined` stream payloads are enabled or not.
The combined property is set to `false` when connecting using `/ws/` ("raw streams") and `true` when connecting using `/stream/`.

> **Response**
  
  ```javascript
{
  "result": null,
  "id": 5
}
  ```

* **Request**

  {    
    "method": "SET_PROPERTY",    
    "params":     
    [   
      "combined",    
      true   
    ],    
    "id": 5   
  }




### Retrieving Properties

> **Response**
  ```javascript
  {
    "result": true, // Indicates that combined is set to true.
    "id": 2
  }
  ```
  
* **Request**
  
  {   
    "method": "GET_PROPERTY",    
    "params":     
    [   
      "combined"   
    ],    
    "id": 2   
  }   
 



### Error Messages

Error Message | Description
---|---
{"code": 0, "msg": "Unknown property", "id": '%s'} | Parameter used in the `SET_PROPERTY` or `GET_PROPERTY` was invalid
{"code": 1, "msg": "Invalid value type: expected Boolean", "id": '%s'} | Value should only be `true` or `false`
{"code": 2, "msg": "Invalid request: property name must be a string"}| Property name provided was invalid
{"code": 2, "msg": "Invalid request: request ID must be an unsigned integer"}| Parameter `id` had to be provided or the value provided in the `id` parameter is an unsupported type
{"code": 2, "msg": "Invalid request: unknown variant %s, expected one of `SUBSCRIBE`, `UNSUBSCRIBE`, `LIST_SUBSCRIPTIONS`, `SET_PROPERTY`, `GET_PROPERTY` at line 1 column 28"} | Possible typo in the provided method or provided method was neither of the expected values
{"code": 2, "msg": "Invalid request: too many parameters"}| Unnecessary parameters provided in the data
{"code": 2, "msg": "Invalid request: property name must be a string"} | Property name was not provided
{"code": 2, "msg": "Invalid request: missing field `method` at line 1 column 73"} | `method` was not provided in the data
{"code":3,"msg":"Invalid JSON: expected value at line %s column %s"} | JSON data sent has incorrect syntax.


## Aggregate Trade Streams


> **Payload:**
```javascript
{
  "e": "aggTrade",  // Event type
  "E": 123456789,   // Event time
  "s": "BNBBTC",    // Symbol
  "a": 12345,       // Aggregate trade ID
  "p": "0.001",     // Price
  "q": "100",       // Quantity
  "f": 100,         // First trade ID
  "l": 105,         // Last trade ID
  "T": 123456785,   // Trade time
  "m": true,        // Is the buyer the market maker?
  "M": true         // Ignore
}
```

The Aggregate Trade Streams push trade information that is aggregated for a single taker order.

**Stream Name:** `<symbol>@aggTrade`

**Update Speed:** Real-time


## Trade Streams


> **Payload:**
```javascript
{
  "e": "trade",     // Event type
  "E": 123456789,   // Event time
  "s": "BNBBTC",    // Symbol
  "t": 12345,       // Trade ID
  "p": "0.001",     // Price
  "q": "100",       // Quantity
  "T": 123456785,   // Trade time
  "m": true,        // Is the buyer the market maker?
}
```

The Trade Streams push raw trade information; each trade has a unique buyer and seller.

**Stream Name:** `<symbol>@trade`

**Update Speed:** Real-time






## Kline/Candlestick Streams


> **Payload:**
```javascript
{
  "e": "kline",     // Event type
  "E": 123456789,   // Event time
  "s": "BNBBTC",    // Symbol
  "k": {
    "t": 123400000, // Kline start time
    "T": 123460000, // Kline close time
    "s": "BNBBTC",  // Symbol
    "i": "1m",      // Interval
    "f": 100,       // First trade ID
    "L": 200,       // Last trade ID
    "o": "0.0010",  // Open price
    "c": "0.0020",  // Close price
    "h": "0.0025",  // High price
    "l": "0.0015",  // Low price
    "v": "1000",    // Base asset volume
    "n": 100,       // Number of trades
    "x": false,     // Is this kline closed?
    "q": "1.0000",  // Quote asset volume
    "V": "500",     // Taker buy base asset volume
    "Q": "0.500",   // Taker buy quote asset volume
    "B": "123456"   // Ignore
  }
}
```

The Kline/Candlestick Stream push updates to the current klines/candlestick every second.

**Stream Name:** `<symbol>@kline_<interval>`

**Update Speed:** 2000ms

**Kline/Candlestick chart intervals:**

m -> minutes; h -> hours; d -> days; w -> weeks; M -> months

* 1m
* 3m
* 5m
* 15m
* 30m
* 1h
* 2h
* 4h
* 6h
* 8h
* 12h
* 1d
* 3d
* 1w
* 1M




## Individual Symbol Mini Ticker Stream

> **Payload:**
```javascript
  {
    "e": "24hrMiniTicker",  // Event type
    "E": 123456789,         // Event time
    "s": "BNBBTC",          // Symbol
    "c": "0.0025",          // Close price
    "o": "0.0010",          // Open price
    "h": "0.0025",          // High price
    "l": "0.0010",          // Low price
    "v": "10000",           // Total traded base asset volume
    "q": "18"               // Total traded quote asset volume
  }
```

24hr rolling window mini-ticker statistics. These are NOT the statistics of the UTC day, but a 24hr rolling window for the previous 24hrs.

**Stream Name:** `<symbol>@miniTicker`

**Update Speed:** 1000ms




## All Market Mini Tickers Stream

> **Payload:**
```javascript
[
  {
    // Same as <symbol>@miniTicker payload
  }
]
```

24hr rolling window mini-ticker statistics for all symbols that changed in an array. These are NOT the statistics of the UTC day, but a 24hr rolling window for the previous 24hrs. Note that only tickers that have changed will be present in the array.

**Stream Name:** `!miniTicker@arr`

**Update Speed:** 1000ms



## Individual Symbol Ticker Streams


> **Payload:**
```javascript
{
  "e": "24hrTicker",  // Event type
  "E": 123456789,     // Event time
  "s": "BNBBTC",      // Symbol
  "p": "0.0015",      // Price change
  "P": "250.00",      // Price change percent
  "w": "0.0018",      // Weighted average price
  "c": "0.0025",      // Last price
  "Q": "10",          // Last quantity
  "o": "0.0010",      // Open price
  "h": "0.0025",      // High price
  "l": "0.0010",      // Low price
  "v": "10000",       // Total traded base asset volume
  "q": "18",          // Total traded quote asset volume
  "O": 0,             // Statistics open time
  "C": 86400000,      // Statistics close time
  "F": 0,             // First trade ID
  "L": 18150,         // Last trade Id
  "n": 18151          // Total number of trades
}
```


24hr rolling window ticker statistics for a single symbol. These are NOT the statistics of the UTC day, but a 24hr rolling window for the previous 24hrs.

**Stream Name:** `<symbol>@ticker`

**Update Speed:** 1000ms


## All Market Tickers Stream

> **Payload:**
```javascript
[
  {
    // Same as <symbol>@ticker payload
  }
]
```

24hr rolling window ticker statistics for all symbols that changed in an array. These are NOT the statistics of the UTC day, but a 24hr rolling window for the previous 24hrs. Note that only tickers that have changed will be present in the array.

**Stream Name:** `!ticker@arr`

**Update Speed:** 1000ms





## Individual Symbol Book Ticker Streams

> **Payload:**
```javascript
{
  "u":400900217,     // order book updateId
  "s":"BNBUSDT",     // symbol
  "b":"25.35190000", // best bid price
  "B":"31.21000000", // best bid qty
  "a":"25.36520000", // best ask price
  "A":"40.66000000"  // best ask qty
}
```


Pushes any update to the best bid or ask's price or quantity in real-time for a specified symbol.

**Stream Name:** `<symbol>@bookTicker`

**Update Speed:** Real-time





## All Book Tickers Stream

> **Payload:**
```javascript
{
  // Same as <symbol>@bookTicker payload
}
```

Pushes any update to the best bid or ask's price or quantity in real-time for all symbols.

**Stream Name:** `!bookTicker`

**Update Speed:** Real-time



## Partial Book Depth Streams

> **Payload:**
```javascript
{ 
  "e": "depthUpdate", // Event type
  "E": 123456789,     // Event time
  "T": 123456788,     // Transaction time 
  "s": "BTCUSDT",     // Symbol
  "U": 100,           // First update ID in event
  "u": 120,           // Final update ID in event
  "pu": 99,          // Final update Id in last stream(ie `u` in last stream) 
  "bids": [             // Bids to be updated
    [
      "0.0024",         // Price level to be updated
      "10"              // Quantity
    ]
  ],
  "asks": [             // Asks to be updated
    [
      "0.0026",         // Price level to be updated
      "100"             // Quantity
    ]
  ]
}
```

Top **<levels\>** bids and asks, Valid **<levels\>** are 5, 10, or 20.

**Stream Names:** `<symbol>@depth<levels>` OR `<symbol>@depth<levels>@100ms`.  

**Update Speed:** 1000ms or 100ms




## Diff. Depth Stream


> **Payload:**
```javascript 
{
  "e": "depthUpdate", // Event type
  "E": 123456789,     // Event time
  "T": 123456788,     // Transaction time 
  "s": "BTCUSDT",     // Symbol
  "U": 100,           // First update ID in event
  "u": 120,           // Final update ID in event
  "pu": 99,          // Final update Id in last stream(ie `u` in last stream)
  "b": [              // Bids to be updated
    [
      "5.4",       // Price level to be updated
      "10"            // Quantity
    ]
  ],
  "a": [              // Asks to be updated
    [
      "5.6",       // Price level to be updated
      "100"          // Quantity
    ]
  ]
} 
```

Order book price and quantity depth updates used to locally manage an order book.
 
**Stream Name:** `<symbol>@depth` OR `<symbol>@depth@100ms`

**Update Speed:** 1000ms or 100ms



## How to manage a local order book correctly
1. Open a stream to **wss://sstream.asterdex.com/ws/bnbbtc@depth**.
2. Buffer the events you receive from the stream.
3. Get a depth snapshot from **https://sapi.asterdex.com/v1/depth?symbol=BNBBTC&limit=1000** .
4. Drop any event where `u` is <= `lastUpdateId` in the snapshot.
5. The first processed event should have `U` <= `lastUpdateId`+1 **AND** `u` >= `lastUpdateId`+1.
6. While listening to the stream, each new event's `U` should be equal to the previous event's `u`+1.
7. The data in each event is the **absolute** quantity for a price level.
8. If the quantity is 0, **remove** the price level.
9. Receiving an event that removes a price level that is not in your local order book can happen and is normal.






# User Data Streams


* The base API endpoint is: **https://sapi.asterdex.com**
* A User Data Stream `listenKey` is valid for 60 minutes after creation.
* Doing a `PUT` on a `listenKey` will extend its validity for 60 minutes.
* Doing a `DELETE` on a `listenKey` will close the stream and invalidate the `listenKey`.
* Doing a `POST` on an account with an active `listenKey` will return the currently active `listenKey` and extend its validity for 60 minutes.
* The base websocket endpoint is: **wss://sstream.asterdex.com**
* User Data Streams are accessed at **/ws/\<listenKey\>**
* A single connection to **sstream.asterdex.com** is only valid for 24 hours; expect to be disconnected at the 24 hour mark


## LISTEN KEY

### Create a ListenKey (USER_STREAM)

> **Response:**
```javascript
{
  "listenKey": "pqia91ma19a5s61cv6a81va65sdf19v8a65a1a5s61cv6a81va65sdf19v8a65a1"
}
```


``
POST /api/v1/listenKey
``

Start a new user data stream. The stream will close after 60 minutes unless a keepalive is sent. If the account has an active `listenKey`, that `listenKey` will be returned and its validity will be extended for 60 minutes.

**Weight:**
1

**Parameters:**
NONE

### Ping/Keep-alive a ListenKey (USER_STREAM)

> **Response:**
```javascript
{}
```

``
PUT /api/v1/listenKey 
``

Keepalive a user data stream to prevent a time out. User data streams will close after 60 minutes. It's recommended to send a ping about every 30 minutes.

**Weight:**
1

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
listenKey | STRING | YES


### Close a ListenKey (USER_STREAM)

> **Response:**
```javascript
{}
```

``
DELETE /api/v1/listenKey
``

Close out a user data stream.

**Weight:**
1

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
listenKey | STRING | YES



## Payload: Balance Update

`outboundAccountPosition` is sent any time an account balance has changed and contains the assets that were possibly changed by the event that generated the balance change.

> **Payload:**
```javascript
{
  "B":[  //Balance
    {
      "a":"SLP25",   //Asset
      "f":"10282.42029415",   //Free
      "l":"653.00000001"   //Locked
    },
    {
      "a":"ADA25",
      "f":"9916.96229880",
      "l":"34.00510000"
    }
  ],
  "e":"outboundAccountPosition",   //Event type
  "T":1649926447190,   //Time of last account update
  "E":1649926447205   //Event Time
  "m":"WITHDRAW" // Event reason type
}
```


## Payload: Order Update

Orders are updated with the `executionReport` event.

> **Payload:**   

```javascript
{
  "s":"ADA25SLP25",   // symbol
  "c":"Xzh0gnxT41PStbwqOtXnjD",  // client order id
  "S":"SELL",   // order direction
  "o":"LIMIT",   // order type
  "f":"GTC",   // Time in force
  "q":"10.001000",   // Order quantity
  "p":"19.1000000000",   // Order price
  "ap":"19.0999999955550656",  //average price
  "P":"0",  //stop price
  "x":"TRADE",   // Current execution type
  "X":"PARTIALLY_FILLED",   // Current order status
  "i":27,   // Order ID
  "l":"1",    // Last executed quantity   
  "z":"8.999000",   // Cumulative filled quantity
  "L":"19.1000000000",   // Last executed price
  "n":"0.00382000",   // Commission amount
  "N":"SLP25",   // Commission asset
  "T":1649926447190,   //Trasanction Time
  "t":18,   // transaction id
  "m":true,   // is this trade the maker side?
  "ot":"LIMIT", //original order type
  "O":0,   // Order creation time
  "Z":"171.88089996",   // Cumulative quote asset transacted quantity
  "Y":"19.1000000000000000",   // Last quote asset transacted quantity (i.e. lastPrice * lastQty)
  "Q":"0",   // Quote Order Qty
  "e":"executionReport",   // event
  "E":1649926447209  // event time
} 
```

**Execution types:**

* NEW - The order has been accepted into the engine.
* CANCELED - The order has been canceled by the user. 
* REPLACED (currently unused)
* TRADE - Part of the order or all of the order's quantity has filled.
* EXPIRED - The order was canceled according to the order type's rules (e.g. LIMIT FOK orders with no fill, LIMIT IOC or MARKET orders that partially fill) or by the exchange, (e.g. orders canceled during maintenance)



# Error Codes

> Here is the error JSON payload:

```javascript
{
"code":-1121,
"msg":"Invalid symbol."
}
```

Errors consist of two parts: an error code and a message. 
Codes are universal,but messages can vary. 




## 10xx - General Server or Network issues
### -1000 UNKNOWN
* An unknown error occured while processing the request.

### -1001 DISCONNECTED
* Internal error; unable to process your request. Please try again.

### -1002 UNAUTHORIZED
* You are not authorized to execute this request.

### -1003 TOO_MANY_REQUESTS
* Too many requests queued.
* Too many requests; please use the websocket for live updates.
* Too many requests; current limit is %s requests per minute. Please use the websocket for live updates to avoid polling the API.
* Way too many requests; IP banned until %s. Please use the websocket for live updates to avoid bans.

### -1004 DUPLICATE_IP
* This IP is already on the white list

### -1005 NO_SUCH_IP
* No such IP has been white listed

### -1006 UNEXPECTED_RESP
* An unexpected response was received from the message bus. Execution status unknown.

### -1007 TIMEOUT
* Timeout waiting for response from backend server. Send status unknown; execution status unknown.

### -1010 ERROR_MSG_RECEIVED
* ERROR_MSG_RECEIVED. 

### -1011 NON_WHITE_LIST
* This IP cannot access this route. 

### -1013 INVALID_MESSAGE
* INVALID_MESSAGE.

### -1014 UNKNOWN_ORDER_COMPOSITION
* Unsupported order combination.

### -1015 TOO_MANY_ORDERS
* Too many new orders.
* Too many new orders; current limit is %s orders per %s.

### -1016 SERVICE_SHUTTING_DOWN
* This service is no longer available.

### -1020 UNSUPPORTED_OPERATION
* This operation is not supported.

### -1021 INVALID_TIMESTAMP
* Timestamp for this request is outside of the recvWindow.
* Timestamp for this request was 1000ms ahead of the server's time.

### -1022 INVALID_SIGNATURE
* Signature for this request is not valid.

### -1023 START_TIME_GREATER_THAN_END_TIME
* Start time is greater than end time.


## 11xx - Request issues
### -1100 ILLEGAL_CHARS
* Illegal characters found in a parameter.
* Illegal characters found in parameter '%s'; legal range is '%s'.

### -1101 TOO_MANY_PARAMETERS
* Too many parameters sent for this endpoint.
* Too many parameters; expected '%s' and received '%s'.
* Duplicate values for a parameter detected.

### -1102 MANDATORY_PARAM_EMPTY_OR_MALFORMED
* A mandatory parameter was not sent, was empty/null, or malformed.
* Mandatory parameter '%s' was not sent, was empty/null, or malformed.
* Param '%s' or '%s' must be sent, but both were empty/null!

### -1103 UNKNOWN_PARAM
* An unknown parameter was sent.

### -1104 UNREAD_PARAMETERS
* Not all sent parameters were read.
* Not all sent parameters were read; read '%s' parameter(s) but was sent '%s'.

### -1105 PARAM_EMPTY
* A parameter was empty.
* Parameter '%s' was empty.

### -1106 PARAM_NOT_REQUIRED
* A parameter was sent when not required.
* Parameter '%s' sent when not required.

### -1108 BAD_ASSET
* Invalid asset.

### -1109 BAD_ACCOUNT
* Invalid account.

### -1110 BAD_INSTRUMENT_TYPE
* Invalid symbolType.

### -1111 BAD_PRECISION
* Precision is over the maximum defined for this asset.

### -1112 NO_DEPTH
* No orders on book for symbol.

### -1113 WITHDRAW_NOT_NEGATIVE
* Withdrawal amount must be negative.

### -1114 TIF_NOT_REQUIRED
* TimeInForce parameter sent when not required.

### -1115 INVALID_TIF
* Invalid timeInForce.

### -1116 INVALID_ORDER_TYPE
* Invalid orderType.

### -1117 INVALID_SIDE
* Invalid side.

### -1118 EMPTY_NEW_CL_ORD_ID
* New client order ID was empty.

### -1119 EMPTY_ORG_CL_ORD_ID
* Original client order ID was empty.

### -1120 BAD_INTERVAL
* Invalid interval.

### -1121 BAD_SYMBOL
* Invalid symbol.

### -1125 INVALID_LISTEN_KEY
* This listenKey does not exist.

### -1127 MORE_THAN_XX_HOURS
* Lookup interval is too big.
* More than %s hours between startTime and endTime.

### -1128 OPTIONAL_PARAMS_BAD_COMBO
* Combination of optional parameters invalid.

### -1130 INVALID_PARAMETER
* Invalid data sent for a parameter.
* Data sent for parameter '%s' is not valid.

### -1136 INVALID_NEW_ORDER_RESP_TYPE
* Invalid newOrderRespType.


## 20xx - Processing Issues

### -2010 NEW_ORDER_REJECTED
* NEW_ORDER_REJECTED

### -2011 CANCEL_REJECTED
* CANCEL_REJECTED

### -2013 NO_SUCH_ORDER
* Order does not exist.

### -2014 BAD_API_KEY_FMT
* API-key format invalid.

### -2015 REJECTED_MBX_KEY
* Invalid API-key, IP, or permissions for action.

### -2016 NO_TRADING_WINDOW
* No trading window could be found for the symbol. Try ticker/24hrs instead.

### -2018 BALANCE_NOT_SUFFICIENT
* Balance is insufficient.

### -2020 UNABLE_TO_FILL
* Unable to fill.

### -2021 ORDER_WOULD_IMMEDIATELY_TRIGGER
* Order would immediately trigger.

### -2022 REDUCE_ONLY_REJECT
* ReduceOnly Order is rejected.

### -2024 POSITION_NOT_SUFFICIENT
* Position is not sufficient.

### -2025 MAX_OPEN_ORDER_EXCEEDED
* Reach max open order limit.

### -2026 REDUCE_ONLY_ORDER_TYPE_NOT_SUPPORTED
* This OrderType is not supported when reduceOnly.


## 40xx - Filters and other Issues
### -4000 INVALID_ORDER_STATUS
* Invalid order status.

### -4001 PRICE_LESS_THAN_ZERO
* Price less than 0.

### -4002 PRICE_GREATER_THAN_MAX_PRICE
* Price greater than max price.

### -4003 QTY_LESS_THAN_ZERO
* Quantity less than zero.

### -4004 QTY_LESS_THAN_MIN_QTY
* Quantity less than min quantity.

### -4005 QTY_GREATER_THAN_MAX_QTY
* Quantity greater than max quantity. 

### -4006 STOP_PRICE_LESS_THAN_ZERO
* Stop price less than zero. 

### -4007 STOP_PRICE_GREATER_THAN_MAX_PRICE
* Stop price greater than max price. 

### -4008 TICK_SIZE_LESS_THAN_ZERO
* Tick size less than zero.

### -4009 MAX_PRICE_LESS_THAN_MIN_PRICE
* Max price less than min price.

### -4010 MAX_QTY_LESS_THAN_MIN_QTY
* Max qty less than min qty.

### -4011 STEP_SIZE_LESS_THAN_ZERO
* Step size less than zero.

### -4012 MAX_NUM_ORDERS_LESS_THAN_ZERO
* Max mum orders less than zero.

### -4013 PRICE_LESS_THAN_MIN_PRICE
* Price less than min price.

### -4014 PRICE_NOT_INCREASED_BY_TICK_SIZE
* Price not increased by tick size.

### -4015 INVALID_CL_ORD_ID_LEN
* Client order id is not valid.
* Client order id length should not be more than 36 chars

### -4016 PRICE_HIGHTER_THAN_MULTIPLIER_UP
* Price is higher than mark price multiplier cap.

### -4017 MULTIPLIER_UP_LESS_THAN_ZERO
* Multiplier up less than zero.

### -4018 MULTIPLIER_DOWN_LESS_THAN_ZERO
* Multiplier down less than zero.

### -4019 COMPOSITE_SCALE_OVERFLOW
* Composite scale too large.

### -4020 TARGET_STRATEGY_INVALID
* Target strategy invalid for orderType '%s',reduceOnly '%b'.

### -4021 INVALID_DEPTH_LIMIT
* Invalid depth limit.
* '%s' is not valid depth limit.

### -4022 WRONG_MARKET_STATUS
* market status sent is not valid.

### -4023 QTY_NOT_INCREASED_BY_STEP_SIZE
* Qty not increased by step size.

### -4024 PRICE_LOWER_THAN_MULTIPLIER_DOWN
* Price is lower than mark price multiplier floor.

### -4025 MULTIPLIER_DECIMAL_LESS_THAN_ZERO
* Multiplier decimal less than zero.

### -4026 COMMISSION_INVALID
* Commission invalid.
* `%s` less than zero.
* `%s` absolute value greater than `%s`

### -4027 INVALID_ACCOUNT_TYPE
* Invalid account type.

### -4029 INVALID_TICK_SIZE_PRECISION
* Tick size precision is invalid.

### -4030 INVALID_STEP_SIZE_PRECISION
* Step size precision is invalid.

### -4031 INVALID_WORKING_TYPE
* Invalid parameter working type
* Invalid parameter working type: `%s`

### -4032 EXCEED_MAX_CANCEL_ORDER_SIZE
* Exceed maximum cancel order size.
* Invalid parameter working type: `%s`

### -4044 INVALID_BALANCE_TYPE
* Balance Type is invalid.

### -4045 MAX_STOP_ORDER_EXCEEDED
* Reach max stop order limit.

### -4055 AMOUNT_MUST_BE_POSITIVE
* Amount must be positive.

### -4056 INVALID_API_KEY_TYPE
* Invalid api key type.

### -4057 INVALID_RSA_PUBLIC_KEY
* Invalid api public key

### -4058 MAX_PRICE_TOO_LARGE
* maxPrice and priceDecimal too large,please check.


### -4060 INVALID_POSITION_SIDE
* Invalid position side.

### -4061 POSITION_SIDE_NOT_MATCH
* Order's position side does not match user's setting.

### -4062 REDUCE_ONLY_CONFLICT
* Invalid or improper reduceOnly value.

### -4083 PLACE_BATCH_ORDERS_FAIL
* Fail to place batch orders.

### -4084 UPCOMING_METHOD
* Method is not allowed currently. Upcoming soon.

### -4086 INVALID_PRICE_SPREAD_THRESHOLD
* Invalid price spread threshold

### -4087 REDUCE_ONLY_ORDER_PERMISSION
* User can only place reduce only order

### -4088 NO_PLACE_ORDER_PERMISSION
* User can not place order currently

### -4114 INVALID_CLIENT_TRAN_ID_LEN
* clientTranId is not valid
* Client tran id length should be less than 64 chars

### -4115 DUPLICATED_CLIENT_TRAN_ID
* clientTranId is duplicated
* Client tran id should be unique within 7 days

### -4118 REDUCE_ONLY_MARGIN_CHECK_FAILED
* ReduceOnly Order Failed. Please check your existing position and open orders

### -4131 MARKET_ORDER_REJECT
* The counterparty's best price does not meet the PERCENT_PRICE filter limit

### -4135 INVALID_ACTIVATION_PRICE
* Invalid activation price

### -4137 QUANTITY_EXISTS_WITH_CLOSE_POSITION
* Quantity must be zero with closePosition equals true

### -4138 REDUCE_ONLY_MUST_BE_TRUE
* Reduce only must be true with closePosition equals true

### -4139 ORDER_TYPE_CANNOT_BE_MKT
* Order type can not be market if it's unable to cancel

### -4140 INVALID_OPENING_POSITION_STATUS
* Invalid symbol status for opening position

### -4141 SYMBOL_ALREADY_CLOSED
* Symbol is closed

### -4142 STRATEGY_INVALID_TRIGGER_PRICE
* REJECT: take profit or stop order will be triggered immediately

### -4164 MIN_NOTIONAL
* Order's notional must be no smaller than 5.0 (unless you choose reduce only)
* Order's notional must be no smaller than %s (unless you choose reduce only)

### -4165 INVALID_TIME_INTERVAL
* Invalid time interval
* Maximum time interval is %s days

### -4183 PRICE_HIGHTER_THAN_STOP_MULTIPLIER_UP
* Price is higher than stop price multiplier cap.
* Limit price can't be higher than %s.

### -4184 PRICE_LOWER_THAN_STOP_MULTIPLIER_DOWN
* Price is lower than stop price multiplier floor.
* Limit price can't be lower than %s.
