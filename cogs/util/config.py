"""class for managing the Config"""
import logging
import json
import redis
import discord

from discord import PermissionOverwrite
from discord.channel import ForumTag

log = logging.getLogger(__name__)

class SetupApproval(discord.ui.Modal):
    """ Popup modal asking for approval """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            discord.ui.InputText(
                label="Confirm?",
                placeholder="Yes",
            ),
            *args,
            **kwargs,
        )

    async def callback(self, ctx: discord.Interaction):
        """ Popup modal asking for approval """

        response = self.children[0].value.lower()
        if not response.startswith('y'):
            await ctx.response.send_message("Config not created.")
            return

        if "COMMUNITY" not in ctx.guild.features:
            await ctx.respond("Convert your discord to a Community")
            return

        event_cat = await ctx.guild.create_category("EVENTS")

        mod_role = None
        for role in await ctx.guild.fetch_roles():
            if role.name == "Event Moderator":
                mod_role = role
        if not mod_role:
            mod_role = await ctx.guild.create_role("Event Moderator", mentionable=True)

        mod_overwrites = {
            ctx.guild.default_role: PermissionOverwrite(read_messages=False),
            mod_role: PermissionOverwrite(read_messages=True),
        }
        mod_channel = await event_cat.create_text_channel(
            "mods", overwrites=mod_overwrites
        )

        forum_overwrites = {
            ctx.guild.default_role: PermissionOverwrite(send_messages=False),
        }
        event_channel = await event_cat.create_forum_channel(
            "events", overwrites=forum_overwrites
        )
        tags = [
            ForumTag(name="Event", emoji="🎟️"),
            ForumTag(name="Bingo", emoji="🎯"),
            ForumTag(name="TileRace", emoji="🎲"),
        ]
        await event_channel.edit(available_tags=tags)
        await mod_channel.edit(position=0)

        guild_config = {
            "mod_role_id": mod_role.id,
            "mod_channel_id": mod_channel.id,
            "event_channel_id": event_channel.id,
        }
        db = redis.StrictRedis(host="db")
        db.set(str(ctx.guild.id), json.dumps(guild_config))
        await ctx.response.send_message("Config created.")


class Config:
    """class for managing the Config"""

    def __init__(self):
        self.db = redis.StrictRedis(host="db")

    def get(self, guild_id, setting):
        """get a specific value from the config"""
        raw = self.db.get(str(guild_id))
        config_json = json.loads(raw.decode("utf-8"))
        return config_json[setting]

    def set(self, guild_id, setting, value):
        """set a specific value to the config"""
        raw = self.db.get(str(guild_id))
        config_json = json.loads(raw.decode("utf-8"))
        config_json[setting] = value
        config_string = json.dumps(config_json)
        self.db.set(str(guild_id), config_string)

    async def setup_config(self, ctx):
        """prepare the discord for events"""
        modal = SetupApproval(title="Create Events category and needed channels?")
        await ctx.send_modal(modal)

    async def setup_request(self, guild):
        """let people know to setup the bot"""
        chan = None
        for c in guild.text_channels:
            if c.permissions_for(guild.me).send_messages:
                chan = c
        if not chan:
            return
        message = (
            "Thank you for adding OSRS Events.\n"
            "To setup have someone with admin rights use `/config setup`."
        )
        async for m in chan.history(limit=100):
            if message == m.content:
                return
        await chan.send(message)
