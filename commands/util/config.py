"""class for managing the Config"""
import logging
import json
import redis

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
        # if "COMMUNITY" in ctx.guild.features:
        # ask for approval
        # create mod role
        # create event category and event channels
        guild_config = {
            "mod_role_id": 1159942632605237298,
            "event_channel_id": 1159949415335854160,
        }
        self.db.set(str(ctx.guild.id), json.dumps(guild_config))
        await ctx.respond("Config created.")
