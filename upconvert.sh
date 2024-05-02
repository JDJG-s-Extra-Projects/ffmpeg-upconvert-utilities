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
    base="$(basename $source)"
    filename="${base%.*}"
    target="${filename}-upgraded.mp4"
    quality="${filename}-quality.mp4"

    if [ "$is_nvidia" = true ]; then
        docker run --rm -it \
            --runtime=nvidia \
            -v $(pwd):/config \
            linuxserver/ffmpeg \
            -i "/config/$base" \
            -c:v hevc_nvenc \
            -qp 17 \
            -vf scale=1920:1080:flags=lanczos \
            "/config/$target"

        docker run --rm -it \
            --runtime=nvidia \
            -v $(pwd):/config \
            linuxserver/ffmpeg \
            -i "/config/$source" \
            -i "/config/$target" \
            -c:v hevc_nvenc \
            -qp 17 \
            -filter_complex "[0]pad=iw:1080:0:(1080-ih)/2,hstack" \
            "/config/$quality"
    elif [ "$is_amd" = true ]; then
        docker run --rm -it \
            --device=/dev/dri:/dev/dri \
            -v $(pwd):/config \
            linuxserver/ffmpeg \
            -vaapi_device /dev/dri/renderD128 \
            -i "/config/$base" \
            -c:v hevc_vaapi \
            -qp 17 \
            -vf "format=nv12,hwupload,scale_vaapi=w=1920:h=1080" \
            "/config/$target"
    fi
done
