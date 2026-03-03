import asyncio
import logging

import video_downloader as video_downloader
import get_reel_details as get_reel_details
import transcribe_wav as transcribe_wav
import utils as utils

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def transcribe_mp4(audio_filepath) -> str:
    audio_wav = 'audio.wav'
    wav_path = utils.convert_mp4_to_wav(audio_filepath, audio_wav)
    logger.info(f'Path: {wav_path}')

    transcription = transcribe_wav.transcribe_wav(wav_path)
    logger.debug(f'Transcription: {transcription}')

    return transcription


async def main():
    logger.info('Hello from mini-chef!')

    insta_url = 'https://www.instagram.com/beatrizcontreras.31/reel/DVEeGePD0Mh/'
    logger.info(f'url: {insta_url}')

    # get_reel_details(instal_url)
    try:
        media = await video_downloader.download_reel_media(insta_url)

        audio_files = media.get('audio', [])
        if not audio_files:
            raise RuntimeError('No audio files found in downloaded media.')

        audio_filepath = audio_files[0]
        transcription = transcribe_mp4(audio_filepath)

        logger.info(f'Transcription: {transcription}')
        logger.info('All done thank you come again')

    except ValueError as error:
        logger.error(f'Invalid input: {error}')
    except RuntimeError as error:
        logger.error(f'Processing failed: {error}')
    except FileNotFoundError as error:
        logger.error(f'File not found: {error}')
    except Exception:
        logger.exception('Unexpected error while processing reel')


if __name__ == '__main__':
    asyncio.run(main())
