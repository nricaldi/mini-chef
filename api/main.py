import logging

from fastapi import FastAPI
from core.models import RecipeUrl


logger = logging.getLogger('uvicorn.error')

app = FastAPI()


@app.get('/')
def read_root():
    return { 'hello' : 'world' }

@app.get('/items/{item_id}')
def read_item(item_id: int, q: str | None = None):
    return { 'item_id' : item_id, 'q' : q }

@app.post('/process-video')
def process_video(url: RecipeUrl):
    logger.info('URL RECIEVED')
    logger.info(f'URL: {url}')

    return { 'message' : 'WOO we got a recipe' }


# TODO - Endpoints

#  /recipes
# - POST

# PURPOSE
# - accept url
# - process recipe
# - return formatted recipe
