""" simple listener for on_ready event """
import logging
import discord

from discord.ext import commands

log = logging.getLogger(__name__)


class Ready(commands.Cog):
    """simple listener for on_ready event"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """simple listener for on_ready event"""
        try:
            await self.bot.change_presence(activity=discord.Game(name="/help"))
            log.info("on_ready,presence state set")
        except Exception as e:
            log.exception(f"on_ready,{type(e)} error occured,{e}")


def setup(bot):
    bot.add_cog(Ready(bot))
