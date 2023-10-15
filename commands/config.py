import logging
import redis
from dataclasses import dataclass
from checks import is_mod
from discord import SlashCommandGroup, Option, ApplicationContext
from discord.ext import commands
from discord.commands import slash_command

log = logging.getLogger(__name__)

"""
"[guild id ##]": {
"mod_role_id": int - role for moderator actions, people who manage events
"event_channel_id": int - channel for events, probably created by bot
}
"""

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = redis.StrictRedis(host='db')

    config = SlashCommandGroup(
        'config',
        'Change the settings for the entire server. CAREFUL.',
        checks=[is_mod()]
    )

    async def setup_server(self, ctx: ApplicationContext):
        # ask for approval
        # create mod role
        # create event category and event channels
        guild_config = {
            'mod_role_id': 0,
            'event_channel_id': 0,
        }
        self.db.set(str(ctx.guild.id), guild_config)

    async def get_config(self, ctx: ApplicationContext):
        raw = self.db.get(str(ctx.guild.id))
        if not raw:
            return await self.setup_server(ctx)
        return json.loads(raw.decode('utf-8'))

    @config.command()
    async def set_mod_role(self,
        ctx: ApplicationContext,
        id: Option(int, 'role id for the games moderators')
    ):
        """
        Set the mod_role_id for this guild.
        People with this role will have control of events.
        """
        try:
            guild_config = await self.get_config(ctx)
            if not guild_config:
                return
            guild_config['mod_role_id'] = id
            self.save_config(ctx.guild.id, guild_config)
            await ctx.reply(f"mod_role updated to {id}.")
        except Exception as e:
            log.exception(f"mod_role,{type(e)} error occured,{e}")

    @config.command()
    async def get_mod_role(self, ctx: ApplicationContext):
        """
        Get the mod_role_id for this guild.
        """
        try:
            guild_config = await self.get_config(ctx)
            if not guild_config:
                return
            id = guild_config['mod_role_id']
            await ctx.reply(f"mod_role id is {id}.")
        except Exception as e:
            log.exception(f"mod_role,{type(e)} error occured,{e}")
