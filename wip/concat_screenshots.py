import os
import asyncio
import pathlib

async def create_video():
    # Base directory where the script is located
    current_directory = pathlib.Path(__file__).absolute().parent

    # Input folder with screenshots
    input_folder = current_directory / "screenshots"

    # Output folder
    output_folder = current_directory
    if not input_folder.exists():
        print("screenshots/ folder does not exist.")
        return

    # Find all JPG files in the screenshots folder
    image_files = list(input_folder.glob("*.jpg"))

    # Sort image files by creation time
    image_files.sort(key=lambda x: x.stat().st_ctime)

    if not image_files:
        print("No .jpg images found in screenshots/ folder.")
        return

    files_txt_path = current_directory / "files.txt"

    # Path to the output video
    output_video_path = current_directory / "output.mp4"

    # Write image paths and durations to files.txt
    with open(files_txt_path, "w") as file_list:
        for img_path in image_files:
            file_list.write(f"file '{str(img_path)}'\n")
            file_list.write("duration 3\n")

    # FFmpeg command
    ffmpeg_command = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(files_txt_path),
        '-color_range', 'pc',
        '-vf', 'scale=1280:720',
        '-framerate', '30',
        '-c:v', 'libx264',
        '-preset', 'slow',
        '-r', '30',
        '-pix_fmt', 'yuv420p',
        str(output_video_path)
    ]

    print("tarting FFmpeg process...")
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
            print(f"FFmpeg: {line.decode().strip()}")

        await process.wait()

        if process.returncode == 0:
            print(f"Video created successfully at: {output_video_path}")
        else:
            print(f"FFmpeg failed with return code: {process.returncode}")
            stderr_output = await process.stderr.read()
            print(stderr_output.decode())

    except FileNotFoundError:
        print("ffmpeg not found. Make sure it’s installed and in your PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Clean up files.txt
    if files_txt_path.exists():
        os.remove(files_txt_path)

    print("Done!")

if __name__ == "__main__":
    asyncio.run(create_video())