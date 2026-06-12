---
name: ECC 和 Firecrawl 配置会话记录
description: 2026-06-04 关于 ECC 项目、Firecrawl MCP 安装、技能读取的会话重点
type: project
---

## ECC 项目
- [ECC](https://github.com/affaan-m/ECC) 是一个 AI 编程助手增强系统，206k stars，20+ 模块
- 三个安装 profile：minimal（5模块）、core（+钩子）、full（23模块全装）
- 最终结论：**不装 ECC**，因为里面的技能大部分是 Nova 本来就懂的通用知识

## Firecrawl MCP 已安装
- 注册 Firecrawl 拿到 API key（免费 500次/月）
- 已通过 `claude mcp add` 命令装好，存在 `C:\Users\17384\.claude.json`
- 重启 Cursor 后生效，以后可以做全网搜索和深度研究

## 已读取的 ECC 技能（记在脑子里了）
- **deep-research** — 深度研究报告流程：拆解问题 → 多源搜索 → 深入阅读 → 出带引用报告
- **python-patterns** — Python 最佳实践和规范
- **pytorch-patterns** — PyTorch 深度学习规范
- **git-workflow** — Git 分支策略和提交规范
- **docker-patterns** — Docker 容器化最佳实践
- **api-design** — REST API 设计规范
- **frontend-slides** — HTML PPT 生成流程
- **security-scan** — AgentShield 安全扫描
- **security-review** — 代码安全审查
- **error-handling** — 错误处理规范
- **coding-standards** — 通用编码规范
