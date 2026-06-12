"""
Nova 语音播报 - 常驻后台服务
TCP socket 监听，收到文本就调火山引擎 TTS 播放
启动: python tts_server.py        (前台运行)
       python tts_server.py --bg  (后台运行，Windows 隐藏窗口)
"""
import requests, json, base64, pygame, time, os, sys
import socket, threading, atexit, signal

# ==================== 配置 ====================
HOST = '127.0.0.1'
PORT = 18765
API_KEY = 'e5730190-6ea2-4bc4-bff4-c603e5131371'
APP_ID = '7221054544'
SPEAKER = 'S_FWAq1oZ42'
RESOURCE_ID = 'volc.megatts.default'
LOCK_FILE = os.path.expanduser('~/.tts_server.lock')

# ==================== 全局 ====================
server_running = True
audio_buffer = b''
last_text = ''  # 防止重复播报同一句


def cleanup():
    """退出时清理锁文件"""
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
    except:
        pass


atexit.register(cleanup)


def is_already_running():
    """检查是否已有实例在运行"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((HOST, PORT))
        sock.close()
        return result == 0
    except:
        return False


def request_tts(text):
    """调火山引擎 TTS，返回音频数据"""
    url = 'https://openspeech.bytedance.com/api/v3/tts/unidirectional'
    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': API_KEY,
        'X-Api-Resource-Id': RESOURCE_ID,
    }
    body = {
        'user': {'uid': '1'},
        'req_params': {
            'text': text,
            'speaker': SPEAKER,
            'audio_params': {'format': 'mp3', 'sample_rate': 24000, 'speed_ratio': 0.95},
        },
    }
    try:
        r = requests.post(url, json=body, headers=headers, timeout=15, stream=True)
        audio = b''
        for line in r.iter_lines(decode_unicode=False):
            if not line:
                continue
            try:
                d = json.loads(line)
                if d.get('code') == 0 and d.get('data'):
                    audio += base64.b64decode(d['data'])
            except Exception:
                continue
        return audio if len(audio) >= 1000 else b''
    except Exception as e:
        print(f"[TTS服务] API 请求失败: {e}")
        return b''


def play_audio(audio_data):
    """播放音频（pygame 已初始化）"""
    import uuid
    temp_path = f'd:/cursor_workspace/downloads/tts_{uuid.uuid4().hex[:8]}.mp3'
    try:
        with open(temp_path, 'wb') as f:
            f.write(audio_data)
        # pygame 已经在主线程初始化好了
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.05)
        # 播完后释放文件句柄，才能删掉
        pygame.mixer.music.unload()
    except Exception as e:
        print(f"[TTS服务] 播放出错: {e}")
    finally:
        try:
            os.remove(temp_path)
        except Exception as e:
            print(f"[TTS服务] 删除临时文件失败: {e}")


def handle_client(conn):
    """处理单个客户端请求"""
    global last_text
    try:
        data = conn.recv(4096)
        if not data:
            return
        try:
            msg = json.loads(data.decode('utf-8'))
            text = msg.get('text', '').strip()
        except:
            conn.close()
            return

        if not text or len(text) < 2:
            conn.send(b'{"ok":false,"err":"text too short"}')
            conn.close()
            return

        # 防重复（100ms 内的相同文本跳过）
        if text == last_text:
            conn.send(b'{"ok":true,"cached":true}')
            conn.close()
            return
        last_text = text

        print(f"[TTS服务] 播报: {text[:50]}...")
        conn.send(b'{"ok":true,"status":"audio_start"}')
        conn.close()

        # 请求 TTS 并播放（不在 conn 生命周期内做，避免阻塞客户端）
        audio = request_tts(text)
        if audio:
            play_audio(audio)
            print(f"[TTS服务] 播放完成")
        else:
            print(f"[TTS服务] 音频数据不足，跳过")

    except Exception as e:
        print(f"[TTS服务] 客户端处理错: {e}")
        try:
            conn.send(json.dumps({'ok': False, 'err': str(e)}).encode())
        except:
            pass
        try:
            conn.close()
        except:
            pass


def handle_client_with_audio(conn):
    """处理客户端请求，在 conn 关闭前完成整个流程（同步模式）"""
    global last_text
    try:
        data = conn.recv(4096)
        if not data:
            conn.close()
            return
        try:
            msg = json.loads(data.decode('utf-8'))
            text = msg.get('text', '').strip()
        except:
            conn.send(b'{"ok":false,"err":"bad json"}')
            conn.close()
            return

        if not text or len(text) < 2:
            conn.send(b'{"ok":false,"err":"text too short"}')
            conn.close()
            return

        print(f"[TTS服务] 播报: {text[:50]}...")

        audio = request_tts(text)
        if audio:
            play_audio(audio)
            conn.send(b'{"ok":true,"status":"played"}')
            print(f"[TTS服务] 播放完成")
        else:
            conn.send(b'{"ok":false,"err":"no audio data"}')
    except Exception as e:
        print(f"[TTS服务] 错误: {e}")
        try:
            conn.send(json.dumps({'ok': False, 'err': str(e)}).encode())
        except:
            pass
    finally:
        try:
            conn.close()
        except:
            pass


def run_server():
    """启动服务"""
    global server_running, last_text

    # 写锁文件
    with open(LOCK_FILE, 'w') as f:
        f.write(str(os.getpid()))

    # 初始化 pygame（只做一次！）
    print("[TTS服务] 初始化 pygame...")
    pygame.mixer.init(frequency=24000)
    print("[TTS服务] pygame 就绪")

    # 启动时清理残留的临时音频文件
    import glob
    for old in glob.glob('d:/cursor_workspace/downloads/tts_*.mp3'):
        try: os.remove(old)
        except: pass
    print("[TTS服务] 临时文件已清理")

    # 创建 socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(5)
    sock.settimeout(1.0)  # 每秒检查一次是否要退出
    print(f"[TTS服务] 监听 {HOST}:{PORT}，等待播报指令...")

    while server_running:
        try:
            conn, addr = sock.accept()
            # 每个请求用新线程处理（同步模式，客户端发完等播完才返回）
            t = threading.Thread(target=handle_client, args=(conn,))
            t.daemon = True
            t.start()
        except socket.timeout:
            continue
        except Exception as e:
            if server_running:
                print(f"[TTS服务] accept 错误: {e}")

    sock.close()
    print("[TTS服务] 已停止")


def signal_handler(sig, frame):
    global server_running
    server_running = False


if __name__ == '__main__':
    # 检查是否已有实例
    if is_already_running():
        print("[TTS服务] 已有实例在运行 (端口已被占用)")
        sys.exit(0)

    # 注册退出信号
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # 是否后台运行
    if '--bg' in sys.argv:
        # Windows 下后台运行
        if sys.platform == 'win32':
            import subprocess
            # 用 CREATE_NO_WINDOW 隐藏窗口
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen(
                [sys.executable, __file__],
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print("[TTS服务] 已在后台启动")
            sys.exit(0)
        else:
            # Linux/Mac 用 fork
            pid = os.fork()
            if pid > 0:
                print(f"[TTS服务] 已在后台启动 (PID: {pid})")
                sys.exit(0)

    run_server()
