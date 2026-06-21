import os
import requests

from dotenv import load_dotenv

load_dotenv()

API_USER = os.getenv("API_USER")
API_SECRET = os.getenv("API_SECRET")


def analyze_frame(image_path):

    url = "https://api.sightengine.com/1.0/check.json"

    data = {

        "models": "genai",

        "api_user": API_USER,

        "api_secret": API_SECRET

    }

    with open(image_path, "rb") as media:

        response = requests.post(

            url,

            data=data,

            files={"media": media}

        )

    return response.json()