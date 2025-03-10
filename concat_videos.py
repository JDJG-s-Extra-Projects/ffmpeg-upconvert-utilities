import asyncio
import datetime
import pathlib
import subprocess

def concat_videos_cuda(input_files, output_file):
    """Concatenates video files using ffmpeg with CUDA, maintaining quality."""

    if not input_files:
        print("No input files provided.")
        return

    temp_file_list = "filelist.txt"
    with open(temp_file_list, "w") as f:
        for file in input_files:
            f.write(f"file '{file.as_posix()}'\n")

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-hwaccel",
                "cuda",
                "-hwaccel_output_format",
                "cuda",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                temp_file_list,
                "-c:v",
                "h264_nvenc", # Use NVENC for hardware encoding
                "-preset",
                "p7", #p7 is for quality
                "-c:a",
                "copy", # Copy audio streams
                output_file,
            ],
            check=True,
        )
        print(f"Videos concatenated successfully to {output_file} (CUDA)")

    except subprocess.CalledProcessError as e:
        print(f"Error concatenating videos (CUDA): {e}")

    finally:
        pathlib.Path(temp_file_list).unlink(missing_ok=True)

async def main():
    current_directory = pathlib.Path(__file__).absolute().parent
    files = list(current_directory.rglob("*.mp4"))
    files.sort(key=lambda path: path.stat().st_mtime)

    if files:
        output_filename = "concatenated_video_cuda.mp4"
        concat_videos_cuda(files, output_filename)
    else:
        print("No mp4 files found in the current directory.")

if __name__ == "__main__":
    asyncio.run(main())

# does not 100% seem to work as wanted though.
