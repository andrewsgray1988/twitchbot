import config
import asyncio

from functions.general import (
    save_all_jsons,
    load_json,
    log_text
)
from functions.twitch import (
    send_message
)
from config import (
    AUTOSAVE_TIMER,
    MESSAGE_DELAY
)

async def autosave_loop():
    while config.TASK_FLAG:
        try:
            save_all_jsons()
            log_text("JSONs saved")
        except Exception as e:
            log_text(f"Failed to save JSONs: {e}")
        await asyncio.sleep(AUTOSAVE_TIMER)

async def message_loops():
    await send_message("Welcome to the stream! Sit back, relax, and let's have some fun shall we?")
    message_list = load_json("messages.json")
    await asyncio.sleep(MESSAGE_DELAY)

    while config.TASK_FLAG:
        try:
            message = message_list.pop(0)
            await send_message(message)
            message_list.append(message)
            await asyncio.sleep(MESSAGE_DELAY)
        except Exception as e:
            log_text(f"Failed to send message: {e}")
            await asyncio.sleep(MESSAGE_DELAY)