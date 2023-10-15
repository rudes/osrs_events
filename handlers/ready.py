import logging
import discord

from discord.ext import commands

log = logging.getLogger(__name__)

class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            await self.bot.change_presence(activity=discord.Game(name="/help"))
            log.info('on_ready,presence state set')
        except Exception as e:
            log.error('on_ready,{0} error occured,{1}'.format(type(e), e))
