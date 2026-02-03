import aiohttp

from functions.general import log_text
from git_ignore.private_constants import (
    CLIENT_ID,
    OAUTH_TOKEN,
    BROADCASTER_ID,
    TWITCH_CHANNEL
)

_bot = None

def init_bot(bot):
    global _bot
    _bot = bot

async def get_channel_info(username: str):
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {OAUTH_TOKEN}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.twitch.tv/helix/users?login={username}",
            headers=headers
        ) as user_resp:
            user_data = await user_resp.json()
            if not user_data["data"]:
                return None
            user_id = user_data["data"][0]["id"]

        async with session.get(
            f"https://api.twitch.tv/helix/channels?broadcaster_id={user_id}",
            headers=headers
        ) as chan_resp:
            chan_data = await chan_resp.json()
            if not chan_data["data"]:
                return None
            return chan_data["data"][0]

async def send_message(message: str):
    if _bot is None:
        log_text("send_message failed: bot not initialized.")
        return False

    bot = _bot

    try:
        channel = bot.get_channel(TWITCH_CHANNEL)
        if not channel:
            log_text("send_message failed: channel not found.")
            return False

        await channel.send(message)
        return True

    except Exception as e:
        log_text(f"send_message failed: {e}")
        return False

async def send_ttm_message(message: str):
    return await send_message(message)