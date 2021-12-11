chcp 65001
@echo off
TITLE     autoClick_XingC 一键打包工具
color 3f
setlocal enabledelayedexpansion
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

:: 生成文件名称(不需要输入后缀名)
set exeName=autoClick_XingC

::要编译的py文件名称
set pyName=autoClick.py

::开始打包
pyinstaller -F -w --workpath workpath --distpath . -n  !exeName! !pyName!

::当前目录
set DIR="%cd%"
::要清理的文件夹名称
set cleanDIR=__pycache__

::开始清理任务
del /f /s !exeName!.spec

for /R %DIR% /d %%f in (*) do ( 
set tmp=%%f
set tmp2=!tmp:~-11!

if !tmp2!==!cleanDIR! (
rd /s /q !tmp!
) 
)
rd /s /q workpath

ECHO. =================================================
echo.
echo     --按任意键关闭
pause >nul
