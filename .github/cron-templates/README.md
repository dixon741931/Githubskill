# Cron Templates

把可复用的 Hermes / agent / GitHub 定时任务配置模板放在这里。

## 现状

- `skill-lint.yml` 在 `.github/workflows/`，对每个 PR / push 自动校验 skill。
- 如果外部用户想复用 Hermes 的 cron job 模板，可在此目录追加 JSON / markdown 模板文件。

## 复用方式

1. 参考模板文件内容
2. 复制到自己的项目或 Hermes 配置目录
3. 按说明修改 schedule / prompt / skills / delivery 字段
