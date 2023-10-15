import os
import discord
import logging

from commands import *
from handlers import *
from discord.ext import commands

logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)-8s %(message)s",
                    filename="/var/log/osrs_games.log", level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
discord_log = logging.getLogger('discord')
discord_log.setLevel(logging.ERROR)

def main():
    bot = commands.Bot(
        command_prefix='!',
        debug_guilds=[1159942455752409118],
        intents=discord.Intents.all()
    )

    # commands
    bot.add_cog(config.Config(bot))

    # handlers
    bot.add_cog(ready.Ready(bot))

    bot.run(str(os.environ['DISCORD_BOTKEY']))

if __name__ == "__main__":
    main()
