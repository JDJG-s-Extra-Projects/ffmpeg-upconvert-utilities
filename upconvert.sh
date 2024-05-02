#!/bin/bash
# Exit on error
set -e

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null
then
    echo "ffmpeg could not be found"
    exit
fi

# Loop over all input arguments
for source in "$@"
do
    # Get the base name of the source file
    base=$(basename "$source")
    target="${base} upgraded.mp4"
    quality="${base} quality.mp4"

    # Convert the source file to hevc format and scale it
    ffmpeg -i "$source" -c:v hevc_nvenc -qp 17 -vf scale=1920x1080:flags=lanczos "$target"

    # Create a quality version of the source file
    ffmpeg -i "$source" -i "$target" -c:v hevc_nvenc -qp 17 -filter_complex "[0]pad=iw:1080:0:(1080-ih)/2,hstack" "$quality"
done
