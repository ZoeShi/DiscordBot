from discord import app_commands, Object
from discord.ext import commands
import discord
import wikipedia
import logging

logger = logging.getLogger("discordbot.search")

class Wikipedia(commands.Cog):
    """The description for Wikipedia goes here."""

    def __init__(self, bot):
        self.bot = bot

    def format_output(self, result):
        if len(result) > 2000:
            return result[:1990] + " ..."
        else:
            return result

    def run_search(self, search_string: str):
        try:
            result = wikipedia.summary(search_string)
        except wikipedia.DisambiguationError:
            result = wikipedia.search(search_string)
        return result

    @commands.command()
    async def sync(self, ctx):
        await self.tree.sync(guild=Object(id=962281156563320832))
        logger.debug("sync")

    @app_commands.command(name="search", description="search things in wikipedia")
    async def search(self, interaction: discord.Interaction, search_string: str):
        wikipedia.set_lang("de")
        try:
            result = self.run_search(search_string)
        except Exception as e:
            logger.error(e)
            await interaction.response.send_message(e)
            return
        logger.info("result: %s", result)
        formatted_result = self.format_output(result)
        await interaction.response.send_message(formatted_result)


async def setup(bot):
    await bot.add_cog(Wikipedia(bot))
