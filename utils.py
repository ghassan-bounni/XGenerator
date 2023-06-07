import os
import logging
import time
from io import BytesIO
import boto3
import requests
from PIL import Image
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import soundfile as sf
from streamlit.runtime.uploaded_file_manager import UploadedFile

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


def upload_file(file_name, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ["ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["SECRET_ACCESS_KEY"],
    )
    try:
        _ = s3_client.upload_file(file_name, os.environ["S3_BUCKET_NAME"], object_name)
        s3_url = f"https://{os.environ['S3_BUCKET_NAME']}.s3.amazonaws.com/{object_name}"
    except ClientError as error:
        logging.error(error)
        return False, None
    return True, s3_url


def super_resolution(url):
    response = None
    response_status = None
    response_id = None
    while response_status != "success":
        # If it's the first time or if it failed, send a new request
        if response_status != "processing":
            payload = {
                "key": os.environ["SD_API_KEY"],
                "url": url,
                "scale": 2,
                "webhook": None,
                "face_enhance": False
            }
            response = requests.post(os.environ["SD_UPSCALE_URL"], json=payload, headers={"Content-Type": "application/json"}, timeout=120).json()
            response_status = response["status"]
            response_id = response["id"] if response_status != "failed" else None
        else:
            # If it's still processing, wait 5 seconds and check again
            time.sleep(5)
            response = requests.get(
                os.environ["SD_FETCH_URL"],
                json={
                    "key": os.environ["SD_API_KEY"],
                    "request_id": response_id
                },
                headers={
                    "Content-Type": "application/json"
                },
                timeout=120
            ).json()
            response_status = response["status"]
    return response["output"]


def upscale(img: Image, aspect_ratio: float, name: str):
    ratio_to_size = {
        2 / 3: (600, 900),
        3 / 2: (900, 600),
        1.0: (750, 750)
    }
    img = img.resize(ratio_to_size[aspect_ratio], resample=Image.BICUBIC)
    img.save(name)
    success, url = upload_file(file_name=name)
    os.remove(name)
    if success:
        upscaled_url = super_resolution(url)
        return Image.open(BytesIO(requests.get(upscaled_url, timeout=120).content))
    else:
        return None


def check_audio_length(audio):
    audio_data, sample_rate = sf.read(audio)
    duration_seconds = len(audio_data) / sample_rate
    return 60 > duration_seconds > 30


def check_cloned_voice(voice_name: str):
    headers = {
        "accept": "application/json",
        "AUTHORIZATION": f"Bearer {os.getenv('PLAY_HT_SECRET_KEY')}",
        "X-USER-ID": os.getenv('PLAY_HT_USER_ID')
    }

    response = requests.get(os.environ["PLAY_HT_LIST_CLONED_VOICES_URL"], headers=headers)

    while response.status_code != 200:
        response = requests.get(os.environ["PLAY_HT_LIST_CLONED_VOICES_URL"], headers=headers)

    if not response.json():
        return None

    return next((voice["id"] for voice in response.json() if voice["name"] == voice_name), None)


def clone_voice(audio: UploadedFile, voice_name: str):
    with open(audio.name, "wb") as f:
        f.write(audio.getvalue())

    with open(audio.name, "rb") as audiofile:
        files = {"sample_file": (audio.name, audiofile, "audio/wav")}
        payload = {"voice_name": voice_name}
        headers = {
            "accept": "application/json",
            "AUTHORIZATION": "Bearer " + os.environ["PLAY_HT_SECRET_KEY"],
            "X-USER-ID": os.environ["PLAY_HT_USER_ID"]
        }

        response = requests.post(os.environ["PLAY_HT_VOICE_CLONE_URL"], data=payload, files=files, headers=headers)

        while response.status_code != 201:
            response = requests.post(os.environ["PLAY_HT_VOICE_CLONE_URL"], data=payload, files=files, headers=headers)

    os.remove("./" + audio.name)

    return response.json()["id"]


def script_to_audio(script: str, voice_id: str):
    payload = {
        "text": script,
        "voice": voice_id if voice_id else "larry",
        "quality": "high",
        "output_format": "mp3",
        "speed": 0.9,
        "sample_rate": 24000,
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "AUTHORIZATION": f"Bearer {os.getenv('PLAY_HT_SECRET_KEY')}",
        "X-USER-ID": os.getenv('PLAY_HT_USER_ID')
    }

    response = requests.post(os.environ["SCRIPT_AUDIO_CONVERT_URL"], json=payload, headers=headers).json()

    while not response["output"]:
        url = response["_links"][0]["href"]
        headers = {
            "accept": "application/json",
            "AUTHORIZATION": f"Bearer {os.getenv('PLAY_HT_SECRET_KEY')}",
            "X-USER-ID": os.getenv('PLAY_HT_USER_ID')
        }

        time.sleep(3)
        response = requests.get(url, headers=headers).json()

    with open("audio.mp3", "wb") as f:
        f.write(requests.get(response["output"]["url"], timeout=120).content)
    return "audio.mp3"
