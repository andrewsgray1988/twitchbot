import config
import asyncio

from functions.general import (
    save_all_jsons,
    load_json
)
from _ import log_text
from functions.twitch import (
    run_ad,
    send_message
)
from config import (
    AUTOSAVE_TIMER,
    FIRST_AD,
    AD_LENGTH,
    AD_ALERT,
    AD_SPACING,
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

async def auto_ads():
    counter = 1
    await asyncio.sleep(FIRST_AD)

    while config.TASK_FLAG:
        try:
            success = await run_ad(AD_LENGTH)
            if not success:
                await asyncio.sleep(AD_ALERT)
                continue

            if counter == 0:
                await send_message(
                    f"Ads have started, and will be back after {AD_LENGTH} seconds!"
                )

        except Exception as e:
            log_text(f"Failed to automatically run ads: {e}")
            await asyncio.sleep(AD_ALERT)
            continue

        await asyncio.sleep(AD_LENGTH)

        if counter > 0:
            await send_message("Hang tight, the stream will be starting soon!")
            counter -= 1
        else:
            await send_message("Ads are over!")
        await asyncio.sleep(AD_ALERT)

        minutes = AD_SPACING // 60
        await send_message(
            f"Ads coming up in {minutes} minutes. "
            "Story moments will wait til ads are over to continue!"
        )
        await asyncio.sleep(AD_SPACING)

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