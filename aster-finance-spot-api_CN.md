# 基本信息
## API 基本信息
* 本篇列出接口的baseurl: **https://sapi.asterdex.com**
* 所有接口的响应都是 JSON 格式。
* 所有时间、时间戳均为UNIX时间，单位为**毫秒**。

## API Key 设置
* 很多接口需要API Key才可以访问.
* 设置API Key的同时，为了安全，建议设置IP访问白名单.
* **永远不要把你的API key/secret告诉给任何人**

<aside class="warning">
如果不小心泄露了API key，请立刻删除此Key, 并可以另外生产新的Key.
</aside>

### 注意事项
* TESTUSDT 或任何其他以 TEST 开头的交易对仅用于 Aster 的内部测试。请不要在这些以 TEST 开头的交易品种上进行交易。Aster 对因交易这些交易对而造成的资金损失不承担任何责任。但是，如果您遇到问题，您可以随时联系支持人员，我们将尽力帮助您收回资金。


### HTTP 返回代码
* HTTP `4XX` 错误码用于指示错误的请求内容、行为、格式。问题在于请求者。
* HTTP `403` 错误码表示违反WAF限制(Web应用程序防火墙)。
* HTTP `429` 错误码表示警告访问频次超限，即将被封IP。
* HTTP `418` 表示收到429后继续访问，IP已经被封禁。
* HTTP `5XX` 错误码用于指示Aster服务侧的问题。    

### 接口错误代码
* 使用接口 `/api/v1`, 每个接口都有可能抛出异常; 
> API的错误代码返回形式如下:
```javascript
{
  "code": -1121,
  "msg": "Invalid symbol."
}
```

### 接口的基本信息

* `GET` 方法的接口, 参数必须在 `query string`中发送。
* `POST`, `PUT`, 和 `DELETE` 方法的接口,参数可以在内容形式为`application/x-www-form-urlencoded`的 `query string` 中发送，也可以在 `request body` 中发送。 
* 对参数的顺序不做要求。

---
## 访问限制
### 访问限制基本信息

* 在 `/api/v1/exchangeInfo` `rateLimits` 数组中包含与交易的有关REQUEST_WEIGHT和ORDERS速率限制相关的对象。这些在 `限制种类 (rateLimitType)` 下的 `枚举定义` 部分中进一步定义。
* 违反任何一个速率限制时，将返回429。

### IP 访问限制
* 每个请求的回报中包含一个`X-MBX-USED-WEIGHT-(intervalNum)(intervalLetter)`的头，其中包含当前IP所有请求的已使用权重。
* 每一个接口均有一个相应的权重(weight)，有的接口根据参数不同可能拥有不同的权重。越消耗资源的接口权重就会越大。
* 收到429时，您有责任停止发送请求，不得滥用API。
* **收到429后仍然继续违反访问限制，会被封禁IP，并收到418错误码**
* 频繁违反限制，封禁时间会逐渐延长，**从最短2分钟到最长3天**。
* `Retry-After`的头会与带有418或429的响应发送，并且会给出**以秒为单位**的等待时长(如果是429)以防止禁令，或者如果是418，直到禁令结束。
* **访问限制是基于IP的，而不是API Key**

<aside class="notice">
建议您尽可能多地使用websocket消息获取相应数据，以减少请求带来的访问限制压力。
</aside>


### 下单频率限制
* 每个成功的下单回报将包含一个`X-MBX-ORDER-COUNT-(intervalNum)(intervalLetter)`的头，其中包含当前账户已用的下单限制数量。
* 当下单数超过限制时，会收到带有429但不含`Retry-After`头的响应。请检查 `GET api/v1/exchangeInfo` 的下单频率限制 (rateLimitType = ORDERS) 并等待封禁时间结束。
* 被拒绝或不成功的下单并不保证回报中包含以上头内容。
* **下单频率限制是基于每个账户计数的。**

### WEB SOCKET 连接限制

* Websocket服务器每秒最多接受5个消息。消息包括:
	* PING帧
	* PONG帧
	* JSON格式的消息, 比如订阅, 断开订阅.
* 如果用户发送的消息超过限制，连接会被断开连接。反复被断开连接的IP有可能被服务器屏蔽。
* 单个连接最多可以订阅 **1024** 个Streams。


---
## 接口鉴权类型
* 每个接口都有自己的鉴权类型，鉴权类型决定了访问时应当进行何种鉴权。
* 鉴权类型会在本文档中各个接口名称旁声明，如果没有特殊声明即默认为 `NONE`。
* 如果需要 API-keys，应当在HTTP头中以 `X-MBX-APIKEY`字段传递。
* API-keys 与 secret-keys **是大小写敏感的**。
* 默认 API-keys 可访问所有鉴权路径.

鉴权类型 | 描述
------------ | ------------
NONE | 不需要鉴权的接口
TRADE | 需要有效的 API-Key 和签名
USER_DATA | 需要有效的 API-Key 和签名
USER_STREAM | 需要有效的 API-Key
MARKET_DATA | 需要有效的 API-Key


* `TRADE` 和`USER_DATA` 接口是 签名(SIGNED)接口.

---
## SIGNED (TRADE AND USER_DATA) Endpoint security
* 调用`SIGNED` 接口时，除了接口本身所需的参数外，还需要在`query string` 或 `request body`中传递 `signature`, 即签名参数。
* 签名使用`HMAC SHA256`算法. API-KEY所对应的API-Secret作为 `HMAC SHA256` 的密钥，其他所有参数作为`HMAC SHA256`的操作对象，得到的输出即为签名。
* `签名` **大小写不敏感**.
* "totalParams"定义为与"request body"串联的"query string"。

### 时间同步安全
* 签名接口均需要传递 `timestamp`参数，其值应当是请求发送时刻的unix时间戳(毫秒)。
* 服务器收到请求时会判断请求中的时间戳，如果是5000毫秒之前发出的，则请求会被认为无效。这个时间空窗值可以通过发送可选参数 `recvWindow`来定义。

> 逻辑伪代码如下:
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

**关于交易时效性** 互联网状况并不完全稳定可靠,因此你的程序本地到Aster服务器的时延会有抖动。这是我们设置`recvWindow`的目的所在，如果你从事高频交易，对交易时效性有较高的要求，可以灵活设置`recvWindow`以达到你的要求。

<aside class="notice">
推荐使用5秒以下的 recvWindow! 最多不能超过 60秒!
</aside>

### POST /api/v1/order 的示例
以下是在linux bash环境下使用 echo openssl 和curl工具实现的一个调用接口下单的示例 apikey、secret仅供示范

Key | Value
------------ | ------------
apiKey | 4452d7e2ed4da80b74105e02d06328c71a34488c9fdd60a5a0900d42d584b795
secretKey | fdde510a2b71fa43a43bff3e3cf7819c8c66df34633d338050f4f59664b3b313


参数 | 取值
------------ | ------------
symbol | BNBUSDT
side | BUY
type | LIMIT
timeInForce | GTC
quantity | 5
price | 1.1
recvWindow | 5000
timestamp | 1756187806000


#### 示例 1: 所有参数通过 request body 发送

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


#### 示例 2: 所有参数通过 query string 发送

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
* **queryString:**  

symbol=BNBUSDT   
&side=BUY   
&type=LIMIT   
&timeInForce=GTC   
&quantity=5   
&price=1.1   
&recvWindow=5000   
&timestamp=1756187806000

---

## 公开 API 参数
### 术语

这里的术语适用于全部文档，建议特别是新手熟读，也便于理解。

* `base asset` 指一个交易对的交易对象，即写在靠前部分的资产名, 比如`BTCUSDT`, `BTC`是`base asset`。
* `quote asset` 指一个交易对的定价资产，即写在靠后部分的资产名, 比如`BTCUSDT`, `USDT`是`quote asset`。

### 枚举定义
**交易对状态 (状态 status):**

* TRADING 交易中


**交易对类型:**

* SPOT 现货

**订单状态 (状态 status):**

状态 | 描述
-----------| --------------
`NEW` | 订单被交易引擎接受
`PARTIALLY_FILLED`| 部分订单被成交
`FILLED` | 订单完全成交
`CANCELED` | 用户撤销了订单
`REJECTED`       | 订单没有被交易引擎接受，也没被处理
`EXPIRED` | 订单被交易引擎取消, 比如 <br/>LIMIT FOK 订单没有成交<br/>市价单没有完全成交<br/>交易所维护期间被取消的订单


**订单类型 (orderTypes, type):**

* LIMIT 限价单
* MARKET 市价单
* STOP 限价止损单
* TAKE_PROFIT 限价止盈单
* STOP_MARKET 市价止损单
* TAKE_PROFIT_MARKET 市价止盈单

**订单返回类型 (newOrderRespType):**

* ACK
* RESULT
* FULL

**订单方向 (方向 side):**

