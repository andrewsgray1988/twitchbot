import os
import json
import config
import asyncio

from datetime import datetime
from functions.tasks import (
    autosave_loop,
    auto_ads,
    message_loops
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_DIR = "information"

def load_json(file):
    with open(os.path.join(BASE_DIR, JSON_DIR, file)) as json_file:
        return json.load(json_file)

def save_json(file, data):
    full_path = os.path.join(BASE_DIR, JSON_DIR, file)
    with open(full_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

def is_mod(user_name:str) -> bool:
    return user_name.lower() in config.MOD_LIST

def save_all_jsons():
    save_json("mods.json", config.MOD_LIST)

def start_tasks():
    if config.TASK_FLAG:
        return

    config.TASK_FLAG = True
    asyncio.create_task(autosave_loop())
    asyncio.create_task(auto_ads())
    asyncio.create_task(message_loops())

def log_text(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_dir = os.path.join(BASE_DIR, JSON_DIR)
    full_path = os.path.join(log_dir, "error_log.txt")
    with open(full_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]: {message}\n")