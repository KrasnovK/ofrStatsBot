import json
import time

from dotenv import load_dotenv

import os

load_dotenv()

TLG_TOKEN = os.environ.get("TLG_TOKEN")
TOKEN = os.environ.get("TOKEN")
PRID = os.environ.get("PRID")
URL = os.environ.get("URL")
ADMIN_ID = int(os.environ.get("TLG_ADMIN"))


with open("file.json", "r", encoding="utf-8") as json_file:
    JSON = json.load(json_file)


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f"Время выполнения {func}: {time.time() - start_time}")
        return result

    return wrapper
