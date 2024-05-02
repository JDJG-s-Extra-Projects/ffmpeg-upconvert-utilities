#!/bin/bash

for SOURCE in "$@"
do
    BASE="${SOURCE%.*}"
    TARGET="${BASE} upgraded.mp4"
    QUALITY="${BASE} quality.mp4"

    echo "time to upconvert the video"
    ffmpeg -i "${SOURCE}"-c:v hevc_nvenc -qp 17 -vf scale=1920x1080:flags=lanczos "${TARGET}"
    echo "finished upconverting"
    echo "comparasion time"
    ffmpeg -i "${SOURCE}" -i "${TARGET}" -c:v hevc_nvenc -qp 17 -filter_complex "[0]pad=iw:1080:0:(1080-ih)/2,hstack" "${QUALITY}"
    echo "done generating"
done
