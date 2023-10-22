"""
bot entrypoint that loads all cogs and starts bot
"""
import os
import logging
import discord

from discord.ext import commands
from commands import config
from handlers import ready

logging.basicConfig(
    format="%(asctime)s %(name)s:%(levelname)-8s %(message)s",
    filename="/var/log/osrs_events.log",
    level=logging.INFO,
)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
discord_log = logging.getLogger("discord")
discord_log.setLevel(logging.ERROR)


def main():
    """main entrypoint"""
    bot = commands.Bot(
        command_prefix="!",
        debug_guilds=[1159942455752409118],
        intents=discord.Intents.all(),
    )

    # commands
    bot.add_cog(config.Config(bot))

    # handlers
    bot.add_cog(ready.Ready(bot))

    bot.run(str(os.environ["DISCORD_BOTKEY"]))


if __name__ == "__main__":
    main()
