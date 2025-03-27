import os
import asyncio
import pathlib

async def create_video():
    # Determine the current directory
    current_directory = pathlib.Path(__file__).absolute().parent

    # Input and output folders are now relative to the current directory
    input_folder = current_directory / "Output"
    output_folder = current_directory / "Videos"

    # Create the output folder if it doesn't exist
    output_folder.mkdir(parents=True, exist_ok=True)

    # Find all JPG files in the input folder
    image_files = list(input_folder.rglob("*.jpg"))

    # Sort image files by creation time using pathlib
    image_files.sort(key=lambda x: x.stat().st_ctime)

    # Create the path to the temporary files.txt in the current directory
    files_txt_path = current_directory / "files.txt"

    # Create the path to the output video in the output folder
    output_video_path = output_folder / "output.mp4"

    # Create the files.txt with correct file paths
    with open(files_txt_path, "w") as file_list:
        for img_path in image_files:
            file_list.write(f"file '{str(img_path)}'\n")
            file_list.write("duration 3\n")

    # Construct the ffmpeg command using h264_nvenc and specifying color range
    ffmpeg_command = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(files_txt_path),
        '-color_range', 'pc',  # Specify full color range for input (JPEG)
        '-vf', 'scale=1280:720',
        '-framerate', '30',
        '-c:v', 'h264_nvenc',  # Use h264_nvenc encoder
        '-preset', 'slow',      # Optional: Adjust encoding preset
        '-r', '30',
        '-pix_fmt', 'yuv420p',
        str(output_video_path)
    ]

    # Run the ffmpeg command asynchronously and print output in real-time
    try:
        process = await asyncio.create_subprocess_exec(
            *ffmpeg_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        while True:
            line = await process.stderr.readline()
            if not line:
                break
            print(f"FFmpeg stderr: {line.decode().strip()}")

        await process.wait()  # Wait for the process to finish

        if process.returncode == 0:
            print("Video created successfully using h264_nvenc!")
        else:
            print(f"Error running ffmpeg. Return code: {process.returncode}")
            # stderr might already be printed, but let's capture it again just in case
            stderr_output = await process.stderr.read()
            if stderr_output:
                print(f"FFmpeg stderr (final):\n{stderr_output.decode()}")

    except FileNotFoundError:
        print("Error: ffmpeg command not found. Make sure it's in your PATH.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Remove the temporary files.txt
    if files_txt_path.exists():
        os.remove(files_txt_path)

    print("done!!!!!!")

if __name__ == "__main__":
    asyncio.run(create_video())