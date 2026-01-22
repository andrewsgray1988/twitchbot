import random

from twitchio.ext import commands
from git_ignore.private_constants import *
from functions.commands import setup_commands
from functions.general import (
    load_json,
    save_json,
    mod_log
)
from functions.twitch import (
    send_message,
    send_ttm_message
)

# Create the bot instance
bot = commands.Bot(
    token=ACCESS_TOKEN,
    prefix="!",
    initial_channel=TWITCH_CHANNEL
)

setup_commands(bot)

chat_stats = set(load_json("chatters.json"))
tasks_started = False

@bot.event
async def event_ready():
    global tasks_started
    print("Bot loading...")

    await bot.wait_for_ready()

    print("Bot ready!")

# Event: when a message is received
@bot.event
async def event_message(message):
    username_lower = message.author.name.lower()
    if message.echo:
        return
    else:
        if username_lower not in chat_stats:
            chat_stats[username_lower] = {"messages": 0}
        chat_stats[username_lower]["messages"] += 1
    await bot.handle_commands(message)

@bot.event
async def event_raw_usernotice(channel, tags):
    msg_id = tags.get("msg_id")

    if msg_id != "reward-redeemed":
        return

    user = tags.get("display_name")
    reward_name = tags.get("msg-param-reward-title")
    user_input = tags.get("msg-param-user-input", "")
    user_input = user_input.replace("\n", "").replace("\t", "")
    user_input = user_input.title().capitalize()

    if reward_name == "Add to Hoard":
        hoard = load_json("hoard.json")
        hoard.append(user_input)
        save_json("hoard.json", hoard)
        await send_ttm_message(f"{user} has contributed a {user_input} to the hoard!")
    elif reward_name == "Steal from the Hoard":
        hoard = load_json("hoard.json")
        if not hoard:
            coin_amount = random.randint(1, 1000)
            await send_ttm_message(f"The hoard's looking a little bare, {user} has only managed to find {coin_amount} gold coins...")
        else:
            item = random.choice(hoard)
            hoard.remove(item)
            save_json("hoard.json", hoard)
            await send_ttm_message(f"{user} has snuck into the hoard, and came back with {item}!")
    elif reward_name == "Hydrate!":
        await send_message(f"{user} is sending out a reminder to everyone to hydrate, or die-drate!")
    elif reward_name == "Suggest a Command":
        mod_log(f"Suggest a command used for a command - {user_input}")

if __name__ == "__main__":
    bot.run()
