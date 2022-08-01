import gordon.core_bot as core
import gordon.music.queue_manager as queue_manager
import disnake
import asyncio
import yt_dlp

ytdl_format_options = {
    'format': 'm4a/bestaudio/best',
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }],
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
    
}

ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

yt_dl = yt_dlp.YoutubeDL(ytdl_format_options)

async def valid_url(url):
    return True

async def search_url_youtube(url):
    pass

# assuming it's a url that works with yt-dlp.
# will have to add checks later
async def create_url_audio_stream(url):
    extracted_data = await asyncio.coroutine(yt_dl.extract_info)(url, download=False)
    selected_entry = extracted_data if 'entries' not in extracted_data else extracted_data['entries'][0]

    remote_filename = selected_entry.get('url')

    
    return (remote_filename, disnake.FFmpegPCMAudio(remote_filename, **ffmpeg_options), url, selected_entry.get('title'))

async def bot_join_channel(channel):
    for client in core.bot_instance.voice_clients:
        if client.channel == channel: return client

    voice_client = await channel.connect()
    
    return voice_client

@core.bot_instance.slash_command()
async def join_channel(intr):
    voice = intr.author.voice.channel
    vclient = await bot_join_channel(intr.author.voice.channel)
    await intr.response.send_message(f"Joined '{voice.name}' as per {intr.author.mention}'s request!")
    
async def bot_in_channel(channel):
    if channel == None: return False

    for client in core.bot_instance.voice_clients:
        if client.channel == channel: return True
    
    return False

@core.bot_instance.slash_command()
async def view_queue(intr):
    if await bot_in_channel(intr.author.voice.channel):
        bot_queue = await queue_manager.get_queue(intr.guild.id)
        if not bot_queue: 
            await intr.response.send_message("No queue available!")
            return

        queue_text = ""
        for index, song in enumerate(bot_queue.get_songs()):
            current_text = " *(current)*" if index == bot_queue.get_current_index() else ""
            queue_text += f"**Track #{index+1}**{current_text}: *{song[3]}* @ {song[2]}"
            if index + 1 != len(bot_queue.get_songs()):
                queue_text += "\n"

        new_embed = disnake.Embed(description = queue_text, title="Your channel's queue")

        await intr.response.send_message(embed=new_embed)
    else:
        await intr.response.send_message("You must be in the same voice channel as me in order to do that!")

@core.bot_instance.slash_command()
async def skip_song(intr):
    if await bot_in_channel(intr.author.voice.channel):
        bot_queue = await queue_manager.get_queue(intr.guild.id)    
        bot_queue.skip_current()
        await intr.response.send_message("Current song has been skipped.")
    else:
        await intr.response.send_message("You must be in the same voice channel as me in order to do that!")

@core.bot_instance.slash_command()
async def play_song(intr, url: str):
    voice = intr.author.voice.channel
    await intr.response.send_message(f"Playing song '{url}'")
    stream = await bot_join_channel(voice)
    audio_results = await create_url_audio_stream(url)
    queue = await queue_manager.make_or_get_queue(stream)

    #stream.play(audio_results[1])
    queue.queue_song(audio_results)
    queue.start_playing()

@core.bot_instance.slash_command()
async def exit_channel(intr):
    voice_client = intr.guild.voice_client
    song_channel = voice_client.channel
    await voice_client.disconnect()
    await intr.response.send_message(f"Exitted '{song_channel.name}' as per {intr.author.mention}'s request!")
