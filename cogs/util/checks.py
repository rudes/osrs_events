"""
helper functions for checking the user of the command can execute it
"""
from discord.ext import commands
from config import Config


def is_mod():
    """
    decorator that checks if the person using the
    command has the correct role relative to the guild they are in
    """

    async def predicate(ctx):
        config = Config()
        mod_role_id = config.get(ctx.guild.id, "mod_role_id")
        mod_role = ctx.guild.get_role(mod_role_id)
        return mod_role in ctx.author.roles

    return commands.check(predicate)
