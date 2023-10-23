"""class for managing the Config"""
import logging
import json
import redis

from discord import PermissionOverwrite
from discord.channel import ForumTag

log = logging.getLogger(__name__)


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
        # ask for approval
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
        self.db.set(str(ctx.guild.id), json.dumps(guild_config))
        await ctx.respond("Config created.")
