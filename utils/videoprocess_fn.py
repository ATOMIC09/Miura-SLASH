import sys
import os
import subprocess
import ffmpy

def ssssssss(file):
    filestats = os.stat(file)
    return size_format(filestats.st_size)

# For converting bytes to bigger units
def size_format(n) :
    for u in ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"]:
        if abs(n) < 1024.0 :
            return f"{n:3.1f}{u}"
        n /= 1024.0
    return f"{n:.1f}YB"

# For compressing a video
def compressvideo(file):
    target_8mb = 8192
    file_path = f"temp/video/{file}"
    filename, ext = os.path.splitext(file_path)

    # Get the duration of the video
    ff = ffmpy.FFprobe(
    inputs={file_path : '-show_entries format=duration -v error -of default=noprint_wrappers=1:nokey=1'}
    )

    duration_byte = ff.run(stdout=subprocess.PIPE)
    duration = float(duration_byte[0].decode())
    ##########

    realfilename = os.path.basename(file_path)
    bitrate = target_8mb / duration
    original_filestats = os.stat(file_path)
    outputpath = filename + "_compressed" + ext
    outputname = filename + "_compressed"

    print(
        f"Compressing {realfilename} . . .",
        f"({size_format(original_filestats.st_size)}) | bitrate = {int(bitrate)}k"
        )
    
    # Compressing the video
    ff = ffmpy.FFmpeg(
        inputs={file_path: None},
        outputs={outputpath : f'-b {str(bitrate)}k -y'}
        )
    ff.run()

    # Print the stats of the compressed video
    final_filestats = os.stat(outputpath)
    percent = final_filestats.st_size / original_filestats.st_size
    if percent < 1 :
        percent = f"{percent:.2f}%"
    else :
        percent = f"{percent:.2f}%"

    return f"🗜 **บีบอัดเหลือ** `{size_format(final_filestats.st_size)}`**,** `{percent}` **ของไฟล์ต้นฉบับ**", outputname
