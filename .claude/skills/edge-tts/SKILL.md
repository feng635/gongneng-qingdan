---
name: edge-tts
description: "自动语音播报系统。回复完自动调用火山引擎TTS播报重点，播完自动删。60+种语音。"
when_to_use: "自动运行，不用手动调。用户也可以说"用语音读出来"手动触发。"
---

# Edge-TTS

Generate high-quality text-to-speech audio using Microsoft Edge's neural TTS service via the `uvx edge-tts` command.
Supports multiple languages, voices, adjustable speed/pitch, and subtitle generation.

## Usage
```shell
uvx edge-tts --text "{msg}" --write-media {tempdir}/{filename}.mp3

# With subtitles
uvx edge-tts --text "{msg}" --write-media {tempdir}/{filename}.mp3 --write-subtitles -
```

## Changing rate(speed), volume and pitch
```shell
uvx edge-tts --text "{msg}" --write-media {tempdir}/{filename}.mp3 --rate=+50%
uvx edge-tts --text "{msg}" --write-media {tempdir}/{filename}.mp3 --volume=+50% --pitch=-50Hz
```

## Changing the voice
```shell
uvx edge-tts --text "{msg}" --write-media {tempdir}/{filename}.mp3 --voice zh-CN-XiaoxiaoNeural
```

## Available voices
```
Name                               Gender    ContentCategories      VoicePersonalities
en-GB-LibbyNeural                  Female    General                Friendly, Positive
en-GB-RyanNeural                   Male      General                Friendly, Positive
en-GB-SoniaNeural                  Female    General                Friendly, Positive
en-GB-ThomasNeural                 Male      General                Friendly, Positive
en-HK-SamNeural                    Male      General                Friendly, Positive
en-HK-YanNeural                    Female    General                Friendly, Positive
en-US-AnaNeural                    Female    Cartoon, Conversation  Cute
en-US-AndrewMultilingualNeural     Male      Conversation, Copilot  Warm, Confident, Authentic, Honest
en-US-AndrewNeural                 Male      Conversation, Copilot  Warm, Confident, Authentic, Honest
en-US-AriaNeural                   Female    News, Novel            Positive, Confident
en-US-AvaMultilingualNeural        Female    Conversation, Copilot  Expressive, Caring, Pleasant, Friendly
en-US-AvaNeural                    Female    Conversation, Copilot  Expressive, Caring, Pleasant, Friendly
en-US-BrianMultilingualNeural      Male      Conversation, Copilot  Approachable, Casual, Sincere
en-US-BrianNeural                  Male      Conversation, Copilot  Approachable, Casual, Sincere
en-US-ChristopherNeural            Male      News, Novel            Reliable, Authority
en-US-EmmaMultilingualNeural       Female    Conversation, Copilot  Cheerful, Clear, Conversational
en-US-EmmaNeural                   Female    Conversation, Copilot  Cheerful, Clear, Conversational
en-US-EricNeural                   Male      News, Novel            Rational
en-US-GuyNeural                    Male      News, Novel            Passion
en-US-JennyNeural                  Female    General                Friendly, Considerate, Comfort
en-US-MichelleNeural               Female    News, Novel            Friendly, Pleasant
en-US-RogerNeural                  Male      News, Novel            Lively
en-US-SteffanNeural                Male      News, Novel            Rational
fr-FR-DeniseNeural                 Female    General                Friendly, Positive
fr-FR-HenriNeural                  Male      General                Friendly, Positive
zh-CN-XiaoxiaoNeural               Female    News, Novel            Warm
zh-CN-YunjianNeural                Male      Sports,  Novel         Passion
zh-CN-liaoning-XiaobeiNeural       Female    Dialect                Humorous
zh-CN-shaanxi-XiaoniNeural         Female    Dialect                Bright
zh-HK-HiuGaaiNeural                Female    General                Friendly, Positive
zh-HK-WanLungNeural                Male      General                Friendly, Positive
zh-TW-HsiaoChenNeural              Female    General                Friendly, Positive
zh-TW-YunJheNeural                 Male      General                Friendly, Positive
```

Retrieve all available voices using shell commands:
```shell
uvx edge-tts --list-voices
```

---

## 🎤 Nova 自动语音播报（火山引擎）

每次回复完自动调用语音播报，使用火山引擎 TTS + pygame 播放，播完自动删。

### 播报规则
- 每次回复末尾，把**总结性短信息（1~2句话）**直接语音播报
- 搭配文字回复一起使用，语音只念重点总结
- **备选方案**：火山引擎用不了时（额度用完/过期/报错），自动切换到微软 edge-tts（`uvx edge-tts`）

### 架构（2026-06-06 更新）

```
┌─────────────────┐     TCP :18765     ┌──────────────────┐
│  tts_send.py     │ ─────────────────→  │  tts_server.py   │
│  (轻量客户端)      │  0.1秒发完立即返回   │  (常驻后台服务)    │
│  调用:            │                    │  - pygame 预加载  │
│  python tts_send  │ ←──────────────── │  - 火山引擎 API   │
│        .py "内容"  │  播完响应          │  - 唯一文件名避免冲突│
└─────────────────┘                    └──────────────────┘
                                               │
                                        ┌──────┴──────┐
                                        │ 火山引擎 TTS  │
                                        │ API 请求音频   │
                                        └─────────────┘
```

### 调用方式
```bash
# 主用 - 后台常驻服务（0.1秒响应）
python d:\cursor_workspace\.agents\skills\edge-tts\tts_send.py "要播的内容"

# 回退 - 直接调用（服务挂了时自动用）
python d:\cursor_workspace\.agents\skills\edge-tts\tts_speak.py "要播的内容"
```

### 开机自启
VBS 脚本位于启动文件夹，开机自动静默启动：
```
C:\Users\17384\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\nova_tts_server.vbs
```

### 配置信息
- **主脚脚本**: `tts_server.py`（常驻后台）/ `tts_send.py`（轻量客户端）
- **回退脚本**: `tts_speak.py`（冷启动，保底方案）
- **API Key**: `e5730190-6ea2-4bc4-bff4-c603e5131371`
- **Speaker**: `S_FWAq1oZ42`（Nova 的御姐音色）
