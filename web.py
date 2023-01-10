from lona.html import HTML, Button, Div, H1, Select
from lona import LonaApp, LonaView
from lona_bootstrap_5 import PrimaryButton, TextInput
import discord
import config


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


app = LonaApp(__file__)

async def start_discord():
    await client.start(config.token)

@app.middleware
class MyMiddleware:
    async def on_startup(self, data):
        server = data.server
        print("test")
        data.server.loop.create_task(start_discord())
        print("test")
        return data

@app.route('/')
class MyView(LonaView):
    def handle_button_click(self, input_event):
        self.message.set_text('Button clicked')
        #hier was der Button machen soll


    def get_channels(self):
        return [
            # value, label, is_selected
            ('rip', 'rip', True),
            ('bar', 'Bar', False),
        ]

    def get_channels_discord(self):
        self.server.run_coroutine_sync(client.wait_until_ready(), wait=True)
        guild = client.guilds[0]
        category = guild.get_channel(962281157251170321)
        # await interaction.response.send_message('This is green.', ephemeral=True)
        channel_items = []
        for channel in guild.channels:
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
