from pydantic import HttpUrl

from app.extraction.metadata import fetch_metadata


class ExtractionService:

    async def extract(self, source_url: HttpUrl):

        metadata = fetch_metadata(source_url)

        return metadata
