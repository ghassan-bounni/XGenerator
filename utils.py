import os
import requests
from PIL import Image
from dotenv import load_dotenv

load_dotenv()


def generate(prompt):
    headers = {
        'Authorization': f'Bearer {os.environ["OPENAI_API_KEY"]}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': 'text-davinci-003',
        'prompt': prompt,
        'max_tokens': 1500,
    }

    response = requests.post(
        os.environ["OPENAI_API_URL"],
        headers=headers,
        json=payload
    )

    api_response = response.json()
    res = api_response["choices"][0]["text"]

    return res


def upscale(img: Image, aspect_ratio: float):
    ratio_to_size = {
        2 / 3: (1200, 1800),
        3 / 2: (1800, 1200),
        1.0: (1500, 1500)
    }

    return img.resize(ratio_to_size[aspect_ratio], resample=Image.BICUBIC)
