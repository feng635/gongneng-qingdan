---
name: web-fetch
description: "当用户要访问被墙的网站、抓取境外网页内容时，通过本地代理（加速器）访问。支持 GitHub API、Bilibili API 等被墙站点的数据获取。"
when_to_use: "用户说"打不开这个网站""被墙了""帮我抓GitHub上的内容""代理访问""访问不了"等场景"
---

# Web 内容抓取（代理模式）

通过本地代理（加速器）访问被墙的网站内容，如 GitHub、Bilibili 等。

## 代理配置

- **代理地址**：`http://127.0.0.1:7897`（Clash 类代理默认端口）
- **加速器开关**：Windows 系统代理可能显示为关闭（`ProxyEnable = 0`），但代理端口仍可直连使用

## 环境变量

每次使用前设置（Bash 环境变量不跨命令持久化）：

```bash
export HTTP_PROXY=http://127.0.0.1:7897
export HTTPS_PROXY=http://127.0.0.1:7897
export http_proxy=http://127.0.0.1:7897
export https_proxy=http://127.0.0.1:7897
export CURL_SSL_NO_REVOKE=1
```

## SSL 证书吊销检查

Windows 的 SChannel 在墙内无法验证 GitHub 等站点的证书吊销状态，必须加 `--ssl-no-revoke`：

```bash
curl -sL --ssl-no-revoke https://api.github.com/...
```

## GitHub API 用法

```bash
# 获取仓库信息
curl -s --ssl-no-revoke https://api.github.com/repos/{owner}/{repo}

# 获取 README（返回 base64 编码，取 download_url 再请求一次得原始内容）
curl -s --ssl-no-revoke https://api.github.com/repos/{owner}/{repo}/readme

# 获取原始 README 内容
curl -s --ssl-no-revoke https://raw.githubusercontent.com/{owner}/{repo}/master/README.md
```

## Bilibili API 用法

```bash
# 获取视频基本信息（标题、简介、UP主、时长等）
curl -sL --ssl-no-revoke "https://api.bilibili.com/x/web-interface/view?bvid={BV号}" \
  -H "User-Agent: Mozilla/5.0" -H "Referer: https://www.bilibili.com"
```

注意：
- Bilibili 页面 HTML 是 JS 动态渲染，直接 curl 拿不到内容
- 必须通过 Bilibili 的官方 API 获取结构化数据
- 大多数视频没有字幕（subtitle.list 为空），拿不到逐字稿
- User-Agent 和 Referer 头必须带上，否则 API 可能拒绝

## 管道到 Python 解析 JSON

```bash
curl ... | python -c "import sys,json; data=json.load(sys.stdin); print(json.dumps(data, indent=2, ensure_ascii=False))"
```

## 注意事项

- 代理端口 `7897` 可能因加速器不同而不同，用 `powershell Get-NetTCPConnection -LocalPort 7897` 确认
- 如果换了加速器软件，端口需要相应更新
- 此方法只能获取文本/API 数据，无法获取 JS 渲染后的页面内容
- WebFetch 工具有自己的网络栈，不受这些环境变量影响，无法通过此代理访问
