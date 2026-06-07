---
name: daily-hotnews
description: "每天早上9点自动推送10条热点新闻到枫的微信。用 hotnews 获取新闻，通过 Server酱 推送。"
when_to_use: "用户说"早安新闻""热点""今天有什么新闻""每日推送"等场景"
---

# Daily Hotnews - 每日热点推送

每天早上9点推送10条综合热点新闻到微信。

## 推送流程

1. 获取热点新闻（hotnews MCP / 百度热搜 / 微博热搜）
2. 整理为标题+摘要格式，每天10条
3. 通过 Server酱 推送到微信

## Server酱 配置

- API: `https://sctapi.ftqq.com/{SENDKEY}.send`
- SendKey: 存储在 GitHub Secrets (`SCT_KEY`)
- 推送格式: POST + URL 编码

## GitHub Actions

定时任务在 `.github/workflows/daily-hotnews.yml`，每天 UTC 1:00（北京时间 9:00）运行。
