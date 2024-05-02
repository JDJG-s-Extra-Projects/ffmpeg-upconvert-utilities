#!/usr/bin/env bash
args="$@"
is_nvidia=false
is_amd=false

if which nvidia-smi &> /dev/null; then
    echo "NVIDIA driver detected, using runtime and encoders..."
    is_nvidia=true
else
    echo "Naively assuming AMD, using VAAPI..."
    is_amd=true
fi

for source in "$@"; do
    base=$(basename "$source")
    target="${base}-upgraded.mp4"

    if [ "$is_nvidia" = true ]; then
        docker run --rm -it \
            --runtime=nvidia \
            -v $(pwd):/config \
            linuxserver/ffmpeg \
            -hwaccel nvdec \
            -i "/config/$base" \
            -c:v h264_nvenc \
            -b:v 8M \
            -vtag hvc1 \
            -vf scale=1920:1080 \
            -preset fast \
            -c:a copy \
            "/config/$target"
    elif [ "$is_amd" = true ]; then
        docker run --rm -it \
            --device=/dev/dri:/dev/dri \
            -v $(pwd):/config \
            linuxserver/ffmpeg \
            -vaapi_device /dev/dri/renderD128 \
            -i "/config/$base" \
            -c:v hevc_vaapi \
            -b:v 8M \
            -vtag hvc1 \
            -vf "format=nv12,hwupload,scale_vaapi=w=1920:h=1080" \
            -crf 20 \
            -preset fast \
            -c:a copy \
            "/config/$target"
    fi
done
