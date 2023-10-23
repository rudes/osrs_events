"""
bot entrypoint that loads all cogs and starts bot
"""
import os
import logging
import discord

from discord.ext import commands

logging.basicConfig(
    format="%(asctime)s %(name)s:%(levelname)-8s %(message)s",
    filename="/var/log/osrs_events.log",
    level=logging.INFO,
)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
discord_log = logging.getLogger("discord")
discord_log.setLevel(logging.ERROR)

if __name__ == "__main__":
    bot = commands.Bot(
        debug_guilds=[1159942455752409118],
        intents=discord.Intents.all(),
    )

    bot.load_extensions("commands", "handlers")
    bot.run(str(os.environ["DISCORD_BOTKEY"]))
