import logging

from fastapi import FastAPI

from app.extraction.routes import router


logger = logging.getLogger("uvicorn.error")

app = FastAPI()
app.include_router(router)


# TODO - Endpoints

#  /recipes
# - POST

# PURPOSE
# - accept url
# - process recipe
# - return formatted recipe
