import asyncio
import logging

import snapinsta_downloader as snapinsta_downloader
import get_reel_details as get_reel_details
import transcribe_wav as transcribe_wav
import utils as utils


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

async def main():
    logger.info('Hello from mini-chef!')

    insta_url = 'https://www.instagram.com/beatrizcontreras.31/reel/DVEeGePD0Mh/'
    print(f'url: {insta_url}')

    # await snapinsta_downloader.download_insta_video(insta_url)
    # get_reel_details(instal_url)

    audio_mp4 = 'audio_0.mp4'
    audio_wav = 'audio.wav'

    wav_path = utils.convert_mp4_to_wav(audio_mp4, audio_wav)
    logger.info(f'Path: {wav_path}')

    transcription = transcribe_wav.transcribe_wav(wav_path)
    logger.info(f'Transcription: {transcription}')

if __name__ == '__main__':
    asyncio.run(main())
