@echo off
title Nova 语音系统
echo ======================
echo   Nova 语音系统启动中
echo ======================

:: 启动 TTS 语音播报服务
echo [1/3] 启动 TTS 语音服务...
start /min "" "D:\python\python.exe" "D:\cursor_workspace\.claude\skills\edge-tts\tts_server.py" --bg

:: 等待 2 秒
timeout /t 2 /nobreak >nul

:: 启动看门狗（自动管理 autosend）
echo [2/3] 启动看门狗...
start /min "" "D:\python\python.exe" "D:\cursor_workspace\.claude\skills\edge-tts\watchdog.py"

:: 等待 3 秒
timeout /t 3 /nobreak >nul

:: 打开 OpenWhispr
echo [3/3] 启动 OpenWhispr...
if exist "D:\OpenWhispr\OpenWhispr.exe" (
    start "" "D:\OpenWhispr\OpenWhispr.exe"
)

echo ======================
echo   语音系统启动完成！
echo   Ctrl+Win 说话即可对话
echo ======================
