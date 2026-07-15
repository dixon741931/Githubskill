---
name: dailyfinds-product-research
description: >
  DailyFinds 选品与执行前置研究：按 DAILYFINDS_COMMERCE_OS_MASTER.md 的 Deep Dive 产出
  可执行选品报告，覆盖 pain chain / supplier chain / margin / compliance / TikTok hooks。
  Trigger: 用户说"找爆款"、"选品"、"研究产品"、"继续想其他办法"、"deep dive"、"sourcing"
---

# DailyFinds Product Research Skill

## 目标
按用户的 Commerce OS 前置研究产品机会，输出可交付 Deep Dive 的候选集，不做无依据铺货。

## 前置文件
- `D:/my_bot/DAILYFINDS_COMMERCE_OS_MASTER.md`
- `D:/my_bot/DAILYFINDS_DESIGN_SYSTEM.md`

Provider/runtime约束：
- Hermes gateway 和任何 scheduled jobs 必须跑在 Nous Portal free tier (`stepfun/step-3.7-flash:free`)，除非用户明确切换 provider
- DeepSeek 只允许在本地 Hermes TUI 会话里用，且用户确认有余额；不要给 cron/后台自动化配 deepseek
- 如果 `.env` 写入被 Hermes 拦截，直接告诉用户手动加那行，然后从 detached shell 重启 gateway；不要盲目重试 programmatic `.env` 修改

## 产品筛选铁律
1. 只能进入 5 pillars 之一：Desk Body Reset / Sleep & Screen Reset / Recovery Comfort / Travel Comfort / Everyday Functional Tools
2. 不能生成虚假评论；不能搬运他人评论；不能做医疗/保证/治愈类宣传
3. 用户已验证 API 可用时以 API 读取店铺数据优先
4. 审核不清时，先学习再执行；不要先创建再补救

## 数据源
- Shopify 店铺现状：collections、现有 products、price/margin 结构
- 需求信号：Google Trends、TikTok Creative Center、Amazon、Etsy；优先找 complaint 和内容缺口
- 供应端：CJ / AliExpress / Shopify Collective / Faire / Alibaba Global Sources，至少比两家
- 价格与 margin：必须输出 landing cost / suggested retail / gross margin
- 设计约束：严格使用 DAILYFINDS_DESIGN_SYSTEM.md token，绝不用 "guarantee"

## Deep Dive 必须覆盖
- Pain intensity + frequency
- 3-second clarity
- TikTok content potential
- U.S. fast shipping feasibility
- Gross margin 是否 ≥55%
- Return risk / compliance risk / battery risk
- Supplier comparison table
- Final score / Decision: DO / WATCH / REJECT

## Shopify 产出的前提条件
- Deep Dive 结论必须已有明确的 DO / WATCH / REJECT
- DO 产品才能进入Execution Mode: title / handle / SEO title / meta description / description / FAQ / tags / collections / metafields / flow tags / Search & Discovery / TikTok hooks / review/UGC plan
- 未获批准前不允许创建 live product
- 未经批准不允许修改 live theme 或安装 apps

## 真实店铺模板约束
- 现有 live PDP 结构：category label → H1 → price → benefit sentence → Details(Material/Dimensions) → Why it works → Problem → Reset → Care → FAQ → shipping block → related products → footer FAQ
- 图片规律：每款 5-6 张图，1 张 lifestyle PNG 名为 lifestyle_<slug>.png，其余为数字命名 JPG
- 当前 tags 极简：DailyFinds, desk, desk-mat；future tags 可含 desk_body_reset / us_fast_shipping / everyday_functional_tools / approved_for_mvp
- 配送文案：两者冲突并存——design system 写 estimated 3-8 business days / 30-day returns，live site 常写 Ships in 1-2 days / 30-day money-back guarantee；与用户确认后再改
- Comms absolute rule：全站禁 guarantee； wellness disclaimer 每页必须有
- Metafield：优先 custom.*；shop not Plus 时可能写保护；未写入时记录 decision_status 在 tag 和商品备忘，不要默默失败

## 常见错误
- 在研究未完成前催促创建 product
- 产出非 5 pillars 的产品
- 只依赖单一供应商
- 忽略 complaint chain
- 忽略 design token / guarantee 规则
- 在未读取 live PDP 模板前创建 body_html；必须先 web_extract 至少 2 个现有 product page
- 在未确认 supplier / landed_cost 前创建 live product；unknown 先填 Pending verification
- 用 Python 脚本创建产品后不 return product id + tags + handle；必须给可直接检查的 Handle

## 实际执行
- 足够信息时可直接调用 Shopify Admin API
- 必须遵守权限分级：既不要额外询问已批准的凭证，也不要越权改 live 设置
- 若平台阻断，优先寻找替代路径而不是重复相同失败步骤
