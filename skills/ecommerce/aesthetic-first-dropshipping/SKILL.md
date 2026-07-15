---
name: aesthetic-first-dropshipping
description: 用 Behance / Pinterest / 设计平台的审美信号驱动 Shopify dropshipping：从设计扫描、供应商匹配、taste profile、建站转化到学习闭环。Desk / lifestyle 品类尤适用。
---

# Aesthetic-First Dropshipping（审美优先 Dropshipping）

## 触发条件

用户提到以下任意一种：
- 从 Behance / Pinterest / 设计平台找灵感做产品
- 要建一个以审美为核心的 Shopify 店
- "读懂市场尖端的品味"
- "增加店面技术"
- "从设计到货源到盈利"
- "打赢那么多对手"

## 核心原则

1. **先诊断现有执行层，再决定是否加模块**。不要因为用户说"更厉害的 AI"就直接新建 agent。先确认：launch-cell / production-pack / fulfillment 是否已经存在且工作正常。如果是，瓶颈大概率在感知层，不在执行层。
2. **用户授权信号大于预设 gate**：当用户说"你可以用 shopify / 直接做 / 先执行"，立刻切换为 L3-L4 执行：读文件、编辑代码、调用 API；不要因为记忆里有旧错误/旧 block 就继续询问。这是即时授权，已覆盖历史失败状态。
3. **图片上传只认 GraphQL 三阶段流**：本店 Shopify 2024-10 下 REST `product_images` / `staged_uploads` 返回 406。固定流程：`stagedUploadsCreate` → 二进制 POST → `productCreateMedia(originalSource=...)`。引用见 `references/shopify-media-upload-2026-07-07.md`。
2. **审美来源和供货来源是两套语言**。Behance 说"clay-terracotta + matte + editorial type"，CJ 说"90x40cm non-slip washable"。必须有一层 Translator。
3. **Taste Profile 是全系统的宪法**。一旦定下来，所有 candidate 筛选、内容生成、店面决策都按这个打分。
4. **Profit 公式**：利润 = (taste_fit × trust_signal) / (decision_time × fulfillment_risk)。优化方向是提高 taste_fit / trust_signal，缩短 decision_time，降低 fulfillment_risk。
5. **从最简单的方式开始**。不要一上来建 10 个 agent。先做 taste_profile.json + 一个 aesthetic-hunter 命令 + 一个 learning log，跑通 3 轮再自动化。

## 系统架构：六层店面技术

1. **感知层 Perception**：扫描多源信号，识别"元素组合共现"而非单品。TikTok 看视觉节奏，Amazon 看 review 抱怨词，Pinterest 看色板组合，Reddit 看冷门方案。
2. **策展层 Curation**：把 raw signal 翻译成可卖的产品规格（材料/尺寸/工艺/价位/禁忌）。
3. **决策层 Decision**：Taste score × margin gate × US fulfillment gate。输出 ready-to-test candidate。
4. **内容层 Content**：带风格记忆的 content system。每个产品有：主视觉方向、thumbnail 逻辑、caption 语气、UGC angle。
5. **转化层 Conversion**：Collection 按情绪场景叙事，定价用锚定+系列感，店面信任信号完整。
6. **学习层 Learning**：销售数据反哺 taste profile，赢的规格被记住，输的规格被标记。

## 标准交付物

### 1. taste_profile.json（一次配置，全系统宪法）

```json
{
  "collection": "Desk Body Reset",
  "aesthetic": {
    "palette": ["clay", "oat", "sage", "warm-black"],
    "texture": ["matte", "tactile", "canvas-tooth"],
    "style": ["editorial-minimal", "archive-type", "warm-luxury"],
    "forbidden": ["plastic-sheen", "harsh-shadow", "pure-black", "generic-ai-stock"]
  },
  "price_anchor": {
    "desk_mat": 29,
    "mouse_pad": 16,
    "art_print": 34
  },
  "keywords": ["warm desk", "minimalist desk setup", "tactile desk mat", "cable management"],
  "sources": ["behance", "pinterest", "tiktok", "amazon_reviews"]
}
```

### 2. aesthetic-hunter CLI 子命令

```
python dailyfindusa_os.py aesthetic-hunter --url <behance-or-pinterest-url>
```

输出：
- 设计描述
- Taste score（0-1）
- 可能的产品类型映射
- CJ 搜索关键词
- 粗略规格猜测
- 价位锚定

### 3. taste_learning.json

每笔销售/测试结果记录 taste input → outcome → margin。每周更新 taste_profile 权重。

## 货源映射现实

