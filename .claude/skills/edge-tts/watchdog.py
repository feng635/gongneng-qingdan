# -*- coding: utf-8 -*-
"""
看门狗 - 监控 autosend，挂了自动重启
"""
import subprocess, time, sys, os

AUTOSEND = r'D:\cursor_workspace\.claude\skills\edge-tts\autosend.py'
PYTHON = r'D:\python\python.exe'
PID_FILE = r'D:\autosend.pid'
LOG = r'D:\autosend_debug.log'

def log(msg):
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(f'[看门狗] {time.strftime("%H:%M:%S")} {msg}\n')

log('看门狗启动')

process = None

while True:
    try:
        if process is None or process.poll() is not None:
            log('启动 autosend...')
            process = subprocess.Popen([PYTHON, AUTOSEND],
                                       stdout=subprocess.DEVNULL,
                                       stderr=subprocess.DEVNULL,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
            log(f'autosend 已启动 (PID: {process.pid})')
        time.sleep(10)  # 每10秒检查一次
    except KeyboardInterrupt:
        log('看门狗退出')
        if process:
            process.terminate()
        break
    except Exception as e:
        log(f'看门狗出错: {e}')
        time.sleep(5)
