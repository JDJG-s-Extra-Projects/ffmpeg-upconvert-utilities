import asyncio
import pathlib

async def ffmpeg_process_file(file_path):
    """Processes a single video file: Upconverts to 1080p, Full RGB, and 30fps."""
    # Updated suffix to reflect the new quality
    output_file = file_path.with_stem(f"{file_path.stem}-1080p-full")

    # Filter chain:
    # 1. Sets fps to 30
    # 2. Upscales to 1920x1080 using Lanczos (sharper than default)
    # 3. Maps the input color range (Limited/16-235) to output (Full/0-255)
    filter_chain = "fps=fps=30/1,scale=1920:1080:flags=lanczos:in_range=limited:out_range=full"

    proc = await asyncio.create_subprocess_exec(
        "ffmpeg",
        "-y",
        "-stats",
        "-noautorotate",
        "-i", str(file_path),
        "-v", "error",
        "-sn",
        "-dn",
        # Metadata flags to tell video players this is Full Range BT.709
        "-color_range", "pc",
        "-colorspace", "bt709",
        "-color_primaries", "bt709",
        "-color_trc", "bt709",
        "-map", "0",
        "-f", "mp4",
        "-vsync", "0",
        "-codec:v", "h264_nvenc",
        "-preset", "p7",        # Slowest/highest quality NVENC preset
        "-rc", "vbr",           # Variable bitrate for better local quality
        "-cq", "18",            # Constant Quality (visually near-lossless)
        "-g", "2",
        "-bf", "0",
        "-codec:a", "aac",
        "-ab", "256k",
        "-filter:v", filter_chain,
        str(output_file),
    )
    
    await proc.wait()
    if proc.returncode != 0:
        print(f"ffmpeg processing failed for {file_path}")
    else:
        print(f"Successfully processed: {file_path.name}")

async def process_mp4_files(directory):
    """Processes all .mp4 files in the given directory recursively, processing sequentially."""
    # Filter out files that we already processed (those ending in our new suffix)
    files = [f for f in directory.rglob("*.mp4") if "-1080p-full" not in f.stem]
    for file in files:
        if file.is_file():
            await ffmpeg_process_file(file)

async def main():
    """Main function to start the file processing."""
    current_directory = pathlib.Path(__file__).absolute().parent
    await process_mp4_files(current_directory)
    print("All tasks complete.")

if __name__ == "__main__":
    asyncio.run(main())