| 渠道 | 能做什么 | 不能做什么 | 当前状态 |
|---|---|---|---|
| CJ Dropshipping | desk mat, mouse pad, cable clip 等标准品 | 设计款、艺术版、定制编辑风、aesthetic desk 线的精确同款 | 已接入；同款核对结论见 `references/2026-07-07-cj-same-style-probe.md` |
| Printify | 可定制 desk mat / mouse pad / art print | API 不稳定 | 备选 |
| 1688 / Alibaba | 同厂同款、定制款 | MOQ、需手动沟通 | 需轻量对接 |
| ZenDrop | desk / lifestyle dropshipping 备选 | 对编辑风/定制的支持度待验证；API 路径 blocked，只能浏览器 UI | 已加 key；浏览器 pid=70428 |
| AliExpress / DSers | 同源款、US warehouse 候选 | 直搜被 captcha 拦；需走 DSers 插件或用户手动核对 | 用户已装 DSers |

**原则**：CJ 对 aesthetic desk 线只能做功能近似，不做精确同款；精确同款优先 Zendrop 现有 supplier 或 AliExpress/DSers 同源核对。第一阶段主力用 Zendrop 上架有货款，有销量数据后再探索 AliExpress 降本。

**原则**：第一阶段主力用 CJ，设计款用 CJ "近款化" 打头，有销量后往 Printify 定制款迁移。

## 盈利路径（时间线）

| 天数 | 做什么 | 结果 |
|---|---|---|
| Day 1 | 给 1 个 Behance / Pinterest 设计链接 | aesthetic-hunter → CJ 搜索词 |
| Day 2 | 用搜索词跑 CJ freight + margin | 确认货源 + 毛利 |
| Day 3 | 进 launch-cell → production-pack | TikTok 视频方案 |
| Day 7 | 发第一条视频，观察 CTR | >3% 继续，<3% kill |
| Day 14 | 5 个 taste learning 样本 | 更新 taste_profile，第二轮更准 |

## Homepage / Theme Edits
  - `templates/index.json` 是可写的 JSON，不是 liquid；直接改 `sections.*.settings` 即可。
  - 上传 asset 后必须 `GET /themes/{id}/assets?asset[key]=...` 读回确认；不要相信编辑器里所见即时生效。
  - Collection 可见的前提：`published_at` 已设置（非 draft）。`status=active` 不是 storefront 可见的充分条件。
  - **Desk-first homepage template**：当用户要求"纯 desk-first"时，直接把 homepage 的 `hero/featured/new_finds/shop_by_need` 改为 desk 产品池，CTA 链接到 `/collections/desk`。不要新建 collection；用现有 Desk collection。
  - **Multiple theme copies**：Shopify 常有多个 draft copies。用户看到的预览 URL 可能指向非 main theme。修改后先 `GET /themes.json` 确认当前 `role=main` 和可能被预览的 `unpublished` theme，两边都改后再 `PUT role=main` 发布。否则用户看到还是旧版。

  ## Findskill 视觉观察工作流

把 Behance / Pinterest / 设计平台结果当作视觉数据源，而不是只读标题。标准流程：

1. 搜索后用 `browser_vision` 看缩略图构图、材质、色板、产品类别。
2. 区分 **概念渲染 (concept render)** 与 **真实可售产品**。只有后者有 supply 价值；前者只提供 design DNA。
3. 记录每个候选项的：`visual_signal`、`product_type`、`materiality`、`palette`、`modularity`、`vs_design_reference`。
4. 只保留最像 2-3 个近邻信号，不要贪多。

当前已确认的高价值信号：
- **DESKO**：modular + matte + warm minimal + industrial，作为 taste 基准。
- **KOMBO | Desk organizer** (Mirko Romanelli)：recycled plastic、soft rounded shapes、modular compartments。这是目前最像 **可卖产品** 的设计信号，可作为 priority A translation target。
- **Moushi**：clay texture desk accessory，pastel colors，soft form。证明 clay/matte 材质已在 Behance desk accessories 中被使用。
- **Modular Desk Set Concept for Ikea**：确认 modular desk 已进入主流设计视线。

Behance 搜索建议：避免带 typo 的搜索词，优先用 `desk accessories`、`minimal desk design`、`premium desk mats`，它们的相关度比 `desk prodcut` 更高。

## Spocket / 轻量 API 客户端策略

当用户问“能不能用 Spocket / MCP / 轻量 API 客户端”时，按以下顺序处理：

1. 先确认现有系统里是否已有 Spocket API 客户端代码或 `.env` 配置。
2. 如果没有，评估**浏览器后台通道是否可用**：
   - 看本机是否已有已登录的 Shopify/Spocket Chrome 窗口
   - 如果已有，直接读 DOM / `browser_vision` / `browser_console` 抓数据
