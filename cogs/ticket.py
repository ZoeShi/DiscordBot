from discord.ext import commands
import discord
import logging

logger = logging.getLogger("discordbot.ticket")

class Ticket(commands.Cog):
    """The description for Ticket goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def enable(self, ctx):
        embed = discord.Embed(title="Title", description="Desc", color=0x00ff00)
        url_view = discord.ui.View()
        url_view.add_item(discord.ui.ChannelSelect())
        url_view.add_item(
            discord.ui.Button(label='Ticket erstellen', style=discord.ButtonStyle.url, url=ctx.message.jump_url))
        await ctx.send(embed=embed, view=url_view)

async def setup(bot):
    await bot.add_cog(Ticket(bot))
