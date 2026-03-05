import logging
import time
import whisper

import utils as utils

from pathlib import Path

logger = logging.getLogger(__name__)


def transcribe_wav(audio_file_path: Path | None) -> str:
    '''
    Call openai whisper model to transcribe wav to text
    '''

    logger.debug('psst...')
    logger.info('Transcribing wav')

    if audio_file_path == None:
        logger.error('No audio file received.')
        return ''

    start_time = time.perf_counter()

    model_name = 'tiny'
    model = whisper.load_model(model_name)
    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    logger.info(f'Loaded model: {model_name} in {elapsed_time:.4f} seconds')

    result = model.transcribe(str(audio_file_path))
    text = result.get('text')

    return str(text)
