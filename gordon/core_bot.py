import disnake
import disnake.ext.commands

bot_intents = disnake.Intents(messages=True,members=True,guilds=True, voice_states=True)
bot_instance = disnake.ext.commands.Bot(
    command_prefix='$',
    sync_commands=True,
    #sync_commands_debug=True,
    intents=bot_intents
)