* BUY 买入
* SELL 卖出

**有效方式 (timeInForce):**

这里定义了订单多久能够失效

Status | Description
-----------| --------------
`GTC` | 成交为止 <br> 订单会一直有效，直到被成交或者取消。
`IOC` | 无法立即成交的部分就撤销 <br> 订单在失效前会尽量多的成交。
`FOK` | 无法全部立即成交就撤销 <br> 如果无法全部成交，订单会失效。
`GTX` | 直到挂单成交 <br> 限价只挂单。

**K线间隔:**

m -> 分钟; h -> 小时; d -> 天; w -> 周; M -> 月

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

**限制种类 (rateLimitType)**

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


* REQUEST_WEIGHT 单位时间请求权重之和上限

* ORDERS 单位时间下单次数限制


**限制间隔 (interval)**

* MINUTE 分

---
## 过滤器 
过滤器，即Filter，定义了一系列交易规则。
共有两类，分别是针对交易对的过滤器`symbol filters`，和针对整个交易所的过滤器`exchange filters`(暂不支持)

### 交易对过滤器  

#### PRICE_FILTER 价格过滤器

> **/exchangeInfo 响应中的格式:**
```javascript
  {                     
    "minPrice": "556.72",
    "maxPrice": "4529764",
    "filterType": "PRICE_FILTER",
    "tickSize": "0.01"   
  }
```

`价格过滤器` 用于检测订单中 `price` 参数的合法性。包含以下三个部分:

* `minPrice` 定义了 `price`/`stopPrice` 允许的最小值。
* `maxPrice` 定义了 `price`/`stopPrice` 允许的最大值。
* `tickSize` 定义了 `price`/`stopPrice` 的步进间隔，即price必须等于minPrice+(tickSize的整数倍)

以上每一项均可为0，为0时代表这一项不再做限制。

逻辑伪代码如下:

* `price` >= `minPrice` 
* `price` <= `maxPrice`
* (`price`-`minPrice`) % `tickSize` == 0


#### PERCENT_PRICE 价格振幅过滤器

> **/exchangeInfo 响应中的格式:**
```javascript
  {                    
	"multiplierDown": "0.9500",
	"multiplierUp": "1.0500",
	"multiplierDecimal": "4",
	"filterType": "PERCENT_PRICE"
  }
```

`PERCENT_PRICE`过滤器基于指数价格来定义价格的有效范围。   

为了通过"价格百分比"，"价格"必须符合以下条件：

* `price` <=`indexPrice` *`multiplierUp`
* `price`> =`indexPrice` *`multiplierDown`


#### LOT_SIZE 订单尺寸

> **/exchangeInfo 响应中的格式:**
```javascript
  {
    "stepSize": "0.00100000",
    "filterType": "LOT_SIZE",
    "maxQty": "100000.00000000",
    "minQty": "0.00100000"
  }
```

Lots是拍卖术语，`LOT_SIZE` 过滤器对订单中的 `quantity` 也就是数量参数进行合法性检查。包含三个部分:

* `minQty` 表示 `quantity` 允许的最小值。
* `maxQty` 表示 `quantity` 允许的最大值。
* `stepSize` 表示 `quantity` 允许的步进值。

逻辑伪代码如下:

* `quantity` >= `minQty`
* `quantity` <= `maxQty`
* (`quantity`-`minQty`) % `stepSize` == 0




#### MARKET_LOT_SIZE 市价订单尺寸

> ***/exchangeInfo 响应中的格式:**
```javascript
  {
    "stepSize": "0.00100000",
    "filterType": "MARKET_LOT_SIZE"
	"maxQty": "100000.00000000",
	"minQty": "0.00100000"
  }
```


`MARKET_LOT_SIZE`过滤器为交易对上的`MARKET`订单定义了`数量`(即拍卖中的"手数")规则。 共有3部分：

* `minQty`定义了允许的最小`quantity`。
* `maxQty`定义了允许的最大数量。
* `stepSize`定义了可以增加/减少数量的间隔。

为了通过`market lot size`，`quantity`必须满足以下条件：

* `quantity` >= `minQty`
* `quantity` <= `maxQty`
* (`quantity`-`minQty`) % `stepSize` == 0










# 行情接口
## 测试服务器连通性
> **响应**
```javascript
{}
```
``
GET /api/v1/ping
``

测试能否联通 Rest API。

**权重:**
1

**参数:**
NONE


## 获取服务器时间
> **响应**
```javascript
{
  "serverTime": 1499827319559
}
```
``
GET /api/v1/time
``

测试能否联通 Rest API 并获取服务器时间。

**权重:**
1

**参数:**
NONE


## 交易规范信息

> **响应** 

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

获取交易规则和交易对信息。

**权重:**
1

**参数:**
无


## 深度信息

> **响应**

