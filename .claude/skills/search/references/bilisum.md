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
- 知识库 LLM：同上

## 已知问题

- **ffmpeg 路径**：`C:\Users\17384\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\`，必须加到 PATH 后才能正确处理音频
- **代理**：下载 B站视频不需要代理（国内直连），但下载 GitHub 资源需要
- **SSL 证书**：Windows SChannel 无法验证 GitHub 证书吊销，curl 需加 `--ssl-no-revoke`，npm 需设 `strict-ssl false`

## API 端点

| 端点 | 用途 |
|------|------|
| `GET /api/v1/tasks` | 查看所有任务 |
| `GET /api/v1/tasks/{task_id}/progress` | 查看任务进度 |
| `GET /api/v1/tasks/{task_id}/events` | 查看任务事件日志 |
| `GET /api/v1/tasks/{task_id}/result` | 获取任务结果 |
| `POST /api/v1/videos/{video_id}/tasks` | 创建新任务 |

## 数据存储

- 数据库：`D:\cursor_workspace\bilisum-data\video_sum.db`（SQLite）
- 缓存：`D:\cursor_workspace\bilisum-data\cache`
- 任务文件：`D:\cursor_workspace\bilisum-data\tasks`

## 使用场景

- 看不懂的 B站教程视频 → 丢进去生成文字总结
- 长视频快速提取要点 → 思维导图一目了然
- 多个相关视频 → 建知识库跨视频检索问答
