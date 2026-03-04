import logging
import random
import subprocess
import time

from pathlib import Path

logger = logging.getLogger(__name__)


def random_sleep(min_seconds: float = 0.0, max_seconds: float = 5.0) -> None:
    if min_seconds < 0 or max_seconds < 0:
        raise ValueError('Sleep bounds must be non-negative.')

    if min_seconds > max_seconds:
        raise ValueError('min_seconds must be less than or equal to max_seconds.')

    random_num = random.uniform(min_seconds, max_seconds)
    time.sleep(random_num)


def convert_mp4_to_wav(mp4_path: Path, *, overwrite: bool = False) -> Path:
    '''
    Converts an MP4 file to a WAV file using ffmpeg via subprocess.
    Define the ffmpeg command:
        -i: specifies the input file
        -vn: disables video recording (output only audio)
        -acodec pcm_s16le: sets the audio codec to PCM signed 16-bit little-endian (standard for WAV)
        -ar 44100: sets the audio sample rate to 44.1 kHz (standard CD quality)
        -ac 2: sets the audio channels to stereo (2 channels)
    '''
    logger.info('Generating wav file...')

    if mp4_path.suffix.lower() != '.mp4':
        raise ValueError(f'Input file must end with .mp4: {mp4_path}')

    if not mp4_path.exists():
        raise FileNotFoundError(f'Input file not found: {mp4_path}')

    if not mp4_path.is_file():
        raise ValueError(f'Input path is not a file: {mp4_path}')

    wav_path = mp4_path.with_suffix('.wav')
    if wav_path.exists() and not overwrite:
        logger.info(f'Wav file already exists, skipping conversion: {wav_path}')
        return wav_path

    command = [
        'ffmpeg',
        '-i',
        str(mp4_path),
        '-vn',
        '-acodec',
        'pcm_s16le',
        '-ar',
        '44100',
        '-ac',
        '2',
        str(wav_path),
    ]

    try:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=120,
        )
    except FileNotFoundError as error:
        raise FileNotFoundError('ffmpeg not found. Install ffmpeg and ensure it is in PATH.') from error
    except subprocess.TimeoutExpired as error:
        raise RuntimeError(f'ffmpeg conversion timed out for: {mp4_path}') from error
    except subprocess.CalledProcessError as error:
        stderr_output = (error.stderr or '').strip()
        raise RuntimeError(f'ffmpeg conversion failed for {mp4_path}: {stderr_output}') from error

    if not wav_path.exists() or wav_path.stat().st_size == 0:
        raise RuntimeError(f'WAV output missing or empty: {wav_path}')

    logger.info(f'Successfully converted {mp4_path} to {wav_path}')
    return wav_path
