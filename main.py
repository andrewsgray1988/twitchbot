import random
import asyncio
import config

from twitchio.ext import commands
from git_ignore.private_constants import ACCESS_TOKEN, TWITCH_CHANNEL
from functions.commands import setup_commands
from functions.panel import start_panel
from functions.general import mod_log
from functions.twitch import (
    init_bot,
    send_ttm_message
)

# Create the bot instance
bot = commands.Bot(
    token=ACCESS_TOKEN,
    prefix="!",
    initial_channel=TWITCH_CHANNEL
)

setup_commands(bot)
init_bot(bot)

@bot.event
async def event_ready():
    print("Bot loading...")
    await bot.wait_for_ready()
    print("Bot ready!")

# Event: when a message is received
@bot.event
async def event_message(message):
    if message.echo:
        return
    username_lower = message.author.name.lower()
    if username_lower not in config.CHAT_STATS:
            config.CHAT_STATS[username_lower] = {"messages": 0}

    config.CHAT_STATS[username_lower]["messages"] += 1
    await bot.handle_commands(message)

@bot.event
async def event_raw_usernotice(channel, tags):
    msg_id = tags.get("msg_id")

    if msg_id != "reward-redeemed":
        return

    user = tags.get("display_name")
    reward_name = tags.get("msg-param-reward-title")
    user_input = tags.get("msg-param-user-input", "").strip().title()

    if reward_name == "Add to Hoard":
        config.HOARD.append(user_input)
        await send_ttm_message(f"{user} has contributed a {user_input} to the hoard!")
    elif reward_name == "Steal from the Hoard":
        if not config.HOARD:
            coin_amount = random.randint(1, 1000)
            await send_ttm_message(f"The hoard's looking a little bare, {user} has only managed to find {coin_amount} gold coins...")
        else:
            item = random.choice(config.HOARD)
            config.HOARD.remove(item)
            await send_ttm_message(f"{user} has snuck into the hoard, and came back with {item}!")
    elif reward_name == "Hydrate!":
        await send_ttm_message(f"{user} is sending out a reminder to everyone to hydrate, or die-drate!")
    elif reward_name == "Suggest a Command":
        mod_log(f"Suggest a command used for a command - {user_input}")

def main():
    loop = asyncio.get_event_loop()
    start_panel(loop)
    bot.run()

if __name__ == "__main__":
    main()
