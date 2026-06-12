---
name: bilisum
description: "当用户要对 B站/YouTube 视频做 AI 总结、转写语音、生成思维导图时，使用 bilisum 工具。自动转写视频语音并生成文字总结。"
when_to_use: "用户说"总结这个视频""视频转文字""B站视频总结""YouTube总结""生成思维导图"等"
---

# BiliSum — AI 视频总结工具

B站/YouTube 视频的 AI 总结工具，自动转写语音、生成文字总结和思维导图。

## 安装与环境

| 项目 | 说明 |
|------|------|
| 安装方式 | `npx bilisum`（自动建 Python 虚拟环境） |
| 默认地址 | `http://127.0.0.1:3838` |
| 数据目录 | `D:\cursor_workspace\bilisum-data` |
| Python | `D:\python\python.exe`（需 3.12） |

## 启动命令

```bash
# 带代理和 ffmpeg 启动
export PATH="$PATH:/c/Users/17384/ffmpeg/ffmpeg-master-latest-win64-gpl/bin"
export HTTP_PROXY=http://127.0.0.1:7897
export HTTPS_PROXY=http://127.0.0.1:7897
export CURL_SSL_NO_REVOKE=1
npx bilisum start --data "D:/cursor_workspace/bilisum-data"
```

## API Key 配置

SiliconFlow（硅基流动）：
- 注册地址：https://cloud.siliconflow.cn
- ASR 转写：提供商选 SiliconFlow，模型 `TeleAI/TeleSpeechASR`
- 摘要 LLM：提供商选 OpenAICompatible，Base URL `https://api.siliconflow.cn/v1`，模型 `Qwen/Qwen2.5-7B-Instruct`

## Web 界面

启动后访问 `http://127.0.0.1:3838` 使用 Web 界面操作。

## 数据存储

- 数据库：`bilisum-data/video_sum.db`
- 缓存：`bilisum-data/cache`
- 任务：`bilisum-data/tasks`
