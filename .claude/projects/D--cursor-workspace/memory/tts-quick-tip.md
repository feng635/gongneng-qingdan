---
name: tts-quick-tip
description: TTS 语音播报必须直接用 tts_send.py，禁止用 uvx edge-tts
metadata:
  type: feedback
---

## TTS 播报提速要点

### 正确流程（不改了）
直接调 `python d:\cursor_workspace\.claude\skills\edge-tts\tts_send.py "内容"`

### ❌ 绝对禁止
`uvx edge-tts --text "..."` — 这是走弯路的错误做法，既不是主用方案又慢。第一次必须直接用 `tts_send.py`。

### 提速逻辑
- `tts_send.py` 已改为 **不检查服务是否存活，直接连 socket**，连不上再启动，省了每次 0.3 秒检查时间
- TTS 服务是常驻后台的，直接发数据秒级返回
- 调用流程：`python tts_send.py "内容"` → 连 socket → 发文本 → 服务端秒回 OK → 后台请求 API + 播放

**为什么:** 之前每次调用先检查服务状态浪费了时间，且第一次用错了 uvx edge-tts 导致要重来。
**如何应用:** 每次需要语音播报时，第一反应直接用 `tts_send.py`，不犹豫、不试错。
