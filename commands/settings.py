"""
Commands for managing the guild level config for osrs events
"""
import logging
import discord

from discord import SlashCommandGroup, ApplicationContext
from discord.ext import commands
from discord.commands import Option
from .util.config import Config

log = logging.getLogger(__name__)

"""
"[guild id ##]": {
"mod_role_id": int - role for moderator actions, people who manage events
"event_channel_id": int - channel for events, probably created by bot
}
"""


class Settings(commands.Cog):
    """
    Config class housing commands for guild level config
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config()

    config = SlashCommandGroup(
        "config",
        "Change the settings for the entire server. CAREFUL.",
        checks=[commands.has_permissions(administrator=True).predicate],
    )

    mod_role = config.create_subgroup(
        "mod_role",
        "View/Change the Moderator Role for this Discord",
        checks=[commands.has_permissions(administrator=True).predicate],
    )

    @mod_role.command(name="set")
    async def set_mod_role(
        self,
        ctx: ApplicationContext,
        role: Option(discord.Role, "role for the events moderators"),
    ):
        """
        Set the Moderator Role for this Discord. People with this role will have control of events.
        """
        try:
            guild_config = await self.config.get_config(ctx)
            if not guild_config:
                return
            guild_config["mod_role_id"] = role.id
            self.config.save_config(ctx.guild.id, guild_config)
            await ctx.respond(f"Moderator Role updated to @**{role.name}**.")
        except Exception as e:
            log.exception(f"set_mod_role,{type(e)} error occured,{e}")

    @mod_role.command(name="view")
    async def view_mod_role(self, ctx: ApplicationContext):
        """Get the Moderator Role for this Discord"""
        try:
            guild_config = await self.config.get_config(ctx)
            if not guild_config:
                return
            mod_role_id = guild_config["mod_role_id"]
            mod_role = ctx.guild.get_role(int(mod_role_id))
            await ctx.respond(f"Moderator Role is @**{mod_role.name}**.")
        except Exception as e:
            log.exception(f"view_mod_role,{type(e)} error occured,{e}")

    event_channel = config.create_subgroup(
        "event_channel",
        "View/Change the Event Forum Channel for this Discord",
        checks=[commands.has_permissions(administrator=True).predicate],
    )

    @event_channel.command(name="set")
    async def set_event_channel(
        self,
        ctx: ApplicationContext,
        chan: Option(discord.ForumChannel, "forum channel for events"),
    ):
        """
        Set the Event Forum Channel for this Discord.
        """
        try:
            guild_config = await self.config.get_config(ctx)
            if not guild_config:
                return
            guild_config["event_channel_id"] = chan.id
            self.config.save_config(ctx.guild.id, guild_config)
            await ctx.respond(f"Event Forum Channel updated to {chan.mention}.")
        except Exception as e:
            log.exception(f"set_event_channel,{type(e)} error occured,{e}")

    @event_channel.command(name="view")
    async def view_event_channel(self, ctx: ApplicationContext):
        """Get the Moderator Role for this Discord"""
        try:
            guild_config = await self.config.get_config(ctx)
            if not guild_config:
                return
            event_chan_id = guild_config["event_channel_id"]
            chan = ctx.guild.get_channel(int(event_chan_id))
            await ctx.respond(f"Event Forum Channel is {chan.mention}.")
        except Exception as e:
            log.exception(f"view_event_channel,{type(e)} error occured,{e}")


def setup(bot):
    """pycord setup function"""
    bot.add_cog(Settings(bot))