```javascript
{
  "lastUpdateId": 1027024,
  "E":1589436922972, // 消息时间
  "T":1589436922959, // 撮合引擎时间
  "bids": [
    [
      "4.00000000", // 价位
      "431.00000000" // 挂单量
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

**权重:**

基于限制调整:

限制 | 权重
------------ | ------------
5, 10, 20, 50 | 2
100 | 5
500 | 10
1000 | 20

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
limit | INT | NO | 默认 100. 可选值:[5, 10, 20, 50, 100, 500, 1000]


## 近期成交列表

> **响应**

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

获取近期成交

**权重:**
1

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
limit | INT | NO | 默认 500；最大1000


## 查询历史成交 (MARKET_DATA)

> **响应**

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

获取历史成交。

**权重:**
20

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
limit | INT | NO | 默认 500; 最大值 1000.
fromId | LONG | NO | 从哪一条成交id开始返回. 缺省返回最近的成交记录。


## 近期成交(归集)

> **响应**

```javascript
[
  {
    "a": 26129, // 归集成交ID
    "p": "0.01633102", // 成交价
    "q": "4.70443515", // 成交量
    "f": 27781, // 被归集的首个成交ID
    "l": 27781, // 被归集的末个成交ID
    "T": 1498793709153, // 成交时间
    "m": true, // 是否为主动卖出单
  }
]
```
``
GET /api/v1/aggTrades
``

归集交易与逐笔交易的区别在于，同一价格、同一方向、同一时间的trade会被聚合为一条

**权重:**
20

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
fromId | LONG | NO | 从包含fromId的成交id开始返回结果
startTime | LONG | NO | 从该时刻之后的成交记录开始返回结果
endTime | LONG | NO | 返回该时刻为止的成交记录
limit | INT | NO | 默认 500; 最大 1000.
* 如果发送startTime和endTime，间隔必须小于一小时。
* 如果没有发送任何筛选参数(fromId, startTime,endTime)，默认返回最近的成交记录


## K线数据

> **响应**
```javascript
[
  [
    1499040000000, // 开盘时间
    "0.01634790", // 开盘价
    "0.80000000", // 最高价
    "0.01575800", // 最低价
    "0.01577100", // 收盘价(当前K线未结束的即为最新价)
    "148976.11427815", // 成交量
    1499644799999, // 收盘时间
    "2434.19055334", // 成交额
    308, // 成交笔数
    "1756.87402397", // 主动买入成交量
    "28.46694368", // 主动买入成交额
  ]
]
```
``
GET /api/v1/klines
``

每根K线代表一个交易对。 
每根K线的开盘时间可视为唯一ID


**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
interval | ENUM | YES | 详见枚举定义：K线间隔
startTime | LONG | NO |
endTime | LONG | NO |
limit | INT | NO | 默认 500; 最大 1500.
* 如果未发送 startTime 和 endTime ，默认返回最近的交易。



## 24hr 价格变动情况

> **响应**

```javascript 
{
  "symbol": "BTCUSDT",
  "priceChange": "-94.99999800",    //24小时价格变动
  "priceChangePercent": "-95.960",  //24小时价格变动百分比
  "weightedAvgPrice": "0.29628482", //加权平均价
  "prevClosePrice": "3.89000000",   //上一次结束价格
  "lastPrice": "4.00000200",        //最近一次成交价
  "lastQty": "200.00000000",        //最近一次成交额
  "bidPrice": "866.66000000",       //最高的买入价格
  "bidQty": "72.05100000",          //最高的买入价格的数量
  "askPrice": "866.73000000",       //最低的卖出价
  "askQty": "1.21700000",           //最低的卖出价格的数量
  "openPrice": "99.00000000",       //24小时内第一次成交的价格
  "highPrice": "100.00000000",      //24小时最高价
  "lowPrice": "0.10000000",         //24小时最低价
  "volume": "8913.30000000",        //24小时成交量
  "quoteVolume": "15.30000000",     //24小时成交额
  "openTime": 1499783499040,        //24小时内，第一笔交易的发生时间
  "closeTime": 1499869899040,       //24小时内，最后一笔交易的发生时间
  "firstId": 28385,   // 首笔成交id
  "lastId": 28460,    // 末笔成交id
  "count": 76,         // 成交笔数
  "baseAsset": "BTC",   //基础代币
  "quoteAsset": "USDT"  //报价代币
}
```

``
GET /api/v1/ticker/24hr
``

24 小时滚动窗口价格变动数据。 请注意，不携带symbol参数会返回全部交易对数据，此时返回的数据为示例相应的数组，不仅数据庞大，而且权重极高

**权重:**
1 单一交易对; 
**40** 交易对参数缺失;

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
symbol | STRING | NO |
* 请注意，不携带symbol参数会返回全部交易对数据

## 最新价格

> **响应**

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

获取交易对最新价格

**权重:**
1 单一交易对; 
**2** 交易对参数缺失;

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
symbol | STRING | NO |
* 不发送交易对参数，则会返回所有交易对信息


## 当前最优挂单
> **响应**
```javascript
{
  "symbol": "LTCBTC",
  "bidPrice": "4.00000000",
  "bidQty": "431.00000000",
  "askPrice": "4.00000200",
  "askQty": "9.00000000"
  "time": 1589437530011   // 交易时间
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
    "time": 1589437530011   // 交易时间
  }
]
```

``
GET /api/v1/ticker/bookTicker
``

返回当前最优的挂单(最高买单，最低卖单)

**权重:**
1 单一交易对; 
**2** 交易对参数缺失;

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
symbol | STRING | NO |
* 不发送交易对参数，则会返回所有交易对信息

## 获取Symbol手续费

> **响应**

```javascript
{
   "symbol": "APXUSDT",
   "makerCommissionRate": "0.000200",    
   "takerCommissionRate": "0.000700"
}
```
``
GET /api/v1/commissionRate
``

获取Symbol手续费。

**权重:**
20

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
recvWindow | LONG | NO |赋值不能大于 ```60000```
timestamp | LONG | YES |





# 现货账户和交易接口


## 下单  (TRADE)

> **Response ACK:**

```javascript
{
  "symbol": "BTCUSDT", // 交易对
  "orderId": 28, // 系统的订单ID
  "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP", // 客户自己设置的ID
  "updateTime": 1507725176595, // 交易的时间戳
  "price": "0.00000000", // 订单价格
  "avgPrice": "0.0000000000000000", //平均价格
  "origQty": "10.00000000", // 用户设置的原始订单数量
  "cumQty": "0",            //累计数量
  "executedQty": "10.00000000", // 交易的订单数量
  "cumQuote": "10.00000000", // 累计交易的金额
  "status": "FILLED", // 订单状态
  "timeInForce": "GTC", // 订单的时效方式
  "stopPrice": "0",     //触发价格
  "origType": "LIMIT",  //触发前订单类型
  "type": "LIMIT", // 订单类型， 比如市价单，现价单等
  "side": "SELL", // 订单方向，买还是卖
}
```

``
POST /api/v1/order  (HMAC SHA256)
``

发送下单。

**权重:**
1

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
side | ENUM | YES | 详见枚举定义：订单方向
type | ENUM | YES | 详见枚举定义：订单类型 
timeInForce | ENUM | NO | 详见枚举定义：有效方式 
quantity | DECIMAL | NO |
quoteOrderQty|DECIMAL|NO|
price | DECIMAL | NO |
newClientOrderId | STRING | NO | 客户自定义的唯一订单ID。 如果未发送，则自动生成
stopPrice | DECIMAL | NO | 仅 `STOP`, `STOP_MARKET` , `TAKE_PROFIT`,`TAKE_PROFIT_MARKET` 需要此参数。
recvWindow | LONG | NO |赋值不能大于 ```60000```
timestamp | LONG | YES |

基于订单 `type`不同，强制要求某些参数:

类型 | 强制要求的参数
------------ | ------------
`LIMIT` | `timeInForce`, `quantity`, `price`
`MARKET` | `quantity` 或 `quoteOrderQty` 
`STOP`和`TAKE_PROFIT` | `quantity`,  `price`, `stopPrice`
`STOP_MARKET`和`TAKE_PROFIT_MARKET` | `quantity`, `stopPrice`

其他信息:

* 下`MARKET` `SELL`市价单，用户通过`QUANTITY`控制想用市价单卖出的基础资产数量。
  * 比如在`BTCUSDT`交易对上下一个`MARKET` `SELL`市价单, 通过`QUANTITY`让用户指明想卖出多少BTC。
* 下`MARKET` `BUY`的市价单，用户使用 `quoteOrderQty` 控制想用市价单买入的报价资产数量，`QUANTITY`将由系统根据市场流动性计算出来。
  * 比如在`BTCUSDT`交易对上下一个`MARKET` `BUY`市价单, 通过`quoteOrderQty`让用户选择想使用多少USDT买入BTC。
* 使用 `quoteOrderQty` 的市价单`MARKET`不会突破`LOT_SIZE`的限制规则; 报单会按给定的`quoteOrderQty`尽可能接近地被执行。
* 除非之前的订单已经成交, 不然设置了相同的`newClientOrderId`订单会被拒绝。



## 撤销订单 (TRADE)

> **响应**

```javascript
{
  "symbol": "BTCUSDT", // 交易对
  "orderId": 28, // 系统的订单ID
  "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP", // 客户自己设置的ID
  "updateTime": 1507725176595, // 交易的时间戳
  "price": "0.00000000", // 订单价格
  "avgPrice": "0.0000000000000000", //平均价格
  "origQty": "10.00000000", // 用户设置的原始订单数量
  "cumQty": "0",            //累计数量
  "executedQty": "10.00000000", // 交易的订单数量
  "cumQuote": "10.00000000", // 累计交易的金额
  "status": "CANCELED", // 订单状态
  "timeInForce": "GTC", // 订单的时效方式
  "stopPrice": "0",     //触发价格
  "origType": "LIMIT",  //触发前订单类型
  "type": "LIMIT", // 订单类型， 比如市价单，现价单等
  "side": "SELL", // 订单方向，买还是卖
}
```

``
DELETE /api/v1/order  (HMAC SHA256)
``

取消有效订单。

**权重:**
1

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
orderId | LONG | NO |
origClientOrderId | STRING | NO |
recvWindow | LONG | NO | 
timestamp | LONG | YES |

`orderId` 或 `origClientOrderId` 必须至少发送一个

## 查询订单 (USER_DATA)

> **响应**
```javascript
{
    "orderId": 38,   // 系统订单号
    "symbol": "ADA25SLP25",  // 交易对
    "status": "FILLED",  // 订单状态
    "clientOrderId": "afMd4GBQyHkHpGWdiy34Li",  // 用户自定义的订单号
    "price": "20",  // 委托价格
    "avgPrice": "12.0000000000000000",  // 平均成交价
    "origQty": "10",  // 原始委托数量
    "executedQty": "10",  // 成交量
    "cumQuote": "120",  // 成交金额
    "timeInForce": "GTC",  // 有效方法
    "type": "LIMIT",  // 订单类型
    "side": "BUY",  // 买卖方向
    "stopPrice": "0",  // 触发价
    "origType": "LIMIT",  // 触发前订单类型
    "time": 1649913186270,  // 订单时间
    "updateTime": 1649913186297  // 更新时间
}
```

``
GET /api/v1/order (HMAC SHA256)
``

查询订单状态。

* 请注意，如果订单满足如下条件，不会被查询到：
	* 订单的最终状态为 `CANCELED` 或者 `EXPIRED`, **并且** 
	* 订单没有任何的成交记录, **并且**
	* 订单生成时间 + 7天 < 当前时间

**权重:**
1

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
orderId | LONG | NO |
origClientOrderId | STRING | NO |
recvWindow | LONG | NO |  
timestamp | LONG | YES |

注意:

* 至少需要发送 `orderId` 与 `origClientOrderId`中的一个


## 查询当前挂单 (USER_DATA)

> **响应**
```javascript
{
    "orderId": 38,   // 系统订单号
    "symbol": "ADA25SLP25",  // 交易对
    "status": "NEW",  // 订单状态
    "clientOrderId": "afMd4GBQyHkHpGWdiy34Li",  // 用户自定义的订单号
    "price": "20",  // 委托价格
    "avgPrice": "12.0000000000000000",  // 平均成交价
    "origQty": "10",  // 原始委托数量
    "executedQty": "10",  // 成交量
    "cumQuote": "120",  // 成交金额
    "timeInForce": "GTC",  // 有效方法
    "type": "LIMIT",  // 订单类型
    "side": "BUY",  // 买卖方向
    "stopPrice": "0",  // 触发价
    "origType": "LIMIT",  // 触发前订单类型
    "time": 1649913186270,  // 订单时间
    "updateTime": 1649913186297  // 更新时间
}
```

``
GET /api/v1/openOrder (HMAC SHA256)
``

查询订单状态。

**权重:**
1

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
orderId | LONG | NO |
origClientOrderId | STRING | NO |
recvWindow | LONG | NO |  
timestamp | LONG | YES |

注意:

* 至少需要发送 `orderId` 与 `origClientOrderId`中的一个


## 当前所有挂单 (USER_DATA)

> **响应**

```javascript
[
    {
        "orderId": 349661, // 系统订单号
        "symbol": "BNBUSDT", // 交易对
        "status": "NEW", // 订单状态
        "clientOrderId": "LzypgiMwkf3TQ8wwvLo8RA", // 用户自定义的订单号
        "price": "1.10000000", // 委托价格
        "avgPrice": "0.0000000000000000", // 平均成交价
        "origQty": "5",  // 原始委托数量
        "executedQty": "0", // 成交量
        "cumQuote": "0", // 成交金额
        "timeInForce": "GTC", // 有效方法
        "type": "LIMIT", // 订单类型
        "side": "BUY",   // 买卖方向
        "stopPrice": "0", // 触发价
        "origType": "LIMIT", // 触发前订单类型
        "time": 1756252940207, // 订单时间
        "updateTime": 1756252940207, // 更新时间
    }
]
```

``
GET /api/v1/openOrders  (HMAC SHA256)
``

获取交易对的所有当前挂单， 请小心使用不带交易对参数的调用。

**权重:**
- 带symbol ***1***
- 不带 ***40***  

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
symbol | STRING | NO |
recvWindow | LONG | NO |
timestamp | LONG | YES |

* 不带symbol参数，会返回所有交易对的挂单



## 取消当前所有挂单 (USER_DATA)

> **响应**

```javascript
{
    "code": 200,
    "msg": "The operation of cancel all open order is done."
}
```

``
DEL /api/v1/allOpenOrders  (HMAC SHA256)
``

**权重:**
- ***1***

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
orderIdList | STRING | NO | id数组字符串
origClientOrderIdList | STRING | NO | clientOrderId数组字符串
recvWindow | LONG | NO |
timestamp | LONG | YES |


## 查询所有订单 (USER_DATA)
> **响应**
```javascript
[
    {
        "orderId": 349661, // 系统订单号
        "symbol": "BNBUSDT", // 交易对
        "status": "NEW", // 订单状态
        "clientOrderId": "LzypgiMwkf3TQ8wwvLo8RA", // 用户自定义的订单号
        "price": "1.10000000", // 委托价格
        "avgPrice": "0.0000000000000000", // 平均成交价
        "origQty": "5",  // 原始委托数量
        "executedQty": "0", // 成交量
        "cumQuote": "0", // 成交金额
        "timeInForce": "GTC", // 有效方法
        "type": "LIMIT", // 订单类型
        "side": "BUY",   // 买卖方向
        "stopPrice": "0", // 触发价
        "origType": "LIMIT", // 触发前订单类型
        "time": 1756252940207, // 订单时间
        "updateTime": 1756252940207, // 更新时间
    }
]
```

``
GET /api/v1/allOrders (HMAC SHA256)
``

获取所有帐户订单； 有效，已取消或已完成。

* 请注意，如果订单满足如下条件，不会被查询到：
	* 订单生成时间 + 7天 < 当前时间

**权重:** 
5

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
symbol | STRING | YES |
orderId | LONG | NO |
startTime | LONG | NO |
endTime | LONG | NO |
limit | INT | NO | 默认 500; 最大 1000.
recvWindow | LONG | NO | 
timestamp | LONG | YES |  

* 查询时间范围最大不得超过7天
* 默认查询最近7天内的数据 



``
GET /api/v1/transactionHistory (HMAC SHA256)
``
> **响应**

```javascript
[
   {
    "tranId": 1759115482304540227, //划转ID
    "tradeId": null,               //流水ID 
    "asset": "ASTER",              //资产
    "symbol": "",                  //交易对
    "balanceDelta": "-500.00000000", //资金流数量，正数代表流入，负数代表流出
    "balanceInfo": "TRADE_SOURCE",   //流水描述 
    "time": 1759115482000,       // 时间
    "type": "TRADE_SOURCE"      //资金流类型
   }
]
```

查询交易流水

**权重:**
30

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
asset | STRING | NO | 资产
type | STRING | NO |  类别
startTime | LONG | NO | 开始时间
endTime | LONG | NO |  结束时间
limit | LONG | NO | 返回的结果集数量 默认值:100 最大值:1000
recvWindow | LONG | NO |  
timestamp | LONG | YES |

注意:

*  `type` 取值 `TRADE_TARGET`,`TRADE_SOURCE`,`TRANSFER_SPOT_TO_FUTURE`,`TRANSFER_FUTURE_TO_SPOT`,`TRANSFER_SPOT_TO_SPOT`,`AIRDROP`,`DIVIDEND`,`TRANSFER_REFUND`,`INTERNAL_TRANSFER`,`TRANSFER`,`SWAP`,`COMMISSION_REBATE`,`CASH_BACK` 中的一种
*  如果`startTime` 和 `endTime` 均未发送, 只会返回最近7天的数据。

## 期货现货互转 (TRADE)

> **响应:**

```javascript
{
    "tranId": 21841, //交易id
    "status": "SUCCESS" //状态
}
```

``
POST /api/v1/asset/wallet/transfer  (HMAC SHA256)
``

**权重:**
5

**参数:**


名称              |  类型   | 是否必需   | 描述
---------------- | ------- | -------- | ----
amount |	DECIMAL | 	YES |	数量
asset |	STRING | 	YES |	资产
clientTranId |	STRING | 	YES |	交易id 
kindType |	STRING | 	YES |	交易类型
recvWindow | LONG | NO | 
timestamp	| LONG | YES	|	时间戳

注意:
* kindType 取值为FUTURE_SPOT(期货转现货),SPOT_FUTURE(现货转期货)

## 现货提现手续费 (NONe)
> **响应**
```javascript
{
  "tokenPrice": 1.00019000,
   "gasCost": 0.5000,
  "gasUsdValue": 0.5
}
```

``
GET /api/v1/aster/withdraw/estimateFee 
``

**权重:** 
1

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
chainId | STRING | YES | 
asset | STRING | YES |

注意:
* chainId: 1(ETH),56(BSC),42161(Arbi)
* gasCost: 提现所需的最少数量的手续费

## 现货提现 (USER_DATA)
> **响应**
```javascript
{
  "withdrawId": "1014729574755487744",
  "hash":"0xa6d1e617a3f69211df276fdd8097ac8f12b6ad9c7a49ba75bbb24f002df0ebb"
}
```

``
POST /api/v1/aster/user-withdraw (HMAC SHA256)
``

**权重:** 
5

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
chainId | STRING | YES | 
asset | STRING | YES |
amount | STRING | YES |
fee | STRING | YES |
receiver | STRING | YES | 
nonce | STRING | YES |  当前时间的微秒值 
userSignature | STRING | YES | 
recvWindow | LONG | NO | 
timestamp | LONG | YES | 

注意:
* chainId: 1(ETH),56(BSC),42161(Arbi)
* receiver : 当前账户的地址
* 如果期货余额不足，会从spot账户划转到期货账户，进行提现
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

## 获取创建apikey nonce (NONE)
> **响应**
```javascript

