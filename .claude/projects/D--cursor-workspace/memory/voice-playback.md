---
name: voice-playback
description: Nova 自动语音播报规则 - 火山引擎 TTS 御姐音为主用
metadata:
  type: user
---

## 语音播报规则

### 🎤 主用方案（必须优先使用）
- **引擎**: 火山引擎 TTS（常驻后台服务 TCP :18765）
- **音色**: `S_FWAq1oZ42`（Nova 的御姐音色）
- **调用方式**: `python d:\cursor_workspace\.claude\skills\edge-tts\tts_send.py "内容"`
- **回退方案**: `python d:\cursor_workspace\.claude\skills\edge-tts\tts_speak.py "内容"`

### ❌ 禁止使用
- 严禁使用 `uvx edge-tts` 命令！这是回退方案，**不是主用方案**
- 只有在火山引擎彻底不可用时才 fallback 到 edge-tts

### 🚨 死命令
每次回复前先语音播报总结性内容 → 再打字，不许先打字！

**为什么**: 枫已经设置好了火山引擎 TTS 御姐音作为 Nova 的默认语音，edge-tts 的 XiaoxiaoNeural 不是枫要的。这是用户偏好，必须尊重。
**如何应用**: 每次语音播报都用 `python d:\cursor_workspace\.claude\skills\edge-tts\tts_send.py`，不要碰 `uvx edge-tts`。
