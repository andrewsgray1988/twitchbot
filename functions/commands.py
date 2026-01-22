import aiohttp

from twitchio.ext import commands
from functions.general import log_text
from functions.twitch import get_channel_info
from general import (
    is_mod
)

def setup_commands(bot: commands.Bot):
    @bot.command(name="shoutout")
    async def shoutout(ctx, target: str):
        if is_mod(ctx.author.name):
            info = await get_channel_info(target)
            if not info:
                await ctx.send(f"Check out @{target}, for being a cool and awesome person!")
                log_text(f"get_channel_info did not work for {target}.")
                return

            game_name = info.get("game_name", "something awesome")
            await ctx.send(f"Check out @{target}, they were last streaming {game_name} and are a rock star!")

    @bot.command(name="socials")
    async def socials(ctx):
        await ctx.send("You can find me on Bluesky at https://bsky.app/profile/prancingmad.bsky.social")

    @bot.command(name="lurk")
    async def lurk(ctx):
        poster = ctx.author.name
        await ctx.send(f"{poster} is going into lurk mode! I appreciate anyone who spends some time with me, lurkers and all!")

    @bot.command(name="hug")
    async def hug(ctx, target: str):
        poster = ctx.author.name
        await ctx.send(f"{poster} has sent {target} a hug!")