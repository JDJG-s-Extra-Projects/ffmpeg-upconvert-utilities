@echo off

:loop
set "SOURCE=%1"
set "BASE=%~n1"
set "TARGET=%BASE% upgraded.mp4"
set "QUALITY=%BASE% quality.mp4"

ffmpeg -i "%SOURCE%" -c:v hevc_nvenc -qp 17 -vf scale=1920x1080:flags=lanczos "%TARGET%"
ffmpeg -i "%SOURCE%" -i "%TARGET%" -c:v hevc_nvenc -qp 17 -filter_complex "[0]pad=iw:1080:0:(1080-ih)/2,hstack" "%QUALITY%"
shift
if not "%~1"=="" goto loop