111111

```

``
POST /api/v1/getNonce 
``

**权重:** 
1

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
address | STRING | YES |
userOperationType | STRING | YES | CREATE_API_KEY
network | STRING | NO | 

注意:
* userOperationType 仅可取值: CREATE_API_KEY
* network: sol网络必须传入SOL,其他忽略
* 限流单IP一分钟60次


## 创建apikey (NONE)
> **响应**
```javascript
{
    "apiKey": "bb3b24d0a3dec88cb06be58a257e4575cb0b1bb256ad6fd90ae8fd0ee1d102ae",
    "apiSecret": "9fe8f5642ae1961674ea0cb7f957fa99dc8e0421b607c985a963ad2ced90ae1c"
}
```

``
POST /api/v1/createApiKey
``

**权重:** 
1

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
address | STRING | YES |
userOperationType | STRING | YES | CREATE_API_KEY
network | STRING | NO | 
userSignature | STRING | YES | 
apikeyIP | STRING | NO | 
desc | STRING | YES | 
recvWindow | LONG | NO | 
timestamp | LONG | YES | 

注意:
* userOperationType 仅可取值: CREATE_API_KEY
* network: sol网络必须传入SOL,其他忽略
* desc: 同一账户不能重复，长度不能超过20个字符
* apikeyIP ip数组以,分隔
* 限流单IP一分钟60次
* userSignature evm demo

```shell

const nonce = 111111
const message = 'You are signing into Astherus ${nonce}' ;

