from discord.ext import commands
import discord
import logging

logger = logging.getLogger("discordbot.ticket")


class CreateTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="neues Ticket", style=discord.ButtonStyle.green, custom_id='my_view:green')
    async def create_ticket_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        category = guild.get_channel(962281157251170321)
        #await interaction.response.send_message('This is green.', ephemeral=True)
        for channel in guild.channels:
            logger.debug(channel)
        await category.create_text_channel('test_channel')
        await interaction.response.send_message('wuff.', ephemeral=True)


class EnableTicketModal(discord.ui.Modal, title='Ticket Aktivierung'):
    name = discord.ui.TextInput(
        label='Titel für das Ticket',
        placeholder='Wähle den Titel für das Ticket..'
    )

    channel = discord.ui.ChannelSelect(channel_types=[discord.ChannelType.text])

    #@discord.ui.select(cls=discord.ui.ChannelSelect, channel_types=[discord.ChannelType.text])
    #async def select_create_ticket_channel(self, interaction: discord.Interaction, select: discord.ui.ChannelSelect):
    #    await interaction.response.send("success")


class EnableTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        #self.add_item(discord.ui.TextInput(label="Wähle den Titel für das Ticket.", default="Klicke den Button um ein Ticket anzulegen. "))

    @discord.ui.button(label="einrichten", style=discord.ButtonStyle.green, custom_id='my_view:green')
    async def show_ticket_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EnableTicketModal())



class Ticket(commands.Cog):
    """The description for Ticket goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def enable(self, ctx):
        embed = discord.Embed(title="Ticket Channel", description="Den Button klicken, um den Ticketbot einzurichten.", color=0x00ff00)
        """url_view = discord.ui.View()
        url_view.add_item(discord.ui.ChannelSelect())
        url_view.add_item(
            discord.ui.Button(label='Ticket erstellen', style=discord.ButtonStyle.url, url=ctx.message.jump_url))"""
        await ctx.send(embed=embed, view=EnableTicketView())



async def setup(bot):
    await bot.add_cog(Ticket(bot))
