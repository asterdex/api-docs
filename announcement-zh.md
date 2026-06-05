# 公告 API

## AnnouncementResp（公共响应字段）

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | Long | 公告 ID |
| `category` | String | 分类，见下方枚举 |
| `title` | String | 标题 |
| `subtitle` | String | 副标题 |
| `content` | String | 正文内容 |
| `publishTime` | Date | 发布时间（毫秒时间戳） |
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

### GET `/bapi/composite/v1/public/composite/ae/announcement/get`

根据 ID 获取单条公告详情。

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | Long | 是 | 公告 ID |

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

### POST `/bapi/composite/v1/public/composite/ae/announcement/search`

分页查询公告列表，支持按分类筛选。

**请求体**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `page` | Integer | 是 | 页码（从 1 开始） |
| `size` | Integer | 是 | 每页条数 |
| `category` | String | 否 | 公告分类，不传则返回所有分类 |

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

**响应** `CommonRet<SearchResult<AnnouncementResp>>`

| 字段 | 类型 | 说明 |
|------|------|------|
| `total` | Long | 总条数 |
| `rows` | List\<AnnouncementResp\> | 公告列表 |

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
      },
      {
        "id": 12344,
        "category": "NEW_LISTING",
        "title": "AsterDex Will List ABC Token",
        "subtitle": "ABC/USDT Trading Pair Now Available",
        "content": "AsterDex is pleased to announce the listing of ABC Token...",
        "publishTime": 1717459200000,
        "jumpLink": "https://www.asterdex.com/en/support/announcement/detail/12344"
      }
    ]
  },
  "success": true
}
```
