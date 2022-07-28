import soundfile
import subprocess
import time
import pyloudnorm
import io

def check_audio(data):
    start = time.process_time()

    cmd = "ffmpeg -hide_banner -loglevel error -read_ahead_limit -1 -i cache:pipe: -ac 2 -f f64le -acodec pcm_f64le -ar 44100 -"
    out, err = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True).communicate(input = data)


    if err != b"":
        if err.find(b"Invalid data found when processing input") > -1:
            raise Exception("Invalid data")
        elif err.find(b"does not contain any stream") > -1:
            raise Exception("No audio")
        elif err.find(b"Inner protocol failed to seekback end") > -1:
            pass #google didn't help
        else:
            raise Exception(f"Unknown error, stderr: {err}")

    data, samplerate = soundfile.read(io.BytesIO(out), samplerate = 44100, channels = 2, format = "RAW", endian = "LITTLE", subtype = "DOUBLE")

    meter = pyloudnorm.Meter(samplerate)
    
    loudness = round(meter.integrated_loudness(data), 2)
    maxamp = round(data.__abs__().max() * 100, 1)

    return loudness, maxamp, (time.process_time() - start) * 1000

# Credit ?