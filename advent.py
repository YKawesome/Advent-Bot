import os
import discord
from discord import app_commands
from discord.ext import commands, tasks
import advent_resources as ar
from dotenv import load_dotenv

load_dotenv()


_SNOOP_GUILD = os.getenv('WALTER_GUILD')


class ADVENT(commands.Cog, description='Event Handlers'):
    def __init__(self, bot):
        self.bot = bot
        # self.give_solution_role.start()

    @tasks.loop(minutes=15)
    async def give_solution_role(self):
        leaderboard = ar.get_leaderboard_json(str(_SNOOP_GUILD))
        mapping = ar.get_mapping_json(_SNOOP_GUILD)
        discord_ids = ar.get_discord_ids_completed_challenge(leaderboard, mapping)
        guild = self.bot.get_guild(_SNOOP_GUILD)
        role = guild.get_role()  # TODO
        for member in guild.members:
            if member.id in discord_ids:
                await member.add_roles(role)
            else:
                await member.remove_roles(role)

    @app_commands.command(name='stats_string', description='Get stats on who has completed today\'s challenge.')
    async def stats_string(self, interaction: discord.Interaction):
        leaderboard = ar.get_leaderboard_json(str(interaction.guild.id))
        string = ar.get_stats_string(leaderboard)
        await interaction.response.send_message(string)

    @app_commands.command(name='stats_embed', description='Get stats on who has completed today\'s challenge.')
    async def stats_embed(self, interaction: discord.Interaction):
        leaderboard = ar.get_leaderboard_json(str(interaction.guild.id))
        embed = ar.get_stats_embed(leaderboard, interaction.guild)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(ADVENT(bot))
