import easyocr
import logging
import time
import re

import cv2 as cv

from pathlib import Path

logger = logging.getLogger(__name__)


def _clean_frame_text(text: str) -> str:
    clean_text = text.lower()

    # Remove punctuation
    # The pattern [^A-Za-z0-9\s]+ matches any character that is NOT alphanumeric or whitespace
    clean_text = re.sub(r'[^A-Za-z0-9\s]+', '', clean_text)

    return clean_text


def process_video(video_file_path: Path | None) -> str:
    logger.info('Procssing video file...')

    if video_file_path == None:
        logger.error('No audio file received.')
        return ''

    reader = easyocr.Reader(['en'])
    cap = cv.VideoCapture(video_file_path)

    start_time = time.perf_counter()

    frame_count = 1
    frame_skip_interval = 20
    video_text = set()
    while cap.isOpened():

        success = cap.grab()
        if not success:
            break

        frame_count += 1
        if frame_count % frame_skip_interval != 0:
            continue

        ret, frame = cap.retrieve()
        if not ret:
            logger.info('Cannot receive frame (stream end?). Exiting...')
            break

        logger.info(f'Frame: {frame_count}')
        cv.imshow('Video', frame)

        results = reader.readtext(frame, paragraph=True, detail=0)
        if len(results) == 0:
            continue

        frame_text = str(results[0])
        video_text.add(_clean_frame_text(frame_text))

        # Press 'q' to exit the loop
        # cv.waitKey(25) adds a delay (in milliseconds) between frames to control playback speed
        if cv.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    logger.info(f'Processed video in {elapsed_time:.4f} seconds')

    return ' '.join(video_text)
