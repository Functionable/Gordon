import disnake
import asyncio
import gordon.core_bot as core
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
    'options': '-vn'
}

yt_dl = yt_dlp.YoutubeDL(ytdl_format_options)

# assuming it's a url that works with yt-dlp.
# will have to add checks later
async def create_url_audio_stream(url):
    extracted_data = await asyncio.coroutine(yt_dl.extract_info)(url, download=False)
    selected_entry = extracted_data if 'entries' not in extracted_data else extracted_data['entries'][0]

    remote_filename = selected_entry.get('url')
    
    return (remote_filename, disnake.FFmpegPCMAudio(remote_filename, **ffmpeg_options))

async def bot_join_channel(channel):
    for client in core.bot_instance.voice_clients:
        if client.channel == channel: return client

    return await channel.connect()

@core.bot_instance.slash_command()
async def join_channel(intr):
    voice = intr.author.voice.channel
    vclient = await bot_join_channel(intr.author.voice.channel)
    await intr.response.send_message(f"Joined '{voice.name}' as per {intr.author.mention}'s request!")
    
@core.bot_instance.slash_command()
async def play_song(intr, url: str):
    voice = intr.author.voice.channel
    stream = await bot_join_channel(voice)
    audio_results = await create_url_audio_stream(url)

    stream.play(audio_results[1])
    await intr.response.send_message(f"Playing song '{url}'")

@core.bot_instance.slash_command()
async def exit_channel(intr):
    voice_client = intr.guild.voice_client
    song_channel = voice_client.channel
    await voice_client.disconnect()
    await intr.response.send_message(f"Exitted '{song_channel.name}' as per {intr.author.mention}'s request!")
