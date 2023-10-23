"""class for managing the Config"""
import logging
import json
import redis

log = logging.getLogger(__name__)


class Config:
    """class for managing the Config"""

    def __init__(self):
        self.db = redis.StrictRedis(host="db")

    def save_config(self, guild_id, guild_config):
        """save the config to the db"""
        config_json = json.dumps(guild_config)
        self.db.set(str(guild_id), config_json)

    async def setup_server(self, ctx):
        """prepare the discord for events"""
        # ask for approval
        # create mod role
        # create event category and event channels
        guild_config = {
            "mod_role_id": 1159942632605237298,
            "event_channel_id": 1159949415335854160,
        }
        self.save_config(str(ctx.guild.id), guild_config)

    async def get_config(self, ctx):
        """get the config from the db"""
        raw = self.db.get(str(ctx.guild.id))
        if not raw:
            return await self.setup_server(ctx)
        return json.loads(raw.decode("utf-8"))