const signature = await signer.signMessage(message);
```


## 账户信息 (USER_DATA)
> **响应**
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

获取当前账户信息。

**权重:**
5

**参数:**

名称 | 类型 | 是否必需| 描述
------------ | ------------ | ------------ | ------------
recvWindow | LONG | NO | 
timestamp | LONG | YES |


## 账户成交历史 (USER_DATA)
> **响应**
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
GET /api/v1/userTrades  (HMAC SHA256)
``

获取账户指定交易对的成交历史

**权重:**
5

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
symbol | STRING | NO |
orderId|LONG|NO| 必须要和参数`symbol`一起使用.
startTime | LONG | NO |
endTime | LONG | NO |
fromId | LONG | NO | 起始Trade id。 默认获取最新交易。
limit | INT | NO | 默认 500; 最大 1000.
recvWindow | LONG | NO | 
timestamp | LONG | YES |

* 如果`startTime` 和 `endTime` 均未发送, 只会返回最近7天的数据。
* startTime 和 endTime 的最大间隔为7天
* 不能同时传`fromId`与`startTime` 或 `endTime`
       




---
# Websocket 行情推送

* 本篇所列出的所有wss接口的baseurl为: **wss://sstream.asterdex.com**
* Streams有单一原始 stream 或组合 stream
* 单一原始 streams 格式为 **/ws/\<streamName\>**
* 组合streams的URL格式为 **/stream?streams=\<streamName1\>/\<streamName2\>/\<streamName3\>**
* 订阅组合streams时，事件payload会以这样的格式封装: **{"stream":"\<streamName\>","data":\<rawPayload\>}**
* stream名称中所有交易对均为 **小写**
* 每个到 **sstream.asterdex.com** 的链接有效期不超过24小时，请妥善处理断线重连。
* 每3分钟，服务端会发送ping帧，客户端应当在10分钟内回复pong帧，否则服务端会主动断开链接。允许客户端发送不成对的pong帧(即客户端可以以高于10分钟每次的频率发送pong帧保持链接)。

## 实时订阅/取消数据流

* 以下数据可以通过websocket发送以实现订阅或取消订阅数据流。示例如下。
* 响应内容中的`id`是无符号整数，作为往来信息的唯一标识。
* 如果相应内容中的 `result` 为 `null`，表示请求发送成功。
  

### 订阅一个信息流
> **响应**
  ```javascript
  {
    "result": null,
    "id": 1
  }
  ```
* **请求**
  	{    
    	"method": "SUBSCRIBE",    
    	"params":     
    	[   
      	"btcusdt@aggTrade",    
      	"btcusdt@depth"     
    	],    
    	"id": 1   
  	}


### 取消订阅一个信息流

> **响应**
  
  ```javascript
  {
    "result": null,
    "id": 312
  }
  ```

* **请求**
  {   
    "method": "UNSUBSCRIBE",    
    "params":     
    [    
      "btcusdt@depth"   
    ],    
    "id": 312   
  }


### 已订阅信息流

> **响应**
  
  ```javascript
  {
    "result": [
      "btcusdt@aggTrade"
    ],
    "id": 3
  }
  ```

* **请求**

  {   
    "method": "LIST_SUBSCRIPTIONS",    
    "id": 3   
  }     
 

### 设定属性
当前，唯一可以设置的属性是设置是否启用`combined`("组合")信息流。   
当使用`/ws/`("原始信息流")进行连接时，combined属性设置为`false`，而使用 `/stream/`进行连接时则将属性设置为`true`。

> **响应**
  
  ```javascript
{
  "result": null,
  "id": 5
}
  ```

* **请求**
  {    
    "method": "SET_PROPERTY",    
    "params":     
    [   
      "combined",    
      true   
    ],    
    "id": 5   
  }


### 检索属性

> **响应**
  ```javascript
  {
    "result": true, // Indicates that combined is set to true.
    "id": 2
  }
  ```
  
* **请求**
  
  {   
    "method": "GET_PROPERTY",    
    "params":     
    [   
      "combined"   
    ],    
    "id": 2   
  }   
 

###错误信息

错误信息 | 描述
---|---
{"code": 0, "msg": "Unknown property"} |  `SET_PROPERTY` 或 `GET_PROPERTY`中应用的参数无效
{"code": 1, "msg": "Invalid value type: expected Boolean", "id": '%s'} | 仅接受`true`或`false`
{"code": 2, "msg": "Invalid request: property name must be a string"}| 提供的属性名无效
{"code": 2, "msg": "Invalid request: request ID must be an unsigned integer"}| 参数`id`未提供或`id`值是无效类型
{"code": 2, "msg": "Invalid request: unknown variant %s, expected one of `SUBSCRIBE`, `UNSUBSCRIBE`, `LIST_SUBSCRIPTIONS`, `SET_PROPERTY`, `GET_PROPERTY` at line 1 column 28"} | 错字提醒，或提供的值不是预期类型
{"code": 2, "msg": "Invalid request: too many parameters"}| 数据中提供了不必要参数
{"code": 2, "msg": "Invalid request: property name must be a string"} | 未提供属性名
{"code": 2, "msg": "Invalid request: missing field `method` at line 1 column 73"} | 数据未提供`method`
{"code":3,"msg":"Invalid JSON: expected value at line %s column %s"} | JSON 语法有误.


## 归集交易流


> **Payload:**
```javascript
{
  "e": "aggTrade",  // 事件类型
  "E": 123456789,   // 事件时间
  "s": "BNBBTC",    // 交易对
  "a": 12345,       // 归集交易ID
  "p": "0.001",     // 成交价格
  "q": "100",       // 成交数量
  "f": 100,         // 被归集的首个交易ID
  "l": 105,         // 被归集的末次交易ID
  "T": 123456785,   // 成交时间
  "m": true,        // 买方是否是做市方。如true，则此次成交是一个主动卖出单，否则是一个主动买入单。
}
```

归集交易 stream 推送交易信息，是对单一订单的集合。

**Stream 名称:** `<symbol>@aggTrade`   

**Update Speed:** 实时


## 逐笔交易


> **Payload:**
```javascript
{
  "e": "trade",     // 事件类型
  "E": 123456789,   // 事件时间
  "s": "BNBBTC",    // 交易对
  "t": 12345,       // 交易ID
  "p": "0.001",     // 成交价格
  "q": "100",       // 成交数量
  "T": 123456785,   // 成交时间
  "m": true,        // 买方是否是做市方。如true，则此次成交是一个主动卖出单，否则是一个主动买入单。
}
```

**Stream Name:** `<symbol>@trade`

逐笔交易推送每一笔成交的信息。**成交**，或者说交易的定义是仅有一个吃单者与一个挂单者相互交易


## K线 Streams
> **Payload:**
```javascript
{
  "e": "kline",     // 事件类型
  "E": 123456789,   // 事件时间
  "s": "BNBBTC",    // 交易对
  "k": {
    "t": 123400000, // 这根K线的起始时间
    "T": 123460000, // 这根K线的结束时间
    "s": "BNBBTC",  // 交易对
    "i": "1m",      // K线间隔
    "f": 100,       // 这根K线期间第一笔成交ID
    "L": 200,       // 这根K线期间末一笔成交ID
    "o": "0.0010",  // 这根K线期间第一笔成交价
    "c": "0.0020",  // 这根K线期间末一笔成交价
    "h": "0.0025",  // 这根K线期间最高成交价
    "l": "0.0015",  // 这根K线期间最低成交价
    "v": "1000",    // 这根K线期间成交量
    "n": 100,       // 这根K线期间成交笔数
    "x": false,     // 这根K线是否完结(是否已经开始下一根K线)
    "q": "1.0000",  // 这根K线期间成交额
    "V": "500",     // 主动买入的成交量
    "Q": "0.500",   // 主动买入的成交额
    "B": "123456"   // 忽略此参数
  }
}
```

K线stream逐秒推送所请求的K线种类(最新一根K线)的更新。

**Stream Name:** `<symbol>@kline_<interval>` 
   
**Update Speed:** 2000ms

**K线图间隔参数:**

m -> 分钟; h -> 小时; d -> 天; w -> 周; M -> 月

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


## 按 Symbol 的精简Ticker

> **Payload:**
```javascript
  {
    "e": "24hrMiniTicker",  // 事件类型
    "E": 123456789,         // 事件时间
    "s": "BNBBTC",          // 交易对
    "c": "0.0025",          // 最新成交价格
    "o": "0.0010",          // 24小时前开始第一笔成交价格
    "h": "0.0025",          // 24小时内最高成交价
    "l": "0.0010",          // 24小时内最低成交价
    "v": "10000",           // 成交量
    "q": "18"               // 成交额
  }