3. 如果浏览器通道不可用，请求用户生成 Spocket API key，或从 Config → Integrations 中复制现有 key
4. 一旦拿到 `api_key` + `base_url`，立刻写轻量客户端：只做 `search / get / variants / shipping` 四个端点，不引入重依赖
5. 如果用户说“我去 app.spocket.co/winning-products 按 generate”，说明 API 页面入口存在，优先走 API route 而非浏览器路线

14. **REST product_images 与 staged_uploads 406**：Shopify Admin REST 2024-10 对 `POST /product_images.json` 和 `POST /staged_uploads.json` 均返回 406。不要继续探针这两种 REST 写法；改用 GraphQL 三阶段流：`stagedUploadsCreate` → 原始二进制 POST 到返回的 `url` → `productCreateMedia` 用 `originalSource`。see `references/shopify-graphql-image-upload-2026-07-07.md`。
15. **productCreateMedia 字段名不可猜**：该 mutation 不接受简写/别名字段。已知有效输入只有 `originalSource`、`mediaContentType`、`altText`；若报 `Field ... doesn't exist on type 'Media'`，直接删掉该字段，不要换同义名继续试。
16. **GraphQL UnsignedInt64 必须字符串化**：`fileSize` 在 `StagedUploadInput` 里必须是 string，不能是 int。
17. **不要重复上传 lifestyle 图**：首轮 productCreateMedia 成功后，后续同产品再发同一 lifestyle 图会重复入库。先查 `images` / previews，只有失败时再重试。

## 产品详情页文案标准

当用户要求优化产品细节、尺寸、材料、讲解时，按以下结构重写所有 active 产品描述：

- **Hook sentence**：一句话讲出 feeling/场景
- **Details 清单**：Size / Material / Thickness / Color 等硬信息
- **Why it works**：用 2-3 句话把 specs 翻译成购买理由
- **Care 说明**：清洁/保养方式
- **FAQ**：3 个高频问题，用 Q&A 格式
- **Pair with**：内链到 1-2 个互补产品

禁忌：
- 不用 `guarantee`、`medical`、`100%` 等词
- 不堆形容词，每句有信息量
- 材料字段必须对应真实 SKU 规格，不允许空泛如 "high quality"
- 颜色/尺寸选项用 product variant 的真实值，不编造

执行方式：
- 批量生成描述 dict，按 `PUT /products/{id}.json` 直写 Shopify
- 每次写入后回读 1-2 个 sample 验证生效
- 不修改 `title`、`handle`、`variants`、`images`，只改 `body_html`

## 流量获取专业体系（2026 平台策略）

### Pinterest：视觉搜索引擎

Pinterest 不是社交平台，是**视觉搜索引擎**。适合 aesthetic desk/home 品类。

DailyFinds 执行标准：
- 比例：2:3 或 1000×1500px，最高不超过 1000×2100px
- 标题前 50-60 字符承载核心关键词
- 描述告诉用户"点了之后能看到什么"，不堆 hashtag
- 80/20 rule：80% 启发灵感，20% 直接促销

Board 结构建议：
- Warm Minimal Desk Setup
- Japandi Home Office
- Terracotta & Sage Aesthetic
- Desk Wellness Reset

发布节奏：每天 5-15 个 Pin，原创 3-5 个/周，用 Tailwind 自动排期

Pinterest Ads 参考：CPM $2-5，CPC $0.10-1.50，起步日预算 $10-20

### Instagram：信任验证平台

2026 Instagram 定位：被 TikTok 种草后来 Instagram 验证品牌"真不真"。

Reels-to-Stories 漏斗：
- Reels：top-of-funnel discovery
- Stories：mid-funnel social proof
- Profile + Shop：bottom-funnel purchase

内容分配：60% 价值内容，30% 产品展示，10% 品牌叙事

### TikTok：内容驱动发现

四支柱：creator-led content（85% 发现）+ affiliate program + Shop Ads + Live Shopping

Short-form 转化公式：
- 0-3s：视觉 hook
- 3-8s：problem→reset 对比
- 8-12s：2 个卖点 + CTA
- 12-15s：福利钩子

Affiliate 佣金结构：micro 12-15%，mid 8-12%，macro 定制

### Reddit：零成本冷启动

适用板块：r/desksetup, r/buyitforlife, r/Japandi, r/WorkFromHome

规则：不发广告，发真实使用场景 + 问题解决。格式：Before/after、"What I use for..."、Setup tour

### X/Twitter：品牌资产 + 社群关系

