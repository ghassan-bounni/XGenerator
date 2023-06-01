import os
import logging
import time
from io import BytesIO
import boto3
import requests
from PIL import Image
from botocore.exceptions import ClientError
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
        return Image.open(BytesIO(requests.get(upscaled_url).content))
    else:
        return None
