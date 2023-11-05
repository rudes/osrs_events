"""Handle joining a new guild or thread"""
import logging

from discord.ext import commands
from .util.config import Config

log = logging.getLogger(__name__)


class JoinGuild(commands.Cog):
    """Handle joining a new guild or thread"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """let people know how to setup the bot"""
        try:
            await self.config.setup_request(guild)
        except Exception as e:
            log.exception(f"on_guild_join,{type(e)} error occured,{e}")

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        """join threads when they are created"""
        try:
            await thread.join()
        except Exception as e:
            log.error(f"on_thread_create,{type(e)} error occured,{e}")


def setup(bot):
    """load extension"""
    bot.add_cog(JoinGuild(bot))
