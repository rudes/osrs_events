"""join threads when they are created"""
import logging

from discord.ext import commands

log = logging.getLogger(__name__)


class Threads(commands.Cog):
    """join threads when they are created"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        """join threads when they are created"""
        try:
            await thread.join()
        except Exception as e:
            log.exception(f"on_thread_create,{type(e)} error occured,{e}")


def setup(bot):
    """pycord entrypoint"""
    bot.add_cog(Threads(bot))
