import asyncio
import logging

import video_downloader as video_downloader
import get_reel_details as get_reel_details
import transcribe_wav as transcribe_wav
import video_processor as video_processor
import utils as utils

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


async def main():
    logger.info('Hello from mini-chef!')

    insta_url = 'https://www.instagram.com/beatrizcontreras.31/reel/DVEeGePD0Mh/'
    logger.info(f'url: {insta_url}')

    try:
        logger.info('Fetching reel details...')
        reel_details = get_reel_details.get_reel_details(insta_url)

        logger.info(f'Details found: {reel_details}')

        media = await video_downloader.download_reel_media(insta_url)

        audio_file_path = media.get('audio')
        if audio_file_path:
            audio_wav = utils.convert_mp4_to_wav(audio_file_path)
            transcription = transcribe_wav.transcribe_wav(audio_wav)

            logger.info(f'Transcription: {transcription}')
        else:
            logger.warning('No audio file found')

        video_file_path = media.get('video')

        video_text = video_processor.process_video(video_file_path)

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
