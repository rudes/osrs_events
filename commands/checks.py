"""
helper functions for checking the user of the command can execute it
"""
import json

from discord.ext import commands
from redis import StrictRedis


def is_mod():
    """
    decorator that checks if the person using the
    command has the correct role relative to the guild they are in
    """

    async def predicate(ctx):
        db = StrictRedis(host="db")
        guild_config = db.get(str(ctx.guild.id)).decode("utf-8")
        mod_role_id = json.loads(guild_config)["mod_role_id"]
        mod_role = ctx.guild.get_role(mod_role_id)
        return mod_role in ctx.author.roles

    return commands.check(predicate)
