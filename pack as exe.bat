chcp 65001
@echo off
TITLE     autoClick_XingC 一键打包工具
color 3f
mode con cols=90 lines=29
echo.
ECHO. =================================================
echo. 		autoClick_XingC 一键打包工具 byXingC
echo     --按任意键继续
echo.
ECHO. =================================================
pause >nul
CLS
ECHO. =================================================
echo.	耐心等待...
pyinstaller -F --workpath workpath --distpath . -n autoClick_XingC autoClick.py
del /f /s autoClick_XingC.spec
rd /s /q __pycache__
rd /s /q lib\__pycache__
rd /s /q workpath
ECHO. =================================================
echo.
echo     --按任意键关闭
pause >nul