```

按Symbol刷新的最近24小时精简ticker信息

**Stream 名称:** `<symbol>@miniTicker`

**Update Speed:** 1000ms


## 全市场所有Symbol的精简Ticker

> **Payload:**
```javascript
[
  {
    // 数组每一个元素对应一个交易对，内容与 \<symbol\>@miniTicker相同
  }
]
```

同上，只是推送所有交易对.需要注意的是，只有更新的ticker才会被推送.

**Stream名称:** !miniTicker@arr

**Update Speed:** 1000ms

## 按Symbol的完整Ticker

> **Payload:**
```javascript
{
  "e": "24hrTicker",  // 事件类型
  "E": 123456789,     // 事件时间
  "s": "BNBBTC",      // 交易对
  "p": "0.0015",      // 24小时价格变化
  "P": "250.00",      // 24小时价格变化(百分比)
  "w": "0.0018",      // 平均价格
  "c": "0.0025",      // 最新成交价格
  "Q": "10",          // 最新成交交易的成交量
  "o": "0.0010",      // 整整24小时前，向后数的第一次成交价格
  "h": "0.0025",      // 24小时内最高成交价
  "l": "0.0010",      // 24小时内最低成交价
  "v": "10000",       // 24小时内成交量
  "q": "18",          // 24小时内成交额
  "O": 0,             // 统计开始时间
  "C": 86400000,      // 统计结束时间
  "F": 0,             // 24小时内第一笔成交交易ID
  "L": 18150,         // 24小时内最后一笔成交交易ID
  "n": 18151          // 24小时内成交数
}
```

每秒推送单个交易对的过去24小时滚动窗口标签统计信息。

**Stream 名称:** `<symbol>@ticker`

**Update Speed:** 1000ms

## 全市场所有交易对的完整Ticker

> **Payload:**
```javascript
[
  {
    // Same as <symbol>@ticker payload
  }
]
```

推送全市场所有交易对刷新的24小时完整ticker信息。需要注意的是，没有更新的ticker不会被推送。

**Stream Name:** `!ticker@arr`

**Update Speed:** 1000ms


## 按Symbol的最优挂单信息

> **Payload:**
```javascript
{
  "u":400900217,     // order book updateId
  "s":"BNBUSDT",     // 交易对
  "b":"25.35190000", // 买单最优挂单价格
  "B":"31.21000000", // 买单最优挂单数量
  "a":"25.36520000", // 卖单最优挂单价格
  "A":"40.66000000"  // 卖单最优挂单数量
}
```

实时推送指定交易对最优挂单信息

**Stream Name:** `<symbol>@bookTicker`

**Update Speed:** 实时

## 全市场最优挂单信息
> **Payload:**
```javascript
{
  // 同 <symbol>@bookTicker payload
}
```

实时推送所有交易对最优挂单信息

**Stream Name:** `!bookTicker`

**Update Speed:** 实时


## 有限档深度信息

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

每秒或每100毫秒推送有限档深度信息。levels表示几档买卖单信息, 可选 5/10/20档

**Stream Names:** `<symbol>@depth<levels>` 或 `<symbol>@depth<levels>@100ms`.  

**Update Speed:** 1000ms 或 100ms


## 增量深度信息
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

每秒或每100毫秒推送orderbook的变化部分(如果有)

**Stream Name:** `<symbol>@depth` 或 `<symbol>@depth@100ms`

**Update Speed:** 1000ms 或 100ms

## 如何正确在本地维护一个orderbook副本
1. 订阅 **wss://sstream.asterdex.com/ws/bnbbtc@depth**
2. 开始缓存收到的更新。同一个价位，后收到的更新覆盖前面的。
3. 访问Rest接口 **https://sapi.asterdex.com/api/v1/depth?symbol=BNBBTC&limit=1000** 获得一个1000档的深度快照
4. 将目前缓存到的信息中`u` <= 步骤3中获取到的快照中的`lastUpdateId`的部分丢弃(丢弃更早的信息，已经过期)。
5. 将深度快照中的内容更新到本地orderbook副本中，并从websocket接收到的第一个`U` <= `lastUpdateId`+1 **且** `u` >= `lastUpdateId`+1 的event开始继续更新本地副本。
6. 每一个新event的`U`应该恰好等于上一个event的`u`+1，否则可能出现了丢包，请从step3重新进行初始化。
7. 每一个event中的挂单量代表这个价格目前的挂单量**绝对值**，而不是相对变化。
8. 如果某个价格对应的挂单量为0，表示该价位的挂单已经撤单或者被吃，应该移除这个价位。






# Websocket账户信息推送

* 本篇所列出API接口的base url : **https://sapi.asterdex.com**
* 用于订阅账户数据的 `listenKey` 从创建时刻起有效期为60分钟
* 可以通过 `PUT` 一个 `listenKey` 延长60分钟有效期
* 可以通过`DELETE`一个 `listenKey` 立即关闭当前数据流，并使该`listenKey` 无效
* 在具有有效`listenKey`的帐户上执行`POST`将返回当前有效的`listenKey`并将其有效期延长60分钟
* websocket接口的baseurl: **wss://sstream.asterdex.com**
* U订阅账户数据流的stream名称为 **/ws/\<listenKey\>**
* 每个链接有效期不超过24小时，请妥善处理断线重连。


## Listen Key(现货账户)

### 生成 Listen Key (USER_STREAM)

> **响应**
```javascript
{
  "listenKey": "pqia91ma19a5s61cv6a81va65sdf19v8a65a1a5s61cv6a81va65sdf19v8a65a1"
}
```

``
POST /api/v1/listenKey
``

开始一个新的数据流。除非发送 keepalive，否则数据流于60分钟后关闭。如果该帐户具有有效的`listenKey`，则将返回该`listenKey`并将其有效期延长60分钟。

**权重:**
1

**参数:**
NONE

### 延长 Listen Key 有效期 (USER_STREAM)

> **响应**
```javascript
{}
```

``
PUT /api/v1/listenKey 
``

有效期延长至本次调用后60分钟,建议每30分钟发送一个 ping 。

**权重:**
1

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
listenKey | STRING | YES


### 关闭 Listen Key (USER_STREAM)

> **响应**
```javascript
{}
```

``
DELETE /api/v1/listenKey
``

关闭用户数据流。

**权重:**
1

**参数:**

名称 | 类型 | 是否必需 | 描述
------------ | ------------ | ------------ | ------------
listenKey | STRING | YES


## Payload: 账户更新

每当帐户余额发生更改时，都会发送一个事件`outboundAccountPosition`，其中包含可能由生成余额变动的事件而变动的资产。

> **Payload**
```javascript
{
  "B":[// 余额
    {
      "a":"SLP25",   // 资产名称
      "f":"10282.42029415",   // 可用余额
      "l":"653.00000001"   // 冻结余额
    },
    {
      "a":"ADA25",
      "f":"9916.96229880",
      "l":"34.00510000"
    }
  ],
  "e":"outboundAccountPosition",   // 事件类型
  "T":1649926447190,     // 账户末次更新时间戳 
  "E":1649926447205   // 事件时间
  "m":"WITHDRAW" // 事件推出原因
}
```


## Payload: 订单更新

订单通过`executionReport`事件进行更新。 

> **Payload**

```javascript
{
  "s":"ADA25SLP25",   // 交易对
  "c":"Xzh0gnxT41PStbwqOtXnjD",  // 客户端自定订单ID
  "S":"SELL",   // 订单方向
  "o":"LIMIT",   // 订单类型
  "f":"GTC",   // 有效方式
  "q":"10.001000",   // 订单原始数量
  "p":"19.1000000000",   // 订单原始价格
  "ap":"19.0999999955550656",  //平均价格
  "P":"0",  // 条件订单触发价格
  "x":"TRADE",   // 本次事件的具体执行类型
  "X":"PARTIALLY_FILLED",   // 订单的当前状态
  "i":27,   // 订单ID
  "l":"1",      // 订单末次成交量 
  "z":"8.999000",   // 订单累计已成交量
  "L":"19.1000000000",   // 订单末次成交价格
  "n":"0.00382000",    // 手续费数量    
  "N":"SLP25",   // 手续费资产类型
  "T":1649926447190,   // 成交时间
  "t":18,   // 成交ID
  "m":true,   // 该成交是作为挂单成交吗？
  "ot":"LIMIT",  //初始订单类型
  "O":0,   // 订单时间
  "Z":"171.88089996",   // 累计报价资产交易数量
  "Y":"19.1000000000000000",   // 最近报价交易数量
  "Q":"0",   // 报价数量
  "e":"executionReport",   // 事件类型
  "E":1649926447209  // 事件时间
}  
```


**执行类型:**
* NEW 新订单
* CANCELED 订单被取消
* REJECTED 新订单被拒绝
* TRADE 订单有新成交
* EXPIRED 订单失效(根据订单的Time In Force参数)






#错误代码

> error JSON payload:
 
```javascript
{
  "code":-1121,
  "msg":"Invalid symbol."
}
```

错误由两部分组成：错误代码和消息。 代码是通用的，但是消息可能会有所不同。


## 10xx - 常规服务器或网络问题
### -1000 UNKNOWN
 * An unknown error occured while processing the request.
 * 处理请求时发生未知错误。

### -1001 DISCONNECTED
 * Internal error; unable to process your request. Please try again.
 * 内部错误; 无法处理您的请求。 请再试一次.

### -1002 UNAUTHORIZED
 * You are not authorized to execute this request.
 * 您无权执行此请求。

### -1003 TOO_MANY_REQUESTS
 * Too many requests queued.
 * 排队的请求过多。
 * Too many requests; please use the websocket for live updates.
 * 请求权重过多； 请使用websocket获取最新更新。
 * Too many requests; current limit is %s requests per minute. Please use the websocket for live updates to avoid polling the API.
 * 请求权重过多； 当前限制为每分钟％s请求权重。 请使用websocket进行实时更新，以避免轮询API。
 * Way too many requests; IP banned until %s. Please use the websocket for live updates to avoid bans.
 * 请求权重过多； IP被禁止，直到％s。 请使用websocket进行实时更新，以免被禁。
 
### -1004 DUPLICATE_IP
 * This IP is already on the white list
 * IP地址已经在白名单

### -1005 NO_SUCH_IP
 * No such IP has been white listed
 * 白名单上没有此IP地址
 
### -1006 UNEXPECTED_RESP
 * An unexpected response was received from the message bus. Execution status unknown.
 * 从消息总线收到意外的响应。执行状态未知。

### -1007 TIMEOUT
 * Timeout waiting for response from backend server. Send status unknown; execution status unknown.
 * 等待后端服务器响应超时。 发送状态未知； 执行状态未知。

### -1014 UNKNOWN_ORDER_COMPOSITION
 * Unsupported order combination.
 * 不支持当前的下单参数组合

### -1015 TOO_MANY_ORDERS
 * Too many new orders.
 * 新订单太多。
 * Too many new orders; current limit is %s orders per %s.
 * 新订单太多； 当前限制为每％s ％s个订单。

### -1016 SERVICE_SHUTTING_DOWN
 * This service is no longer available.
 * 该服务不可用。

### -1020 UNSUPPORTED_OPERATION
 * This operation is not supported.
 * 不支持此操作。

### -1021 INVALID_TIMESTAMP
 * Timestamp for this request is outside of the recvWindow.
  * 此请求的时间戳在recvWindow之外。
 * Timestamp for this request was 1000ms ahead of the server's time.
 * 此请求的时间戳比服务器时间提前1000毫秒。

### -1022 INVALID_SIGNATURE
 * Signature for this request is not valid.
 * 此请求的签名无效。

### -1023 START_TIME_GREATER_THAN_END_TIME
 * Start time is greater than end time.
 * 参数里面的开始时间在结束时间之后


## 11xx - Request issues
### -1100 ILLEGAL_CHARS
 * Illegal characters found in a parameter.
 * 在参数中发现非法字符。
 * Illegal characters found in parameter '%s'; legal range is '%s'.
 * 在参数`％s`中发现非法字符； 合法范围是`％s`。

### -1101 TOO_MANY_PARAMETERS
 * Too many parameters sent for this endpoint.
 * 为此端点发送的参数太多。
 * Too many parameters; expected '%s' and received '%s'.
 * 参数太多；预期为`％s`并收到了`％s`。
 * Duplicate values for a parameter detected.
 * 检测到的参数值重复。

### -1102 MANDATORY_PARAM_EMPTY_OR_MALFORMED
 * A mandatory parameter was not sent, was empty/null, or malformed.
 * 未发送强制性参数，该参数为空/空或格式错误。
 * Mandatory parameter '%s' was not sent, was empty/null, or malformed.
 * 强制参数`％s`未发送，为空/空或格式错误。
 * Param '%s' or '%s' must be sent, but both were empty/null!
 * 必须发送参数`％s`或`％s`，但两者均为空！

### -1103 UNKNOWN_PARAM
 * An unknown parameter was sent.
 * 发送了未知参数。

### -1104 UNREAD_PARAMETERS
 * Not all sent parameters were read.
 * 并非所有发送的参数都被读取。
 * Not all sent parameters were read; read '%s' parameter(s) but was sent '%s'.
 * 并非所有发送的参数都被读取； 读取了`％s`参数，但被发送了`％s`。

### -1105 PARAM_EMPTY
 * A parameter was empty.
 * 参数为空。
 * Parameter '%s' was empty.
 * 参数`％s`为空。

### -1106 PARAM_NOT_REQUIRED
 * A parameter was sent when not required.
 * 发送了不需要的参数。
 * Parameter '%s' sent when not required.
 * 发送了不需要参数`％s`。

### -1111 BAD_PRECISION
 * Precision is over the maximum defined for this asset.
 * 精度超过为此资产定义的最大值。

### -1112 NO_DEPTH
 * No orders on book for symbol.
 * 交易对没有挂单。
 
### -1114 TIF_NOT_REQUIRED
 * TimeInForce parameter sent when not required.
 * 发送的`TimeInForce`参数不需要。

### -1115 INVALID_TIF
 * Invalid timeInForce.
 * 无效的`timeInForce`

### -1116 INVALID_ORDER_TYPE
 * Invalid orderType.
 * 无效订单类型。

### -1117 INVALID_SIDE
 * Invalid side.
 * 无效买卖方向。

### -1118 EMPTY_NEW_CL_ORD_ID
 * New client order ID was empty.
 * 新的客户订单ID为空。

### -1119 EMPTY_ORG_CL_ORD_ID
 * Original client order ID was empty.
 * 客户自定义的订单ID为空。

### -1120 BAD_INTERVAL
 * Invalid interval.
 * 无效时间间隔。

### -1121 BAD_SYMBOL
 * Invalid symbol.
 * 无效的交易对。

### -1125 INVALID_LISTEN_KEY
 * This listenKey does not exist.
 * 此`listenKey`不存在。

### -1127 MORE_THAN_XX_HOURS
 * Lookup interval is too big.
 * 查询间隔太大。
 * More than %s hours between startTime and endTime.
 * 从开始时间到结束时间之间超过`％s`小时。

### -1128 OPTIONAL_PARAMS_BAD_COMBO
 * Combination of optional parameters invalid.
 * 可选参数组合无效。

### -1130 INVALID_PARAMETER
 * Invalid data sent for a parameter.
 * 发送的参数为无效数据。
 * Data sent for parameter '%s' is not valid.
 * 发送参数`％s`的数据无效。

### -1136 INVALID_NEW_ORDER_RESP_TYPE
 * Invalid newOrderRespType.
 * 无效的 newOrderRespType。


## 20xx - Processing Issues
### -2010 NEW_ORDER_REJECTED
 * NEW_ORDER_REJECTED
 * 新订单被拒绝

### -2011 CANCEL_REJECTED
 * CANCEL_REJECTED
 * 取消订单被拒绝

### -2013 NO_SUCH_ORDER
 * Order does not exist.
 * 订单不存在。

### -2014 BAD_API_KEY_FMT
 * API-key format invalid.
 * API-key 格式无效。

### -2015 REJECTED_MBX_KEY
 * Invalid API-key, IP, or permissions for action.
 * 无效的API密钥，IP或操作权限。

### -2016 NO_TRADING_WINDOW
 * No trading window could be found for the symbol. Try ticker/24hrs instead.
 * 找不到该交易对的交易窗口。 尝试改为24小时自动报价。

### -2018 BALANCE_NOT_SUFFICIENT
 * Balance is insufficient.
 * 余额不足

### -2020 UNABLE_TO_FILL
 * Unable to fill.
 * 无法成交

### -2021 ORDER_WOULD_IMMEDIATELY_TRIGGER
 * Order would immediately trigger.
 * 订单可能被立刻触发

### -2022 REDUCE_ONLY_REJECT
 * ReduceOnly Order is rejected.
 * `ReduceOnly`订单被拒绝

### -2024 POSITION_NOT_SUFFICIENT
 * Position is not sufficient.
 * 持仓不足

### -2025 MAX_OPEN_ORDER_EXCEEDED
 * Reach max open order limit.
 * 挂单量达到上限

### -2026 REDUCE_ONLY_ORDER_TYPE_NOT_SUPPORTED
 * This OrderType is not supported when reduceOnly.
 * 当前订单类型不支持`reduceOnly`

## 40xx - Filters and other Issues
### -4000 INVALID_ORDER_STATUS
 * Invalid order status.
 * 订单状态不正确

### -4001 PRICE_LESS_THAN_ZERO
 * Price less than 0.
 * 价格小于0

### -4002 PRICE_GREATER_THAN_MAX_PRICE
 * Price greater than max price.
 * 价格超过最大值
 
### -4003 QTY_LESS_THAN_ZERO
 * Quantity less than zero.
 * 数量小于0

### -4004 QTY_LESS_THAN_MIN_QTY
 * Quantity less than min quantity.
 * 数量小于最小值
 
### -4005 QTY_GREATER_THAN_MAX_QTY
 * Quantity greater than max quantity.
 * 数量大于最大值

### -4006 STOP_PRICE_LESS_THAN_ZERO
 * Stop price less than zero. 
 * 触发价小于最小值
 
### -4007 STOP_PRICE_GREATER_THAN_MAX_PRICE
 * Stop price greater than max price.
 * 触发价大于最大值

### -4008 TICK_SIZE_LESS_THAN_ZERO
 * Tick size less than zero.
 * 价格精度小于0

### -4009 MAX_PRICE_LESS_THAN_MIN_PRICE
 * Max price less than min price.
 * 最大价格小于最小价格

### -4010 MAX_QTY_LESS_THAN_MIN_QTY
 * Max qty less than min qty.
 * 最大数量小于最小数量

### -4011 STEP_SIZE_LESS_THAN_ZERO
 * Step size less than zero.
 * 步进值小于0

### -4012 MAX_NUM_ORDERS_LESS_THAN_ZERO
 * Max num orders less than zero.
 * 最大订单量小于0

### -4013 PRICE_LESS_THAN_MIN_PRICE
 * Price less than min price.
 * 价格小于最小价格

### -4014 PRICE_NOT_INCREASED_BY_TICK_SIZE
 * Price not increased by tick size.
 * 价格增量不是价格精度的倍数。
 
### -4015 INVALID_CL_ORD_ID_LEN
 * Client order id is not valid.
 * 客户订单ID有误。
 * Client order id length should not be more than 36 chars
 * 客户订单ID长度应该不多于36字符

### -4016 PRICE_HIGHTER_THAN_MULTIPLIER_UP
 * Price is higher than mark price multiplier cap.

### -4017 MULTIPLIER_UP_LESS_THAN_ZERO
 * Multiplier up less than zero.
 * 价格上限小于0

### -4018 MULTIPLIER_DOWN_LESS_THAN_ZERO
 * Multiplier down less than zero.
 * 价格下限小于0

### -4019 COMPOSITE_SCALE_OVERFLOW
 * Composite scale too large.

### -4020 TARGET_STRATEGY_INVALID
 * Target strategy invalid for orderType '%s',reduceOnly '%b'.
 * 目标策略值不适合`%s`订单状态, 只减仓`%b`。

### -4021 INVALID_DEPTH_LIMIT
 * Invalid depth limit.
 * 深度信息的`limit`值不正确。
 * '%s' is not valid depth limit.
 * `%s`不是合理的深度信息的`limit`值。

### -4022 WRONG_MARKET_STATUS
 * market status sent is not valid.
 * 发送的市场状态不正确。
 
### -4023 QTY_NOT_INCREASED_BY_STEP_SIZE
 * Qty not increased by step size.
 * 数量的递增值不是步进值的倍数。

### -4024 PRICE_LOWER_THAN_MULTIPLIER_DOWN
 * Price is lower than mark price multiplier floor.

### -4025 MULTIPLIER_DECIMAL_LESS_THAN_ZERO
 * Multiplier decimal less than zero.

### -4026 COMMISSION_INVALID
 * Commission invalid.
 * 收益值不正确
 * `%s` less than zero.
 * `%s`少于0
 * `%s` absolute value greater than `%s`
 * `%s`绝对值大于`%s`

### -4027 INVALID_ACCOUNT_TYPE
 * Invalid account type.
 * 账户类型不正确。

### -4029 INVALID_TICK_SIZE_PRECISION
 * Tick size precision is invalid.
 * 价格精度小数点位数不正确。

### -4030 INVALID_STEP_SIZE_PRECISION
 * Step size precision is invalid.
 * 步进值小数点位数不正确。

### -4031 INVALID_WORKING_TYPE
 * Invalid parameter working type
 * 不正确的参数类型
 * Invalid parameter working type: `%s`
 * 不正确的参数类型: `%s`

### -4032 EXCEED_MAX_CANCEL_ORDER_SIZE
 * Exceed maximum cancel order size.
 * 超过可以取消的最大订单量。
 * Invalid parameter working type: `%s`
 * 不正确的参数类型: `%s`

### -4044 INVALID_BALANCE_TYPE
 * Balance Type is invalid.
 * 余额类型不正确。

### -4045 MAX_STOP_ORDER_EXCEEDED
 * Reach max stop order limit.
 * 达到止损单的上限。

### -4055 AMOUNT_MUST_BE_POSITIVE
 * Amount must be positive.
 * 数量必须是正整数

### -4056 INVALID_API_KEY_TYPE
 * Invalid api key type.
 * API key的类型不正确

### -4057 INVALID_RSA_PUBLIC_KEY
 * Invalid api public key
 * API key不正确

### -4058 MAX_PRICE_TOO_LARGE
 * maxPrice and priceDecimal too large,please check.
 * maxPrice和priceDecimal太大，请检查。

### -4060 INVALID_POSITION_SIDE
 * Invalid position side.
 * 仓位方向不正确。

### -4061 POSITION_SIDE_NOT_MATCH
 * Order's position side does not match user's setting.
 * 订单的持仓方向和用户设置不一致。

### -4062 REDUCE_ONLY_CONFLICT
 * Invalid or improper reduceOnly value.
 * 仅减仓的设置不正确。

### -4084 UPCOMING_METHOD
 * Method is not allowed currently. Upcoming soon.
 * 方法不支持

### -4086 INVALID_PRICE_SPREAD_THRESHOLD
 * Invalid price spread threshold
 * 无效的价差阀值
 
### -4087 REDUCE_ONLY_ORDER_PERMISSION
 * User can only place reduce only order
 * 用户只能下仅减仓订单

### -4088 NO_PLACE_ORDER_PERMISSION
 * User can not place order currently
 * 用户当前不能下单

### -4114 INVALID_CLIENT_TRAN_ID_LEN
 * clientTranId  is not valid
 * clientTranId不正确
 * Client tran id length should be less than 64 chars
 * 客户的tranId长度应该小于64个字符

### -4115 DUPLICATED_CLIENT_TRAN_ID
 * clientTranId  is duplicated
 *  clientTranId重复
 * Client tran id should be unique within 7 days
 * 客户的tranId应在7天内唯一

### -4118 REDUCE_ONLY_MARGIN_CHECK_FAILED
 * ReduceOnly Order Failed. Please check your existing position and open orders
 * 仅减仓订单失败。请检查现有的持仓和挂单
 
### -4131 MARKET_ORDER_REJECT
 * The counterparty's best price does not meet the PERCENT_PRICE filter limit
 * 交易对手的最高价格未达到PERCENT_PRICE过滤器限制

### -4135 INVALID_ACTIVATION_PRICE
 * Invalid activation price
 * 无效的激活价格

### -4137 QUANTITY_EXISTS_WITH_CLOSE_POSITION
 * Quantity must be zero with closePosition equals true
 * 数量必须为0，当closePosition为true时

### -4138 REDUCE_ONLY_MUST_BE_TRUE
 * Reduce only must be true with closePosition equals true
 * Reduce only 必须为true，当closePosition为true时

### -4139 ORDER_TYPE_CANNOT_BE_MKT
 * Order type can not be market if it's unable to cancel
 * 订单类型不能为市价单如果不能取消

### -4140 INVALID_OPENING_POSITION_STATUS
 * Invalid symbol status for opening position
 * 无效的交易对状态

### -4141 SYMBOL_ALREADY_CLOSED
 * Symbol is closed
 * 交易对已下架

### -4142 STRATEGY_INVALID_TRIGGER_PRICE
 * REJECT: take profit or stop order will be triggered immediately
 * 拒绝：止盈止损单将立即被触发

### -4164 MIN_NOTIONAL
 * Order's notional must be no smaller than 5.0 (unless you choose reduce only)
 *  订单的名义价值不可以小于5，除了使用reduce only
 * Order's notional must be no smaller than %s (unless you choose reduce only)
 *  订单的名义价值不可以小于`%s`，除了使用reduce only

### -4165 INVALID_TIME_INTERVAL
 * Invalid time interval
 * 无效的间隔
 * Maximum time interval is %s days
 * 最大的时间间隔为 `%s` 天

### -4183 PRICE_HIGHTER_THAN_STOP_MULTIPLIER_UP
 * Price is higher than stop price multiplier cap.
 * 止盈止损订单价格不应高于触发价与报价乘数上限的乘积
 * Limit price can't be higher than %s.
 * 止盈止损订单价格不应高于 `%s`

### -4184 PRICE_LOWER_THAN_STOP_MULTIPLIER_DOWN
 * Price is lower than stop price multiplier floor.
 * 止盈止损订单价格不应低于触发价与报价乘数下限的乘积
 * Limit price can't be lower than %s.
 * 止盈止损订单价格不应低于 `%s`f
