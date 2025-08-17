import aiohttp
from common.config import settings

API_URL = "https://api.api-ninjas.com/v1/imagetotext"



async def extract_text_from_image(file_path: str) -> str:
    headers = {"X-Api-Key": settings.api_ninjas_key}
    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as f:
            data = {"image": f}
            async with session.post(API_URL, headers=headers, data=data) as r:
                if r.status != 200:
                    text = await r.text()
                    raise Exception(f"API failed: {r.status} {text}")
                result = await r.json()
                return " ".join([item["text"] for item in result])
