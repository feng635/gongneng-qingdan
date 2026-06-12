# -*- coding: utf-8 -*-
"""AutoSend v4 - 打不死版"""
import sys, io, os, time, threading, traceback

LOG = r'D:\autosend_debug.log'
PID_FILE = r'D:\autosend.pid'

def log(msg):
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(f'{time.strftime("%H:%M:%S")} {msg}\n')

# 写 PID 文件防重复启动
try:
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))
except:
    pass

log('=== AutoSend 启动 ===')

try:
    import keyboard, pyautogui, pyperclip
except Exception as e:
    log(f'导入失败: {e}')
    sys.exit(1)

state = 'idle'
press_count = 0
lock = threading.Lock()
clip_cache = ''
stop_detect = False


def get_active_window():
    try:
        import ctypes
        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        length = user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        return buf.value
    except:
        return ''


def is_vscode_active():
    title = get_active_window()
    return 'Visual Studio Code' in title or 'cursor' in title.lower()


def send_enter():
    try:
        if is_vscode_active():
            pyautogui.press('enter')
            log('已发送 Enter！（VS Code）')
        else:
            log(f'跳过 Enter（不在 VS Code）')
    except Exception as e:
        log(f'发送 Enter 失败: {e}')


def detect_clipboard():
    global clip_cache, stop_detect, state
    log('开始检测剪贴板...')
    try:
        for i in range(30):
            if stop_detect:
                log('检测被中止')
                return
            try:
                current = pyperclip.paste()
                if current and current != clip_cache and len(current.strip()) > 2:
                    log(f'检测到文字! ({current.strip()[:30]}...)')
                    time.sleep(0.3)
                    with lock:
                        if state == 'waiting':
                            send_enter()
                            clip_cache = current
                            state = 'idle'
                    return
            except:
                pass
            time.sleep(0.5)
        log('超时未检测到文字')
    except Exception as e:
        log(f'检测出错: {e}')
    finally:
        with lock:
            if state == 'waiting':
                state = 'idle'


def on_hotkey():
    global press_count, clip_cache, stop_detect, state
    try:
        with lock:
            press_count += 1
            count = press_count
        log(f'触发 #{count}')

        if count % 2 == 1:
            stop_detect = True
            time.sleep(0.1)
            with lock:
                stop_detect = False
                try:
                    clip_cache = pyperclip.paste()
                except:
                    clip_cache = ''
                state = 'recording'
            log(f'开始录音')
        else:
            with lock:
                state = 'waiting'
            threading.Thread(target=detect_clipboard, daemon=True).start()
            log(f'停止录音，检测中...')
    except Exception as e:
        log(f'on_hotkey 出错: {e}')


# 注册热键
try:
    keyboard.add_hotkey('ctrl+win', on_hotkey, suppress=False)
    log('Ctrl+Win 注册成功！')
except Exception as e:
    log(f'注册热键失败: {e}')
    sys.exit(1)

log('就绪！')

# 用轮询代替 keyboard.wait，更稳定
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    log('手动退出')
except Exception as e:
    log(f'意外退出: {e}')
    traceback.print_exc()
