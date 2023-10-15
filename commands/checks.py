import json

from discord.ext import commands
from redis import StrictRedis

"""
@is_mod() is a decorator that checks if the person using the
command has the correct role relative to the guild they are in
"""
def is_mod():
    async def predicate(ctx):
        db = StrictRedis(host='db')
        guild_config = db.get(ctx.guild.id).decode('utf-8')
        mod_role_id = json.loads(guild_config)['mod_role_id']
        mod_role = ctx.guild.get_role(mod_role_id)
        return mod_role in ctx.author.roles
    return commands.check(predicate)
