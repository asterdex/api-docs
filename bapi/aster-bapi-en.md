# AsterDex BAPI Documentation

> **Base URLs**
> - Composite / Announcement: `https://www.asterdex.com`
> - Futures / Portfolio: `https://asterdex.com/bapi/futures`
>
> **Authentication**
> - `public` endpoints — no authentication required
> - `private` endpoints — require valid user session / auth headers

---

## Table of Contents

- [Announcement Module](#announcement-module)
  - [Public — Get Announcement](#1-get-announcement)
  - [Public — Search Announcements](#2-search-announcements)
- [Portfolio Module](#portfolio-module)
  - [Private — Pro Summary](#3-pro-summary)
  - [Private — Portfolio Line Chart](#4-portfolio-line-chart)
  - [Private — Portfolio Line Calendar](#5-portfolio-line-calendar)
- [Appendix](#appendix)

---

# Announcement Module

## Common Response Object — `AnnouncementResp`

| Field | Type | Description |
|-------|------|-------------|
| `id` | `Long` | Announcement ID |
| `category` | `String` | Category, see enum values below |
| `title` | `String` | Title |
| `subtitle` | `String` | Subtitle |
| `content` | `String` | Body content |
| `publishTime` | `Date` | Publish time (Unix timestamp in milliseconds) |
| `jumpLink` | `String` | Detail page URL |

**Category Enum**

| Value | Description |
|-------|-------------|
| `ACTIVITY` | Activity announcements |
| `NEW_LISTING` | New token listings |
| `DELISTING` | Delisting notices |
| `UPDATES` | Platform updates |

---

## 1. Get Announcement

**`PUBLIC`** `GET /bapi/composite/v1/public/composite/ae/announcement/get`

Retrieve a single announcement by ID.

**Request Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | `Long` | Yes | Announcement ID |

**Request Example**

```bash
curl -X GET "https://www.asterdex.com/bapi/composite/v1/public/composite/ae/announcement/get?id=12345"
```

**Response Example**

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

## 2. Search Announcements

**`PUBLIC`** `POST /bapi/composite/v1/public/composite/ae/announcement/search`

Paginated search for announcements with optional category filtering.

**Request Body**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page` | `Integer` | Yes | Page number (starts from 1) |
| `size` | `Integer` | Yes | Number of items per page |
| `category` | `String` | No | Announcement category; returns all categories if omitted |

**Request Examples**

Fetch all categories, page 1, 10 items per page:

```bash
curl -X POST "https://www.asterdex.com/bapi/composite/v1/public/composite/ae/announcement/search" \
  -H "Content-Type: application/json" \
  -d '{
    "page": 1,
    "size": 10
  }'
```

Filter by category (`NEW_LISTING`):

```bash
curl -X POST "https://www.asterdex.com/bapi/composite/v1/public/composite/ae/announcement/search" \
  -H "Content-Type: application/json" \
  -d '{
    "page": 1,
    "size": 10,
    "category": "NEW_LISTING"
  }'
```

**Response** — `SearchResult<AnnouncementResp>`

| Field | Type | Description |
|-------|------|-------------|
| `total` | `Long` | Total number of records |
| `rows` | `List<AnnouncementResp>` | List of announcements |

**Response Example**

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

# Portfolio Module

> Base URL: `https://asterdex.com/bapi/futures`
> All Portfolio endpoints are **private** and require authentication.

---

## 3. Pro Summary

**`PRIVATE`** `POST /v1/private/campaign/portfolio/summary/pro`

Returns trading summary statistics for the Pro portfolio within a given time period, including funding fees, commissions, trade counts, trade volumes, and grid strategy metrics.

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `period` | `String` | No | Time period. Enum: `24h`, `7d`, `14d`, `30d`, `all`. Defaults to all-time if omitted. |

**Response** — `ProSummaryResp`

| Field | Type | Description |
|-------|------|-------------|
| `fundingFee` | `BigDecimal` | Cumulative funding fee for the period |
| `latestFundingFee` | `BigDecimal` | Most recent funding fee |
| `totalCommission` | `BigDecimal` | Total commission paid for the period |
| `latestCommission` | `BigDecimal` | Most recent commission payment |
| `totalTradeCount` | `Long` | Total number of trades |
| `longTradeCount` | `Long` | Number of long trades |
| `shortTradeCount` | `Long` | Number of short trades |
| `totalTradeVol` | `BigDecimal` | Total trade volume |
| `longTradeVol` | `BigDecimal` | Long trade volume |
| `shortTradeVol` | `BigDecimal` | Short trade volume |
| `latestUpdated` | `Date` | Timestamp of the last data update |
| `periodStart` | `Date` | Start time of the statistics period |
| `periodEnd` | `Date` | End time of the statistics period |
| `gridTotalCommission` | `BigDecimal` | Total commission for grid strategy |
| `gridLatestCommission` | `BigDecimal` | Most recent grid commission |
| `gridTotalTradeCount` | `Long` | Total trade count for grid strategy |
| `gridLongTradeCount` | `Long` | Long trade count for grid strategy |
| `gridShortTradeCount` | `Long` | Short trade count for grid strategy |
| `gridTotalTradeVol` | `BigDecimal` | Total trade volume for grid strategy |
| `gridLongTradeVol` | `BigDecimal` | Long trade volume for grid strategy |
| `gridShortTradeVol` | `BigDecimal` | Short trade volume for grid strategy |
| `gridLatestUpdated` | `Date` | Last update timestamp for grid data |
| `gridPeriodStart` | `Date` | Grid statistics period start |
| `gridPeriodEnd` | `Date` | Grid statistics period end |

**Request Example**

```json
{
  "period": "7d"
}
```

**Response Example**

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

## 4. Portfolio Line Chart

**`PRIVATE`** `POST /v1/private/campaign/portfolio/overview/v2/line/chart`

Returns time-series data points for the portfolio equity curve. Each point contains balance and PnL broken down by asset type (perp, spot, staking) for rendering a multi-line chart.

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `period` | `String` | No | Time period. Enum: `24h`, `7d`, `14d`, `30d`, `all`. |

**Response** — `List<PortfolioLineChartResp>`

| Field | Type | Description |
|-------|------|-------------|
| `dt` | `String` | Data point timestamp / label |
| `balance` | `BigDecimal` | Total portfolio balance at this point |
| `pnl` | `BigDecimal` | Total portfolio PnL at this point |
| `perpBalance` | `BigDecimal` | Perpetual contract balance |
| `perpPnl` | `BigDecimal` | Perpetual contract PnL |
| `perpTradePnl` | `BigDecimal` | Realized PnL from perp trades |
| `shieldTradePnl` | `BigDecimal` | Realized PnL from shield trades |
| `spotBalance` | `BigDecimal` | Spot account balance |
| `spotPnl` | `BigDecimal` | Spot PnL |
| `stakingBalance` | `BigDecimal` | Staking balance |
| `stakingPnl` | `BigDecimal` | Staking PnL |
| `predictionPnl` | `BigDecimal` | Prediction (Earn) PnL |
| `allSPnl` | `BigDecimal` | Combined spot + prediction PnL |
| `period` | `String` | Period enum value for this data point |
| `futureUid` | `Long` | User's futures UID |

**Request Example**

```json
{
  "period": "30d"
}
```

**Response Example**

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

## 5. Portfolio Line Calendar

**`PRIVATE`** `POST /v1/private/campaign/portfolio/overview/line/calendar`

Returns daily-granularity portfolio data points within a specified date range, used to render a calendar-style or date-range chart. Unlike the period-based line chart, this endpoint queries by explicit start and end dates.

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `startDate` | `String` | **Yes** | Start date (inclusive), format: `yyyy-MM-dd` |
| `endDate` | `String` | **Yes** | End date (inclusive), format: `yyyy-MM-dd` |

**Response** — `List<PortfolioLineChartResp>`

Same structure as [Portfolio Line Chart](#4-portfolio-line-chart). The `dt` field contains the date in `yyyy-MM-dd` format.

**Request Example**

```json
{
  "startDate": "2026-05-01",
  "endDate": "2026-05-31"
}
```

**Response Example**

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

**Error Cases**

| Scenario | Behavior |
|----------|----------|
| `startDate` or `endDate` missing | Returns validation error (400) |
| Date range too large | Keep range ≤ 90 days (recommended) |

---

# Appendix

## Period Enum Values

| Enum | String Value | Description |
|------|-------------|-------------|
| `H_24` | `24h` | Last 24 hours |
| `D_7` | `7d` | Last 7 days |
| `D_14` | `14d` | Last 14 days |
| `D_30` | `30d` | Last 30 days |
| `ALLTIME` | `all` | All time |

## Common Response Wrapper

All endpoints return a standard wrapper:

```json
{
  "code": "000000",
  "message": null,
  "data": { ... },
  "success": true
}
```

| Field | Type | Description |
|-------|------|-------------|
| `code` | `String` | `"000000"` indicates success |
| `message` | `String` | Error message, `null` on success |
| `data` | `Object` | Response payload |
| `success` | `Boolean` | `true` on success |
