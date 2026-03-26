import logging

from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

def generate_recipe(client: genai.Client, title: str, description: str, transcription: str, video_text: str) -> str:

    json_schema = '''
        {
          'title': 'string',
          'summary': 'string',
          'ingredients': [
            {
              'item': 'string',
              'quantity': 'string|null',
              'unit': 'string|null',
              'preparation': 'string|null',
              'optional': false,
              'source_evidence': ['transcript', 'onscreen_text']
            }
          ],
          'steps': [
            {
              'step_number': 1,
              'instruction': 'string',
              'time_seconds': null,
              'temperature_f': null,
              'tool': null,
              'source_evidence': ['transcript']
            }
          ],
          'tools': ['air fryer', 'blender'],
          'tags': ['high-protein', 'mexican'],
          'missing_information': ['exact shrimp quantity not stated'],
          'confidence': 'high'
        }
    '''

    system_instruction = f'''
        You are extracting a recipe from imperfect multimodal evidence.

        Rules:
        - Use only the provided evidence.
        - Prefer title/description for dish name and tags.
        - Always prefer the more specific value when information is available in multiple sources.
        - Note the conflict in missing_information if there is an explicit discrepancy.
        - If information is missing or ambiguous, set fields to null and record the issue in missing_information.
        - Do not invent ingredient quantities, cook times, or temperatures.
        - Return only valid JSON matching the schema.

        JSON schema: {json_schema}
    '''

    content = f'''
        video_title: {title},
        video_description: {description},
        video_transcription: {transcription},
        video_ocr: {video_text}
    '''

    response = client.models.generate_content(
        model='gemini-3-flash-preview',
        config=types.GenerateContentConfig(system_instruction=system_instruction),
        contents=content
    )

    return response.text or ''


