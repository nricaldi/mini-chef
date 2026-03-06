import easyocr
import logging

import cv2 as cv

from pathlib import Path

logger = logging.getLogger(__name__)


def process_video(video_file_path: Path | None) -> str:
    logger.info('Procssing video file...')

    if video_file_path == None:
        logger.error('No audio file received.')
        return ''

    reader = easyocr.Reader(['en'], gpu=True)
    cap = cv.VideoCapture(video_file_path)

    frame_count = 0
    while cap.isOpened():
        frame_count += 1
        ret, frame = cap.read()
        if not ret:
            logger.info('Cannot receive frame (stream end?). Exiting...')
            break

        logger.info(f'Frame: {frame_count}')
        cv.imshow('Video', frame)

        # results = reader.readtext(frame, detail=0)
        results = reader.readtext(frame, paragraph=True)
        logger.info(results)

        # Press 'q' to exit the loop
        # cv.waitKey(25) adds a delay (in milliseconds) between frames to control playback speed
        if cv.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

    return ''
