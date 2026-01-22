import random

from twitchio.ext import commands
from git_ignore.private_constants import *
from functions.paths import load_json_list, load_json_dict, save_json
from functions.txt_functions import log_error, chat_box, mod_log
from functions.timer_functions import save_data_timer, obs_scene_listener, auto_ads, message_loops
from functions.command_functions import setup_commands

# Create the bot instance
bot = commands.Bot(
    token=ACCESS_TOKEN,
    prefix="!",
    initial_channel=TWITCH_CHANNEL
)

setup_commands(bot)

chat_stats = load_json_dict("chatters.json")
tasks_started = False

# Event: when the bot connects successfully
@bot.event
async def event_ready():
    global tasks_started
    print("Bot loading...")

    await bot.wait_for_ready()

    if not tasks_started:
        save_task = bot.loop.create_task(save_data_timer(bot))
        ad_task = bot.loop.create_task(auto_ads(bot))
        message_task = bot.loop.create_task(message_loops(bot))
        obs_task = bot.loop.create_task(obs_scene_listener(bot, save_task, ad_task, message_task))
        tasks_started = True

    print("Bot ready!")

# Event: when a message is received
@bot.event
async def event_message(message):
    username = message.author.name
    username_lower = message.author.name.lower()
    msg = message.content
    if message.echo:  # Prevent the bot from responding to itself
        return
    elif message.content in bot_msg_spam:
        try:
            await message.delete()
        except Exception as e:
            error_message = f"Failed to delete message from {username}: \"{msg}\" — {e}"
            log_error(error_message)
    else:
        if username_lower not in chat_stats:
            chat_stats[username_lower] = {"messages": 0}
        chat_stats[username_lower]["messages"] += 1
        count = chat_stats[username_lower]["messages"]
        chat_box(username, count, msg)
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
        hoard = load_json_list("hoard.json")
        hoard.append(user_input)
        save_json("hoard.json", hoard)
        await channel.send(f"{user} has contributed a {user_input} to the hoard!")
    elif reward_name == "Steal from the Hoard":
        hoard = load_json_list("hoard.json")
        if not hoard:
            coin_amount = random.randint(1, 1000)
            await channel.send(f"The hoard's looking a little bare, {user} has only managed to find {coin_amount} gold coins...")
        else:
            item = random.choice(hoard)
            hoard.remove(item)
            save_json("hoard.json", hoard)
            await channel.send(f"{user} has snuck into the hoard, and came back with {item}!")
    elif reward_name == "Hydrate!":
        await channel.send(f"{user} is sending out a reminder to everyone to hydrate, or die-drate!")
    elif reward_name == "Suggest a Command":
        mod_log(f"Suggest a command used for a command - {user_input}")

# Run the bot
if __name__ == "__main__":
    bot.run()
