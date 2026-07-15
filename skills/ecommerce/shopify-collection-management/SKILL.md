---
name: shopify-collection-management
title: Shopify Collection Management
description: CREATE, RETITLE, REBUILD, and BIND Shopify collections and collection-layout templates via REST API. Covers custom vs smart collections, template.json manifests, collect assignment, duplicate-safe creation, orphan cleanup, and the user's desk-first shop-structure preference.
triggers:
  - "create / rename a Shopify collection"
  - "bind a custom template to a collection"
  - "restructure collections into focused groups"
  - "clean up old collection templates"
  - "assign products to one or more collections"
  - "Shopify collection 422 / product_type / template_suffix"
---

# Shopify Collection Management

## Rules

1. Use **custom collections** for curated/manual groupings. `products_count` is reliable for custom collections via REST; for smart collections it is often null.
2. Use **smart collections** only when the grouping is truly dynamic (price/type/tag rules). Otherwise prefer custom for predictability.
3. Never rename a collection handle by mutating the id. Rebuild via a new POST and delete the old one.
4. A template `templates/collection.<handle>.json` only takes effect when the collection has `template_suffix == <handle>`.
5. Template JSON must pass Shopify section schema at PUT time (`max_blocks`, numeric types, etc.). Validate inline, not offline.
6. `POST /collects` returns **422 if the product is already in the collection** — treat as success.
7. Always delete orphan template files when unbinding a collection template.
8. Apply a focused/single-purpose naming rule: one collection = one concept, avoid overlapping Home / Shop / All / Desk duplication.

## User Preferences

- Shop 收敛成一个单一 collection（如 `desk`），不再保留 `all-finds` 这种笼统入口。
- 细分类要有专一标题：不要用 `Daily Need` 这种泛称，改成 `Lamp` / `Sleep` / `Wall Art` 等可读名称。
- 旧 overlap collection（Healthy / The Warm Collection / Trends / Electronics Accessories / Sleep / Office Furniture / Poster / Bags & Wallets / Quiet Night ）清空 collect，保留 collection 作 SEO 历史。
- 新建分类优先 desk-first；sleep/healthy 延后按需再建。
- 核心分类：Desk Mats / Desk Accessories / Desk Lighting / Charging Station / Cable Management / Wall Art / Sleep / Desk Toys。
- 产品 `product_type` 需跟 collection 语义对齐，否则 breadcrumb 会乱。

## Procedure

### 1 盘点现状
```
GET /admin/api/2024-01/smart_collections.json (limit 250)
GET /admin/api/2024-01/custom_collections.json (limit 250)
GET /admin/api/2024-01/products.json (limit 250)  + 分页到空为止
GET collects?collection_id=<id> 确认每个 collection 下的产品
```

### 2 清空旧 collect 映射
只删 collect，不删 collection 本身（保留历史 SEO 与 redirect）：

```
for collect in GET /collects.json?collection_id=<old_id>:
    DELETE /collects/<collect_id>.json
```

### 3 创建新 collection
```json
POST /admin/api/2024-01/custom_collections.json
{
  "custom_collection": {
    "title": "Desk",
    "handle": "desk",
    "sort_order": "best-selling"
  }
}
```

记下返回的 `id`。

### 4 修正 product_type
对已乱的商品 `PUT /products/<id>.json` + `"product": {"product_type": "..."}`。

### 5 批量 assign collects
按设计映射表逐一 `POST /collects`，422 already-exist 忽略。

### 6 创建/绑定 collection template（可选）
```
PUT /admin/api/2024-01/themes/<theme_id>/assets.json
  ?asset[key]=templates/collection.<handle>.json
  ?asset[value]=<json_dumps(section_manifest)>
```

必须约束：
- `max_blocks` 硬限制：`df-shop-by-need` 为 2
- 数字型 setting 必须传 number，不能传 `"3"` 字符串
- 只引用已安装 section type；用不存在 type 会 422

绑定 template：
```json
PUT /admin/api/2024-01/smart_collections/<collection_id>.json
{
  "smart_collection": {
    "id": <collection_id>,
    "template_suffix": "<handle>"
  }
}
```

解绑：
```json
{
  "smart_collection": {
    "id": <collection_id>,
    "template_suffix": ""
  }
}
```

### 7 清理 orphan template
```
DELETE /admin/api/2024-01/themes/<theme_id>/assets.json?asset[key]=templates/collection.<old_handle>.json
```

### 8 验证

运行技能内置验证脚本，不依赖外部文件：
```bash
python scripts/hermes-verify-collections.py
```
输出：
- stdout 可读结果
- JSON report → `%TEMP%/hermes-verify-collections.json`
检查项：
- 每个 product_type 正确
- 每个 collect 指到预期 collection_id
- 目标 collection 的产品数量与设计一致
- 旧 overlap collection 的 collects = 0

## Pitfalls

1. `/products.json` 只返回 250 个，但分页参数坑人；必须 while loop 到 `products` 为空为止。
2. custom_collection 的 `products_count` 在 REST 中经常 null；从 collects 端点计数，不要依赖 products_count。
3. smart_collection rules 不太好验证 tag 条件是否生效；对窄 collection 直接用 custom collection 更稳。
4. template JSON 的 `order` 数组缺失会导致 422；一定带上 `"order": [...]`。
5. `df-shop-by-need` 的 `max_blocks` 是 2，超了就 422。
6. `source_count` / `price` 这类数字 setting 在 template JSON 里必须是数字字面量。

## Output Artifacts

每次完整 collection restructure 落盘：
- `shopify_collection_map.json`：handle / collection_id / product_ids / product_type / expected_product_count
- `shopify_collects_by_collection.json`：每个 collection 下面的 product handle 列表
- 模板文件：`templates/collection.<handle>.json` 保存到主题备份目录
