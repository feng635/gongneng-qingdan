"""
Nova 语音播报 - 轻量客户端
把文本发给后台 TTS 服务，秒发秒回
调用: python tts_send.py "要播的内容"
"""
import socket, json, sys, subprocess, os, time

HOST = '127.0.0.1'
PORT = 18765
SERVER_SCRIPT = os.path.join(os.path.dirname(__file__), 'tts_server.py')


def is_server_running():
    """检查后台服务是否在运行"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        result = sock.connect_ex((HOST, PORT))
        sock.close()
        return result == 0
    except:
        return False


def start_server():
    """启动后台服务（等待最多 3 秒）"""
    print("[TTS] 启动后台服务...")
    # 后台启动
    if sys.platform == 'win32':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.Popen(
            [sys.executable, SERVER_SCRIPT],
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        subprocess.Popen(
            [sys.executable, SERVER_SCRIPT],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    # 等它起来
    for _ in range(30):  # 最多等 3 秒
        if is_server_running():
            return True
        time.sleep(0.1)
    return False


def send_text(text):
    """发送文本到后台服务"""
    if not text or len(text.strip()) < 2:
        return

    # 自动启动服务
    if not is_server_running():
        if not start_server():
            print("[TTS] 启动服务失败，回退到直接调 API")
            # 回退：直接调 tts_speak.py
            subprocess.Popen(
                [sys.executable,
                 os.path.join(os.path.dirname(__file__), 'tts_speak.py'),
                 text],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return

    # 发数据
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)  # 等播放完成（同步模式）
        sock.connect((HOST, PORT))

        msg = json.dumps({'text': text})
        sock.sendall(msg.encode('utf-8'))

        # 等响应（服务端播完才返回）
        response = sock.recv(1024)
        result = json.loads(response.decode('utf-8'))
        sock.close()

        if result.get('ok'):
            print(f"[TTS] 播报成功" + (" (缓存)" if result.get('cached') else ''))
        else:
            print(f"[TTS] 播报失败: {result.get('err')}")

    except ConnectionRefusedError:
        print("[TTS] 连接被拒，重试启动服务...")
        if start_server():
            # 重试一次
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock.connect((HOST, PORT))
                msg = json.dumps({'text': text})
                sock.sendall(msg.encode('utf-8'))
                response = sock.recv(1024)
                sock.close()
                print(f"[TTS] 播报成功（重试）")
            except Exception as e:
                print(f"[TTS] 重试也失败了: {e}")
        else:
            print("[TTS] 服务启动失败")
    except Exception as e:
        print(f"[TTS] 发送失败: {e}")


if __name__ == '__main__':
    text = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else ''
    if text:
        send_text(text)
    else:
        print("用法: python tts_send.py <要播报的内容>")
        sys.exit(1)
