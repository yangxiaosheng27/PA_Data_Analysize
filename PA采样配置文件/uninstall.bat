%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cd /D %~dp0

REG Delete HKEY_LOCAL_MACHINE\SOFTWARE\PowerAutomation\CncKernel\1 /v CncPlcDataDefinitions /f
REG Delete HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\PowerAutomation\CncKernel\1 /v CncPlcDataDefinitions /f

copy  "C:\PACnc\User data\CncPlcVarDefs.ini" "C:\PACnc\User data\CncPlcVarDefs.ini.backup"
del /f "C:\PACnc\User data\CncPlcVarDefs.ini"

set Options=0x5
for /f "tokens=2*" %%i in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\PowerAutomation\System" /v "Options"') do set Options=%%j
setlocal enabledelayedexpansion
set /a "Options=!Options!&0xFFEF"
reg add HKEY_LOCAL_MACHINE\SOFTWARE\PowerAutomation\System /v Options /t REG_DWORD /d %Options% /f

set Options=0x5
for /f "tokens=2*" %%i in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\PowerAutomation\System" /v "Options"') do set Options=%%j
setlocal enabledelayedexpansion
set /a "Options=!Options!&0xFFEF"
reg add HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\PowerAutomation\System /v Options /t REG_DWORD /d %Options% /f

@echo off
echo .
echo uninstall done, wait to exit...
timeout /t 5
