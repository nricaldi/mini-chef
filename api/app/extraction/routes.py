import logging

from fastapi import APIRouter

from app.extraction.models import VideoRequest
from app.extraction.service import ExtractionService


logger = logging.getLogger("uvicorn.error")
router = APIRouter(tags=["admin"])


@router.post('/process-video')
async def post_video(request: VideoRequest):

    logger.info('Hello')

    extraction_service = ExtractionService()

    metadata = await extraction_service.extract(request.url)

    logger.info(f'TITLE: {metadata.title}')
    logger.info(f'DESCRIPTION: {metadata.description}')
    logger.info(f'IMAGE URL: {metadata.image_url}')

    return { 'message' : 'WOO we got a recipe' }
