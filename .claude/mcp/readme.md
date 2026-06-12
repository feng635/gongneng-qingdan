# MCP 工具

通过 Claude Code MCP 系统集成的外部工具，共 10 个。

| 工具 | 类型 | 用途 | 状态 |
|:----|:----:|:------|:----:|
| **Firecrawl** | npx | 全网搜索、网页抓取、结构化提取、爬虫（500次/月） | ✅ 正常 |
| **IDE** | 内置 | VS Code 诊断 + Jupyter 代码执行 | ✅ 内置 |
| **GitHub** | npx | 管理仓库、Issue、PR（需 GITHUB_TOKEN） | ✅ 正常 |
| **Playwright** | npx | 浏览器自动化操控 | ✅ 正常 |
| **彩云天气** | HTTP | 天气预报、降水预报、预警 | ✅ 正常 |
| **hotnews** | npx | Wopal 实时热点新闻获取 | ✅ 正常 |
| **files** | npx | 桌面文件读写管理 | ✅ 正常 |
| **Knowledge Graph** | npx | AI 长期记忆存储，`memory.db` 在 `.claude/knowledge-graph/` | ✅ 正常 |
| **Sequential Thinking** | npx | 链式结构化推理 | ✅ 正常 |
| **Docfork** | HTTP | 文档搜索与抓取（需浏览器 OAuth 授权） | ⚠️ 需授权 |

> 配置位置：`C:\Users\17384\.claude.json` → `projects["D:/cursor_workspace"].mcpServers`
