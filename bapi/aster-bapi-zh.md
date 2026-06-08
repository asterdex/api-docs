# AsterDex BAPI 接口文档

> **Base URL**
> - 综合 / 公告模块：`https://www.asterdex.com`
> - 合约 / 投资组合模块：`https://asterdex.com/bapi/futures`
>
> **鉴权说明**
> - `public` 接口 — 无需鉴权
> - `private` 接口 — 需携带有效用户登录态 / 鉴权请求头

---

## 目录

- [公告模块](#公告模块)
  - [Public — 获取单条公告](#1-获取单条公告)
  - [Public — 分页搜索公告](#2-分页搜索公告)
- [投资组合模块](#投资组合模块)
  - [Private — Pro 汇总数据](#3-pro-汇总数据)
  - [Private — 投资组合折线图](#4-投资组合折线图)
  - [Private — 投资组合日历](#5-投资组合日历)
- [附录](#附录)

---

# 公告模块

## 公共响应对象 — `AnnouncementResp`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `Long` | 公告 ID |
| `category` | `String` | 分类，见下方枚举 |
| `title` | `String` | 标题 |
| `subtitle` | `String` | 副标题 |
| `content` | `String` | 正文内容 |
| `publishTime` | `Date` | 发布时间（毫秒时间戳） |
| `jumpLink` | `String` | 详情页跳转链接 |

**category 枚举值**

| 值 | 说明 |
|----|------|
| `ACTIVITY` | 活动公告 |
| `NEW_LISTING` | 新币上线 |
| `DELISTING` | 下架公告 |
| `UPDATES` | 更新公告 |

---

## 1. 获取单条公告

**`PUBLIC`** `GET /bapi/composite/v1/public/composite/ae/announcement/get`

根据 ID 获取单条公告详情。

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | `Long` | 是 | 公告 ID |

**请求示例**

```bash
curl -X GET "https://www.asterdex.com/bapi/composite/v1/public/composite/ae/announcement/get?id=12345"
```

**响应示例**

```json
{
  "code": "000000",
  "message": null,
  "data": {
    "id": 12345,
    "category": "NEW_LISTING",
    "title": "AsterDex Will List XYZ Token",
    "subtitle": "XYZ/USDT Trading Pair Now Available",
    "content": "AsterDex is pleased to announce the listing of XYZ Token...",
    "publishTime": 1717545600000,
    "jumpLink": "https://www.asterdex.com/en/support/announcement/detail/12345"
  },
  "success": true
}
```

---

## 2. 分页搜索公告

**`PUBLIC`** `POST /bapi/composite/v1/public/composite/ae/announcement/search`

分页查询公告列表，支持按分类筛选。

**请求体**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `page` | `Integer` | 是 | 页码（从 1 开始） |
| `size` | `Integer` | 是 | 每页条数 |
| `category` | `String` | 否 | 公告分类，不传则返回所有分类 |

**请求示例**

查询所有分类，第 1 页，每页 10 条：

```bash
curl -X POST "https://www.asterdex.com/bapi/composite/v1/public/composite/ae/announcement/search" \
  -H "Content-Type: application/json" \
  -d '{
    "page": 1,
    "size": 10
  }'
```

按分类筛选（新币上线）：

```bash
curl -X POST "https://www.asterdex.com/bapi/composite/v1/public/composite/ae/announcement/search" \
  -H "Content-Type: application/json" \
  -d '{
    "page": 1,
    "size": 10,
    "category": "NEW_LISTING"
  }'
```

**响应** — `SearchResult<AnnouncementResp>`

| 字段 | 类型 | 说明 |
|------|------|------|
| `total` | `Long` | 总条数 |
| `rows` | `List<AnnouncementResp>` | 公告列表 |

**响应示例**

```json
{
  "code": "000000",
  "message": null,
  "data": {
    "total": 128,
    "rows": [
      {
        "id": 12345,
        "category": "NEW_LISTING",
        "title": "AsterDex Will List XYZ Token",
        "subtitle": "XYZ/USDT Trading Pair Now Available",
        "content": "AsterDex is pleased to announce the listing of XYZ Token...",
        "publishTime": 1717545600000,
        "jumpLink": "https://www.asterdex.com/en/support/announcement/detail/12345"
      }
    ]
  },
  "success": true
}
```

---

# 投资组合模块

> Base URL：`https://asterdex.com/bapi/futures`
> 所有投资组合接口均为 **private**，需要用户登录态。

---

## 3. Pro 汇总数据

**`PRIVATE`** `POST /v1/private/campaign/portfolio/summary/pro`

查询 Pro 投资组合在指定时间段内的交易汇总统计，包括资金费率、手续费、多空交易次数 / 量及网格策略数据。

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `period` | `String` | 否 | 统计周期，枚举值：`24h`、`7d`、`14d`、`30d`、`all`，不传默认全部时间 |

**响应** — `ProSummaryResp`

| 字段 | 类型 | 说明 |
|------|------|------|
| `fundingFee` | `BigDecimal` | 周期内累计资金费 |
| `latestFundingFee` | `BigDecimal` | 最近一次资金费 |
| `totalCommission` | `BigDecimal` | 周期内累计手续费 |
| `latestCommission` | `BigDecimal` | 最近一次手续费 |
| `totalTradeCount` | `Long` | 总交易笔数 |
| `longTradeCount` | `Long` | 做多交易笔数 |
| `shortTradeCount` | `Long` | 做空交易笔数 |
| `totalTradeVol` | `BigDecimal` | 总交易量 |
| `longTradeVol` | `BigDecimal` | 做多交易量 |
| `shortTradeVol` | `BigDecimal` | 做空交易量 |
| `latestUpdated` | `Date` | 数据最后更新时间 |
| `periodStart` | `Date` | 统计周期开始时间 |
| `periodEnd` | `Date` | 统计周期结束时间 |
| `gridTotalCommission` | `BigDecimal` | 网格策略累计手续费 |
| `gridLatestCommission` | `BigDecimal` | 网格策略最近一次手续费 |
| `gridTotalTradeCount` | `Long` | 网格策略总交易笔数 |
| `gridLongTradeCount` | `Long` | 网格策略做多交易笔数 |
| `gridShortTradeCount` | `Long` | 网格策略做空交易笔数 |
| `gridTotalTradeVol` | `BigDecimal` | 网格策略总交易量 |
| `gridLongTradeVol` | `BigDecimal` | 网格策略做多交易量 |
| `gridShortTradeVol` | `BigDecimal` | 网格策略做空交易量 |
| `gridLatestUpdated` | `Date` | 网格数据最后更新时间 |
| `gridPeriodStart` | `Date` | 网格统计周期开始时间 |
| `gridPeriodEnd` | `Date` | 网格统计周期结束时间 |

**请求示例**

```json
{
  "period": "7d"
}
```

**响应示例**

```json
{
  "code": "000000",
  "data": {
    "fundingFee": "12.34",
    "latestFundingFee": "0.56",
    "totalCommission": "5.00",
    "latestCommission": "0.10",
    "totalTradeCount": 200,
    "longTradeCount": 120,
    "shortTradeCount": 80,
    "totalTradeVol": "500000.00",
    "longTradeVol": "300000.00",
    "shortTradeVol": "200000.00",
    "latestUpdated": "2026-06-08T00:00:00Z",
    "periodStart": "2026-06-01T00:00:00Z",
    "periodEnd": "2026-06-08T00:00:00Z",
    "gridTotalCommission": "1.00",
    "gridLatestCommission": "0.05",
    "gridTotalTradeCount": 50,
    "gridLongTradeCount": 25,
    "gridShortTradeCount": 25,
    "gridTotalTradeVol": "100000.00",
    "gridLongTradeVol": "50000.00",
    "gridShortTradeVol": "50000.00",
    "gridLatestUpdated": "2026-06-08T00:00:00Z",
    "gridPeriodStart": "2026-06-01T00:00:00Z",
    "gridPeriodEnd": "2026-06-08T00:00:00Z"
  }
}
```

---

## 4. 投资组合折线图

**`PRIVATE`** `POST /v1/private/campaign/portfolio/overview/v2/line/chart`

查询投资组合资产曲线的时序数据，按合约、现货、Staking 等维度拆分余额和盈亏，用于渲染多折线图表。

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `period` | `String` | 否 | 统计周期，枚举值：`24h`、`7d`、`14d`、`30d`、`all` |

**响应** — `List<PortfolioLineChartResp>`

| 字段 | 类型 | 说明 |
|------|------|------|
| `dt` | `String` | 数据点时间标签 |
| `balance` | `BigDecimal` | 该时间点总资产余额 |
| `pnl` | `BigDecimal` | 该时间点总盈亏 |
| `perpBalance` | `BigDecimal` | 永续合约账户余额 |
| `perpPnl` | `BigDecimal` | 永续合约盈亏 |
| `perpTradePnl` | `BigDecimal` | 永续合约已实现交易盈亏 |
| `shieldTradePnl` | `BigDecimal` | Shield 策略已实现交易盈亏 |
| `spotBalance` | `BigDecimal` | 现货账户余额 |
| `spotPnl` | `BigDecimal` | 现货盈亏 |
| `stakingBalance` | `BigDecimal` | Staking 余额 |
| `stakingPnl` | `BigDecimal` | Staking 盈亏 |
| `predictionPnl` | `BigDecimal` | 预测（Earn）盈亏 |
| `allSPnl` | `BigDecimal` | 现货 + 预测盈亏合计 |
| `period` | `String` | 该数据点对应的周期枚举值 |
| `futureUid` | `Long` | 用户合约 UID |

**请求示例**

```json
{
  "period": "30d"
}
```

**响应示例**

```json
{
  "code": "000000",
  "data": [
    {
      "dt": "2026-05-09",
      "balance": "10000.00",
      "pnl": "200.00",
      "perpBalance": "7000.00",
      "perpPnl": "150.00",
      "perpTradePnl": "100.00",
      "shieldTradePnl": "20.00",
      "spotBalance": "2000.00",
      "spotPnl": "30.00",
      "stakingBalance": "1000.00",
      "stakingPnl": "20.00",
      "predictionPnl": "10.00",
      "allSPnl": "40.00",
      "period": "30d",
      "futureUid": 123456789
    }
  ]
}
```

---

## 5. 投资组合日历

**`PRIVATE`** `POST /v1/private/campaign/portfolio/overview/line/calendar`

按指定日期范围查询每日粒度的投资组合数据，用于渲染日历视图或自定义日期区间折线图。与基于周期的折线图不同，本接口按明确的起止日期查询。

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `startDate` | `String` | **是** | 起始日期（含），格式：`yyyy-MM-dd` |
| `endDate` | `String` | **是** | 结束日期（含），格式：`yyyy-MM-dd` |

**响应** — `List<PortfolioLineChartResp>`

结构与[投资组合折线图](#4-投资组合折线图)一致，`dt` 字段格式为 `yyyy-MM-dd`。

**请求示例**

```json
{
  "startDate": "2026-05-01",
  "endDate": "2026-05-31"
}
```

**响应示例**

```json
{
  "code": "000000",
  "data": [
    {
      "dt": "2026-05-01",
      "balance": "9800.00",
      "pnl": "-20.00",
      "perpBalance": "6800.00",
      "perpPnl": "-30.00",
      "perpTradePnl": "-25.00",
      "shieldTradePnl": "5.00",
      "spotBalance": "2000.00",
      "spotPnl": "10.00",
      "stakingBalance": "1000.00",
      "stakingPnl": "0.00",
      "predictionPnl": "0.00",
      "allSPnl": "10.00",
      "period": null,
      "futureUid": 123456789
    }
  ]
}
```

**错误场景**

| 场景 | 行为 |
|------|------|
| `startDate` 或 `endDate` 缺失 | 返回校验错误（400） |
| 日期范围过大 | 建议单次查询不超过 90 天 |

---

# 附录

## 周期枚举值

| 枚举值 | 字符串值 | 说明 |
|--------|---------|------|
| `H_24` | `24h` | 近 24 小时 |
| `D_7` | `7d` | 近 7 天 |
| `D_14` | `14d` | 近 14 天 |
| `D_30` | `30d` | 近 30 天 |
| `ALLTIME` | `all` | 全部时间 |

## 通用响应结构

所有接口均返回统一的响应包装：

```json
{
  "code": "000000",
  "message": null,
  "data": { ... },
  "success": true
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | `String` | `"000000"` 表示成功 |
| `message` | `String` | 错误信息，成功时为 `null` |
| `data` | `Object` | 业务响应数据 |
| `success` | `Boolean` | 成功时为 `true` |
