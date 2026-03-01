import time
import random
import logging
import subprocess

from pathlib import Path

logger = logging.getLogger(__name__)


def random_sleep(min=0.0, max=5.0):
    random_num = random.uniform(min, max)
    time.sleep(random_num)


def convert_mp4_to_wav(mp4_filename: str, wav_filename: str) -> Path:
    """
    Converts an MP4 file to a WAV file using ffmpeg via subprocess.
    """
    # Define the ffmpeg command
    # -i: specifies the input file
    # -vn: disables video recording (output only audio)
    # -acodec pcm_s16le: sets the audio codec to PCM signed 16-bit little-endian (standard for WAV)
    # -ar 44100: sets the audio sample rate to 44.1 kHz (standard CD quality)
    # -ac 2: sets the audio channels to stereo (2 channels)
    logger.info('Generating wav file...')

    assert str(mp4_filename).endswith('.mp4'), f'Invalid mp4 filename: {mp4_filename}'

    mp4_path = Path(mp4_filename)
    assert mp4_path.exists(), f'Path not found: {mp4_path}'

    wav_path = Path(wav_filename)
    if wav_path.exists():
        logger.warning(f'Wav file already exists: {wav_path}')
        return wav_path

    command = [
        'ffmpeg',
        '-i', mp4_filename,
        '-vn',
        '-acodec', 'pcm_s16le',
        '-ar', '44100',
        '-ac', '2',
        wav_filename
    ]

    try:
        # Run the command using subprocess
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logger.info(f'Successfully converted {mp4_filename} to {wav_filename}')
        return wav_path

    except subprocess.CalledProcessError as e:
        logger.error(f'An error occurred during conversion: {e.stderr}')
    except FileNotFoundError:
        logger.error("Error: ffmpeg not found. Make sure it is installed and in your system's PATH.")
    except Exception as e:
        logger.error(e)

    raise Exception('Error converting mp4 file')
