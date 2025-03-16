@echo off
setlocal

if "%1"=="" (
    echo Drag and drop your video file onto this script.
    pause
    exit /b 1
)

set "INPUT_FILE=%~1"
set "INPUT_FILENAME=%~n1"
set "OUTPUT_FILE=%INPUT_FILENAME% video short.mp4"

echo Processing "%INPUT_FILE%"...

ffmpeg -i "%INPUT_FILE%" -vf "scale=1080:1080,format=yuv420p,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v hevc_nvenc -c:a copy "%OUTPUT_FILE%"

if errorlevel 1 (
    echo An error occurred during processing.
    pause
    exit /b 1
)

echo Processing complete. Output saved as "%OUTPUT_FILE%".
pause
exit /b 0