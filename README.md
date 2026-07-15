# Hermes Skills — 实战精选

可复用的 Hermes Agent 技能仓库。原则：**少即是多，只放经过验证的 skill**。

## 已收录

- `smart-router`：Hermes / Claude Code / Codex 联合路由，最小化 token
- `autonomous-ai-agents/desktop-agent-orchestration`：Windows 机器上驱动 Claude Code Desktop + Codex CLI 的编排规则
- `ecommerce/`：Dropshipping / E-commerce 商品研究、Aesthetic-first 选品、Shopify/Printify 工作流

## 快速开始

```
git clone https://github.com/dixon741931/Githubskill.git
cd Githubskill
```

然后在 Hermes 里按路径加载：

```
skill_view(name="smart-router")
skill_view(name="autonomous-ai-agents/desktop-agent-orchestration")
skill_view(name="ecommerce")
```

## 贡献

1. Fork 本仓库
2. 创建 feature branch
3. 只提交**测试过的、可用的 skill**
4. 提交前确认：
   - 在 Windows 机器上可运行
   - 不依赖外部付费 API（除非明确不是必选依赖）
   - 有真实使用证据
   - **绝不包含 secrets / tokens / API keys**

## License

MIT
