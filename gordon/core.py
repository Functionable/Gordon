import disnake
from disnake.ext import commands

def retrieve_token():
    global bot_token
    try:
        with open('./bot-token', 'r') as token_file:
            bot_token = token_file.read().strip()

        return not bot_token
    except OSError:
        return False

bot_intents = disnake.Intents(messages=True,members=True,guilds=True)
bot_instance = commands.Bot(
    command_prefix='$',
    sync_commands=True,
    sync_commands_debug=True,
    intents=bot_intents
)

@bot_instance.slash_command()
async def helloworld(inter):
    await inter.response.send_message(f"Hello, World!")

def start_bot():
    if retrieve_token():
        print("Token file empty or not found, aborting start process.")
        print("In order to function, this bot requires a bot dev token at ./bot-token")
        return

    global bot_instance

    bot_instance.run(bot_token)