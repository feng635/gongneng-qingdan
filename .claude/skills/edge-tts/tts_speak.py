"""
Nova 语音播报脚本
火山引擎 TTS → pygame 播放 → 播完自动删
调用方式: python tts_speak.py "要说的内容"
"""
import requests, json, base64, pygame, time, os, sys

# 火山引擎配置
API_KEY = 'e5730190-6ea2-4bc4-bff4-c603e5131371'
APP_ID = '7221054544'
SPEAKER = 'S_FWAq1oZ42'  # Nova 的御姐音色

def speak(text):
    if not text or len(text.strip()) < 2:
        return

    print(f"[语音] 播报: {text[:60]}...")

    # 1. 调用火山引擎 TTS
    url = 'https://openspeech.bytedance.com/api/v3/tts/unidirectional'
    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': API_KEY,
        'X-Api-Resource-Id': 'volc.megatts.default'
    }
    body = {
        'user': {'uid': '1'},
        'req_params': {
            'text': text,
            'speaker': SPEAKER,
            'audio_params': {'format': 'mp3', 'sample_rate': 24000, 'speed_ratio': 0.95}
        }
    }

    r = requests.post(url, json=body, headers=headers, timeout=30, stream=True)

    # 2. 收集音频数据（流式响应，每行一个 JSON）
    audio_data = b''
    for line in r.iter_lines(decode_unicode=False):
        if not line:
            continue
        try:
            d = json.loads(line)
            if d.get('code') == 0 and d.get('data'):
                audio_data += base64.b64decode(d['data'])
        except Exception:
            continue

    # 3. 播放
    if len(audio_data) < 1000:
        print(f"[语音] 音频数据不足 ({len(audio_data)} bytes)，跳过")
        return

    import uuid, glob
    # 先清理上次残留
    for old in glob.glob('d:/cursor_workspace/downloads/tts_*.mp3'):
        try: os.remove(old)
        except: pass
    temp_path = f'd:/cursor_workspace/downloads/tts_{uuid.uuid4().hex[:8]}.mp3'
    with open(temp_path, 'wb') as f:
        f.write(audio_data)

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.quit()
    except Exception as e:
        print(f"[语音] 播放出错: {e}")
    finally:
        # 播完等一会儿自动删
        try:
            time.sleep(0.2)
            os.remove(temp_path)
        except:
            pass

    print(f"[语音] 播放完成")

if __name__ == '__main__':
    text = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else ''
    if text:
        speak(text)
    else:
        print("用法: python tts_speak.py <要说的内容>")
