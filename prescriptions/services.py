import json
import google.generativeai as genai
import pytesseract
from django.conf import settings
from PIL import Image
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)
def parse_prescription(text):
    if not settings.GEMINI_API_KEY:
        raise ValueError('Gemini API key is missing. Set GEMINI_API_KEY environment variable.')
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"""
Extract medicines from this prescription text.
Return ONLY valid JSON in this format:
[
  {{
    "name": "",
    "dosage": "",
    "frequency_per_day": number,
    "timing": ""
  }}
]
Rules:
- BD = 2 times/day
- TDS = 3 times/day
- OD = 1 time/day
- Ignore unrelated text
Prescription:
{text}
"""
    response = model.generate_content(prompt)
    raw = response.text.strip()
    if raw.startswith('```'):
        raw = raw.replace('```json', '').replace('```', '').strip()
    parsed = json.loads(raw)
    if not isinstance(parsed, list):
        raise ValueError('AI output is not a JSON array.')
    return parsed