# Announcement API

响应数据有 **1 分钟本地缓存**。

`title`、`subtitle`、`content` 根据请求头语言自动返回对应语言版本；语言含 `zh` 时返回中文，其次匹配精确语言，兜底返回英文 `en`。

---

## AnnouncementResp（公共响应字段）

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | Long | 公告 ID |
| `category` | String | 分类，见下方枚举 |
| `title` | String | 标题 |
| `subtitle` | String | 副标题 |
| `content` | String | 正文内容 |
| `publishTime` | Date | 发布时间 |
| `jumpLink` | String | 跳转链接 |

## category 枚举值

| 值 | 说明 |
|----|------|
| `ACTIVITY` | 活动公告 |
| `NEW_LISTING` | 新币上线 |
| `DELISTING` | 下架公告 |
| `UPDATES` | 更新公告 |

---

## Public 接口

### GET `/v1/public/composite/ae/announcement/get`

根据 ID 获取单条公告详情。

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | Long | 是 | 公告 ID |

**响应** `CommonRet<AnnouncementResp>`

---

### POST `/v1/public/composite/ae/announcement/search`

分页查询公告列表，支持按分类筛选。

**请求体**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `page` | Integer | 是 | 页码（从 1 开始） |
| `size` | Integer | 是 | 每页条数 |
| `category` | String | 否 | 公告分类，不传则返回所有分类 |

**响应** `CommonRet<SearchResult<AnnouncementResp>>`

| 字段 | 类型 | 说明 |
|------|------|------|
| `total` | Long | 总条数 |
| `rows` | List\<AnnouncementResp\> | 公告列表 |

---

## Private 接口（需登录）

### POST `/v1/private/composite/ae/announcement/search-direct`

分页查询当前用户的定向公告。用户地址从登录态自动获取，无需传参。

**请求体**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `page` | Integer | 是 | 页码（从 1 开始） |
| `size` | Integer | 是 | 每页条数 |

**响应** `CommonRet<SearchResult<AnnouncementResp>>`

| 字段 | 类型 | 说明 |
|------|------|------|
| `total` | Long | 总条数 |
| `rows` | List\<AnnouncementResp\> | 公告列表 |

---

### GET `/v1/private/composite/ae/announcement/direct-list`

获取当前用户的定向公告列表（不分页）。

**响应** `CommonRet<List<AnnouncementResp>>`

---

### GET `/v1/private/composite/ae/announcement/get-direct`

根据 ID 获取当前用户的单条定向公告详情。

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | Long | 是 | 公告 ID |

**响应** `CommonRet<AnnouncementResp>`
