# Changelog

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
