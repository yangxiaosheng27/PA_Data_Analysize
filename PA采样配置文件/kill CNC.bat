%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cd /D %~dp0

taskkill /F /im lzs386.exe
taskkill /F /im logrec.exe
taskkill /F /im cncinterpolator.exe
taskkill /F /im cncinterpreter.exe
taskkill /F /im runcontrol.exe
taskkill /F /im cncsrv.exe
taskkill /F /im qmiframe.exe

timeout /t 3
