# Changelog

## 2026-05-21

### Added

#### `POST /fapi/v3/stpMode` — Change STP Mode / 更改STP模式

A new TRADE endpoint that sets the account-level **Self-Trade Prevention (STP) mode** applied to all orders by default. Accepted values: `EXPIRE_TAKER`, `EXPIRE_MAKER`, `EXPIRE_BOTH`.

#### `GET /fapi/v3/stpMode` — Get Current STP Mode / 查询STP模式

A new USER_DATA endpoint that returns the account's current STP mode.

### Changed

#### `POST /fapi/v3/order` — New Order: added optional `stpMode` parameter

Added `stpMode` (ENUM, optional) to the place-order parameter list. When specified, it overrides the account-level STP default for that individual order.

---

## 2026-05-20

### Added

#### Strategy Order APIs / 策略订单接口

- `POST /fapi/v3/placeStrategyOrder` — Place Strategy Order / 策略下单
- `POST /fapi/v3/updateStrategyOrder` — Update Strategy Order / 更新策略订单
- `GET /fapi/v3/strategyOrder` — Query Strategy Open Order / 查询策略当前挂单
- `GET /fapi/v3/strategyOrder/history` — Query Strategy History Order / 查询策略历史订单

Supports OTO, OCO, and OTOCO strategy types.

---

## 2026-05-19

### Added

#### `POST /fapi/v3/chase` — Place Chase Order / 下追单

A new public endpoint that **places a BBO-pegged GTX limit order with automatic price tracking**. The strategy service polls each tick and re-pegs the order to `bid1 − chaseOffset` (BUY) or `ask1 + chaseOffset` (SELL). The chase auto-cancels when the market moves beyond `maxChaseOffset` from the original BBO. Supports `priceLimit`, `quantityUnit` (`BASE` / `QUOTE`), and optional `maxChaseOffset` in `ABSOLUTE` or `PERCENTAGE` units.

### Changed

#### `PUT /fapi/v3/order` — Modify Order: clarified BBO-pegged behavior

Added a note that BBO-pegged orders (placed with `pegPriceType = COUNTERPARTY_1 / QUEUE_1`) cannot have their price re-resolved via plain modify — to continuously track the BBO use a Chase order (`POST /fapi/v3/chase`).

---

## 2026-05-12

### Added

#### `POST /fapi/v3/registerAndApproveAgent` — Register and Approve Agent / 注册并授权 Agent

A new public endpoint that **registers an API agent account and grants trading/withdrawal permissions in a single atomic call**.

---

## 2025-xx-xx

### Added

#### `POST /fapi/v3/asset/migrateUser` — Migrate User Assets / 用户资产迁移

#### `GET /fapi/v3/asset/migrateUser/history` — Migrate User Assets History / 用户资产迁移历史
