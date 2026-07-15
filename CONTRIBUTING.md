# Contributing to Githubskill

## 只提交测试过的 skill

- 先在 Hermes 里跑通至少 1 次
- 不要提交实验性脚本

## 提交流程

1. Fork
2. 改 `skills/<skill-name>/SKILL.md`
3. 连同 `references/` 一起提交
4. 开 PR，说明这个 skill 解决了什么问题

## 禁止提交的内容

- secrets / tokens / API keys / cookies / session
- 会产生真实外部写操作的默认配置
- 拷贝自他人仓库且无实测证据的内容

## 目录规则

```
skills/<skill-name>/
  SKILL.md
  references/    # 可选，参考文档
  scripts/       # 可选，脚本
  assets/        # 可选，模板/图片
```

每个 skill 目录必须包含 `SKILL.md`。