不适合 primary discovery channel for desk goods。适合 founder story、社群关系。良性动作：同步 Reddit 好帖到 X 扩大 signal。

### 预算分配框架

| 渠道 | 阶段 | 日预算 | 优先级 |
|---|---|---|---|
| Pinterest organic | Day 1-30 | $0 | 高 |
| Instagram Reels | Day 1-60 | $0 | 高 |
| Reddit organic | Day 1-30 | $0 | 中 |
| Pinterest Ads | Day 30+ | $10-20 | 验证后 |
| TikTok Shop ads | Day 60+ | ROAS > 2.5x | 高 |
| Email/SMS | 有首单后 | $0 | 高 LTV |

## 渠道优先级偏好

| 渠道 | 角色 | 使用姿势 |
|---|---|---|
| Spocket | 优先 desk 渠道 | 质量主观更好；优先搜 Spocket；有 US fulfillment |
| CJ | 严格筛选近款 | 只接受高 design-score 的近款；弱 style 商品直接 skip |
| Printify | 定制备选 | 有销量数据后再转定制；不要一开始就硬走定制 |

## 数据栈（DailyFinds 标配）

Free tools: Microsoft Clarity (heatmap + session recording), Google PageSpeed Insights (target mobile >70), Google Trends, TikTok Creative Center, Etsy search, Google Keyword Planner. Paid layer when ready: SEMrush / Ahrefs, Jungle Scout / Helium 10.

## 周期性 Collection 漂移清理

Audit every 2-3 weeks: list all custom + smart collections via API, check product counts via `collects.json`, delete empty duplicates and orphan templates. Given this store's pattern, hunt `*-1` duplicates, `healthy` / `trends` / `lighting`.

## Head + favicon + footer social 一键优化模式

When user asks for SEO/social/footer work, do all four in one session: 1) OG + Twitter card + JSON-LD in `layout/theme.liquid`, 2) `<link rel="icon">` pointing at `settings.favicon`, 3) add missing `social_facebook` / `social_pinterest` in `sections/footer.liquid`, 4) patch `current.default_shop_url` in `config/settings_data.json`. Verify all four with a read-back before reporting done.

## Admin Cloudflare 阻断时的 App 安装降级策略

Queue installs as manual user actions with direct URLs — Tawk.to: `https://apps.shopify.com/tawk-to`, Klaviyo: `https://apps.shopify.com/klaviyo-email-marketing`, Judge.me: `https://apps.shopify.com/judgeme`. Stop looping on browser automation until challenge cleared.

## 1-hour aesthetic/system audit deliverable

When the user asks for a broad system optimization, produce exactly three compact research blocks, ordered by leverage:

1. **做好网页** — 3 principles + 3 tactics. Focus on: first-screen clarity, mobile before desktop, one CTA per page. Add PageSpeed + Clarity as verification.
2. **搞好审美** — validate current brand palette against current trend; 3 visual lifts (product bg consistency, font hierarchy, whitespace). Reference Behance / Pinterest / Awwwards as free learning sources.
3. **找数据** — 3 layers: user behavior (Shopify Analytics, Clarity), market (Google Trends, TikTok labels, competitor sites), product research (Keyword Planner, MerchantWords, Etsy, TikTok Creative Center). End with a 15-min daily routine.

Always close with concrete next actions I can execute immediately.

## 数据栈（DailyFinds 标配）

Free tools that require no app install:
- **Microsoft Clarity** — heatmap + session recording; 5-min snippet install into `layout/theme.liquid`. Reveals where PDP visitors drop off.
- **Google PageSpeed Insights** — performance + mobile UX score. Target mobile >70.
- **Google Trends** — keyword interest over time; use for collection/landing-page copy.
- **TikTok Creative Center** — discover viral desk/japandi setups; copy hook structure.
- **Etsy search + sorting** — competitor pricing + review signal; lowest friction without API.
- **Google Keyword Planner** — search volume for product-category terms; requires Google Ads account only.

Paid layer when ready:
- **SEMrush / Ahrefs** — SEO health + competitor traffic.
- **Jungle Scout / Helium 10** — Amazon-side demand validation.

## 周期性 Collection 漂移清理

This store accumulates empty/duplicate collections from prior experiments. Audit every 2-3 weeks:
1. `GET /custom_collections.json` + `GET /smart_collections.json`.
2. For each: check product count via `collects.json`. If 0 and no inbound theme links, delete.
3. Remove orphan template files `templates/collection.<handle>.json` if any.
4. Rescan all theme assets for old-handle references after deletion.

Known suspect patterns on this store: `*-1` duplicates, `healthy` / `trends` / `lighting` orphans.

