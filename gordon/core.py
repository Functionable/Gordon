import disnake
import asyncio
import gordon.core_bot
import gordon.command_modules

def retrieve_token():
    global bot_token
    try:
        with open('./bot-token', 'r') as token_file:
            bot_token = token_file.read().strip()

        return not bot_token
    except OSError:
        return False

def start_bot():
    if retrieve_token():
        print("Token file empty or not found, aborting start process.")
        print("In order to function, this bot requires a bot dev token at ./bot-token")
        return

    global bot_instance

    gordon.core_bot.bot_instance.run(bot_token)