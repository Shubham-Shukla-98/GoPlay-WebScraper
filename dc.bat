@echo off
set filename=%1
cls
set dcode=%2
cls
md Downloads
cls
goto downloadmkv

:downloadmkv
echo "Downloading %filename%.mkv... Please wait..."

"%~dp0ffmpeg.exe" -loglevel error -stats -i "https://goplay.anontpp.com/?dcode=%dcode%&quality=1080p&downloadmp4vid=1" -i "https://goplay.anontpp.com/?dcode=%dcode%&downloadccsub=1" -headers "Origin: https://goplay.cf" -c copy -disposition:s:0 default -bsf:a aac_adtstoasc "%~dp0Downloads\%filename%.mkv"
goto exit

:exit
pause
exit