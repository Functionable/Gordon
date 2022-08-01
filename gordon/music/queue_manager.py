import gordon.core_bot as core
from typing import List
import time
music_queues = {}

# there needs to be a mechanism to dispose of 'dead' music queues.

class MusicQueue(object):
    def __init__(self, voice_client):
        self.voice_client = voice_client
        self.delete_time = 0
        self.valid = True
        self.head = 0
        self.songs = []

    def mark_for_deletion(self):
        self.valid = False
        self.delete_time = time.time() + 120

    def is_playing(self):
        return self.voice_client.is_playing()

    def next_song_exists(self):
        return self.head < len(self.songs)

    def get_current_index(self):
        return self.head

    def get_songs(self):
        return self.songs

    def is_dead(self):
        return self.valid

    def revive(self):
        self.valid = True

    def queue_song(self, song):
        self.songs.append(song)

    def stop_playing(self):
        self.voice_client.stop()

    def play_next(self):
        if self.next_song_exists():
            self.head += 1
            self.start_playing()

    def start_playing(self):
        print(f"playing song {self.head}, playing={self.is_playing()}")
        if self.is_playing(): return

        self.voice_client.play(
            self.songs[self.head][1],
            
            # runs after the audio has finished.
            after=lambda x: self.play_next()
        )

    def skip_current(self):
        if self.is_playing():
            self.stop_playing()
            self.play_next()
        else:
            self.head += 1

    def is_client_connected(self):
        return self.voice_client.is_connected()

async def get_all_queues() -> List[MusicQueue]:
    return music_queues

async def make_queue(voice_client) -> MusicQueue:
    new_queue = MusicQueue(voice_client)
    music_queues[voice_client.guild.id] = new_queue
    return new_queue

async def make_or_get_queue(voice_client) -> MusicQueue:
    retrieved_queue = await get_queue(voice_client.guild.id)
    if not retrieved_queue:
        return await make_queue(voice_client)
    return retrieved_queue

async def get_queue(guild_id) -> MusicQueue:
    return None if guild_id not in music_queues else music_queues[guild_id]