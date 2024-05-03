#!/usr/bin/env bash
ARGUMENTS="$@"
DIRECTORY_NAME="config"
DIRECTORY="/$DIRECTORY_NAME"
VOLUME="$PWD:$DIRECTORY"
is_nvidia=false
is_amd=false

if which nvidia-smi &> /dev/null; then
    echo "NVIDIA driver detected, using runtime and encoders..."
    is_nvidia=true
else
    echo "Naively assuming AMD, using VAAPI..."
    is_amd=true
fi

hevc_upscale() {
    input_file="$(basename $1)"
    input_file_without_extension="${input_file%.*}"
    input="$DIRECTORY/$input_file"

    output_file="$(basename $2)"
    output_file_without_extension="${output_file%.*}"
    output="$DIRECTORY/$output_file_without_extension.mp4"

    if [ "$is_nvidia" = true ]; then
        docker run --rm -it \
            --runtime=nvidia \
            -v $VOLUME \
            linuxserver/ffmpeg \
            -i $input \
            -c:v hevc_nvenc \
            -qp 17 \
            -vf scale=1920:1080:flags=lanczos \
            $output
    elif [ "$is_amd" = true ]; then
        docker run --rm -it \
            --device=/dev/dri:/dev/dri \
            -v $VOLUME \
            linuxserver/ffmpeg \
            -vaapi_device /dev/dri/renderD128 \
            -i $input \
            -c:v hevc_vaapi \
            -qp 17 \
            -vf "format=nv12,hwupload,scale_vaapi=w=1920:h=1080" \
            $output
    fi
}

comparison_render() {
    source_file="$(basename $1)"
    source_file_without_extension="${source_file%.*}"

    comparison_file="$(basename $2)"
    comparison_file_without_extension="${comparison_file%.*}"

    input_flags="-i $DIRECTORY/$source_file -i $DIRECTORY/$comparison_file"

    output_file="$(basename $3)"
    output_file_without_extension="${output_file%.*}"
    output="$DIRECTORY/$output_file_without_extension.mp4"

    echo $input_flags

    if [ "$is_nvidia" = true ]; then
        docker run --rm -it \
            --runtime=nvidia \
            -v $VOLUME \
            linuxserver/ffmpeg \
            $input_flags \
            -filter_complex "[0]pad=iw:1080:0:(1080-ih)/2,hstack" \
            $output
    elif [ "$is_amd" = true ]; then
        echo "Comparison rendering is unsupported for AMD"
    fi
}

for source in $ARGUMENTS; do
    base="$(basename $source)"
    filename="${base%.*}"
    upscaled="${filename}-upscaled.mp4"
    final="${filename}-final.mp4"

    hevc_upscale $source $upscaled
    comparison_render $source $upscaled $final
done