## Head + favicon + footer social 一键优化模式

When user asks for SEO/social/footer work, do all four in one session:
1. **OG + Twitter card + JSON-LD** in `layout/theme.liquid` `<head>`: type, title, description, image, site_name.
2. **Favicon**: add `<link rel="icon">` pointing to uploaded asset or `settings.favicon`.
3. **Footer social links**: add missing `social_facebook` / `social_pinterest` after existing Instagram/TikTok in `sections/footer.liquid`.
4. **`default_shop_url`**: patch to point at the actual shop collection.

Verify all four with a single read-back script before reporting done.

## Admin Cloudflare 阻断时的 App 安装降级策略

When `admin.shopify.com` returns a Cloudflare challenge:
- Stop looping on browser automation.
- Queue installs as manual user actions with direct URLs:
  - Tawk.to: `https://apps.shopify.com/tawk-to`
  - Klaviyo: `https://apps.shopify.com/klaviyo-email-marketing`
  - Judge.me: `https://apps.shopify.com/judgeme`
- Ask the user to install, then return with credentials (widget ID / API key) for wiring.

## DSERS CUA / SPA 表单限制与修复路径

在 Windows 上操作 DSERS Settings 页面时，两个稳定结论：

1. **SPA 表单控件未暴露给 Windows UIA 树**：`get_window_state` 只能读到页面骨架，input/select 等表单控件不可见。CUA `execute_javascript` 也会失败，除非 Chrome 以 `--remote-debugging-port=9222` 启动。
2. **普通 Chrome 窗口不等于调试端口实例**：即使地址栏显示 `dsers.com/...`，也不能假设 9222 端口可用。必须先用 `netstat -ano | findstr :9222` 验证端口在监听，否则 JS/DOM 操作一律失败。
3. **正确启动调试端口 Chrome 的流程**：全关 Chrome → 用 `terminal` 启动新实例并携带 `--remote-debugging-port=9222` → 定向打开目标 URL → `netstat` 确认端口在监听 → 再调用 `page(execute_javascript/query_dom)`。
4. **DAILYFINDS DSERS 配置清单**：General= dropshipping/English/email dailyfindusa@outlook.com/minimal sync；Shipping= Advanced US/7days/$0/less-than-day；Fulfillment= 美区本地仓优先/14天自动取消/库存预警；Order= 自动推供应商/关闭审核/退款通知发 outlook/备注加 `DailyFinds USA - fast local ship`；Product= 不同步描述价格/保持原名；Pricing= 固定毛利法/US +15-20%；Application= 只保留 Shopify+DSers。

## 已批准高设计产品落地清单

用户 2026-07-09 全批以下 3 款，进入执行阶段：

1. **模块化桌面收纳组**：Behance KOMBO/DESKO 信号，P1 优先级。Etsy $35+ 成交，AliExpress 成本 $6–12/套，3件套 $39.99 / 4件套 $59.99，毛利率 65–70%。Hook："3 件，6 种摆法。桌面从杂乱到完整，只要 30 秒。"
2. **弧形实木显示器支架**：Behance CUT Monitor Stand，P2 优先级。Etsy $35–65 热销，AliExpress $8–15/件，无抽屉 $34.99 / 带抽屉 $49.99，毛利率 60–65%。Hook："抬高一寸，桌面即景色。"
3. **有机形态陶瓷台灯**：Pinterest 2026 趋势 900+ pins，P3 优先级。AliExpress $16–28/件，mini $49.99 / 标准 $69.99，毛利率 68%。Hook："不是灯。是桌面的安静雕塑。"

版权路径：Behance 找灵感 → Etsy/Amazon 验证需求 → AliExpress 找供应商做类似但不同款 → 原创 PDP 文案和拍摄。禁止直接复制设计上架。

## 站点可达性快速诊断

当用户怀疑 dailyfindusa.com 无法访问时：
1. `nslookup` 双 DNS（8.8.8.8 + 1.1.1.1）确认 A 记录
2. `curl -I` 确认 HTTP 状态码
3. `curl -s -L | head` 读取首页前 800 字符验证内容返回
4. 若 DNS 正常且 HTTP 200，结论为"站点正常"，问题大概率在本地浏览器缓存或临时网络抖动。

## 对接现有系统的标准命令

```
python dailyfindusa_os.py aesthetic-hunter --url <url>
python dailyfindusa_os.py launch-cell --limit 5
python dailyfindusa_os.py tiktok-production-pack --limit 5
python dailyfindusa_os.py ceo-review --summary
```

Hunter 的输出应能直接作为 launch-cell 的输入查询词。
