from lona.html import HTML, Button, Div, H1, Select
from lona import LonaApp, LonaView
from lona_bootstrap_5 import PrimaryButton, TextInput
import discord
import config
import toml

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

app = LonaApp(__file__)

@client.event
async def on_ready():
    config1 = toml.load("config.toml")
    channel_id = config1["channel"]
    print(channel_id)
    channel = client.get_channel(channel_id)
    print(channel)
    client.add_view(CreateTicketView(channel, client.loop))

async def start_discord():
    await client.start(config.token)



@app.middleware
class MyMiddleware:
    async def on_startup(self, data):
        server = data.server
        data.server.loop.create_task(start_discord())
        return data

class CreateTicketView(discord.ui.View):
    def __init__(self, channel, loop):
        try:
            super().__init__(timeout=None)
        except:
            pass
        self._View__stopped = loop.create_future()
        self.discord_channel = channel

    @discord.ui.button(label="neues Ticket", style=discord.ButtonStyle.green, custom_id='my_view:green')
    async def create_ticket_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        category = self.discord_channel.category
        await category.create_text_channel('test_channel')
        await interaction.response.send_message('TicketBot erfogreich erstellt', ephemeral=True)


@app.route('/')
class MyView(LonaView):
    def handle_button_click(self, input_event):

        selected_message = self.create_message_input.value
        selected_channel = self.channel.value
        channel_id = int(selected_channel)
        config1 = toml.load("config.toml")
        config1["channel"] = channel_id
        with open("config.toml", "w") as config_file:
            toml.dump(config1, config_file)
        discord_channel = self.guild.get_channel(channel_id)
        ticket_view = CreateTicketView(discord_channel, self.server.loop)
        self.server.run_coroutine_sync(discord_channel.send(selected_message, view=ticket_view))

    def get_channels_discord(self):
        self.server.run_coroutine_sync(client.wait_until_ready(), wait=True)
        self.guild = client.guilds[0]
        # category = self.guild.get_channel(962281157251170321)
        # await interaction.response.send_message('This is green.', ephemeral=True)
        channel_items = []
        for channel in self.guild.channels:
            channel_items.append((channel.id, channel.name, False))
        return channel_items

    def handle_request(self, request):
        self.title_select_text = Div("Nachricht die dem User im Ticketchannel angezeigt wird.")
        self.create_message_input = TextInput(_style={'width': '100em'})
        self.title_select_channel = Div("Wähle den Raum aus, wo der Ticketbot hin soll")
        self.channel = Select(
            values=self.get_channels_discord(),
            _class="form-control"
        )

        html = HTML(
            H1('einrichten'),
            self.title_select_text,
            self.create_message_input,
            self.title_select_channel,
            self.channel,
            PrimaryButton('einrichten', handle_click=self.handle_button_click),
        )

        return html

    app.add_template('lona/frontend.js', """
        lona_context.add_disconnect_hook(function(lona_context, event) {
            document.querySelector('#lona').innerHTML = `
                Server disconnected <br> Trying to reconnect...
            `;

            setTimeout(function() {
                lona_context.reconnect();

            }, 1000);
        });
    """)


app.run(port=8080)
