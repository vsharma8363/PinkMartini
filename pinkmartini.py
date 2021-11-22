import discord
import os
from typing import Tuple
import requests
import json
import music_interface
import constants
import threading

client = discord.Client()

@client.event
async def on_ready():
    global music_queue
    music_queue = []
    print('Discord connection activated, login as {0.user}'.format(client))

@client.event
async def on_message(message):
    # This message came from PinkMartini.
    if message.author == client.user:
        return
    elif (message.content.startswith(constants.PLAY_CMD) or
         message.content.startswith(constants.QUEUE_CMD)):
        await play_or_queue_track(message)
    elif message.content.startswith(constants.PAUSE_CMD):
        await pause_track(message)
    elif message.content.startswith(constants.SKIP_CMD):
        await skip_track(message)
    elif message.content.startswith(constants.VOLUME_CMD):
        await set_volume(message)
    elif message.content.startswith(constants.STOP_CMD):
        await stop_and_disconnect(message)
    elif message.content.__eq__("Elizabeth Morgan Til Death"):
        await message.channel.send("YOU HAVE ACTIVATED LIZZIE BURNETT MODE")
        await playYoutubeAudio("https://www.youtube.com/watch?v=Uo2yEByF4Mw")

'''
This definition will return None if the user is connected to the voice channel,
and will connect to the voice channel if it has not already (provided the user
who sent the message is also in the voice channel).
'''
async def initiate_voice_connection(message):
    global current_volume
    global voice_channel
    global voice_client
    try:
        voice_channel
        voice_client
        if voice_channel is None or voice_client is None:
            raise NameError('Voice connection not initiated')
        elif voice_client and not voice_client.is_connected():
            raise NameError('Voice client not connected')
    except NameError:
        if not message.author.voice:
            await message.channel.send("{} is not connected to a voice channel".format(message.author.name))
            voice_channel = None
            voice_client = None
            return False
        else:
            channel = message.author.voice.channel
            voice_channel = await channel.connect()
            voice_client = message.guild.voice_client
            current_volume = 0.5
            return True
    else:
        return True

async def play_or_queue_track(message):
    global voice_channel
    global music_queue
    if await initiate_voice_connection(message):
        # User most likely want to resume content.
        if message.content.__eq__(constants.PLAY_CMD):
            if message.guild.voice_client.is_paused():
                await resume_track(message)
            else:
                await message.channel.send('Nothing was playing...')
            return
        else:
            query = (
                message.content.replace(constants.PLAY_CMD, '')
                                .replace(constants.QUEUE_CMD, ''))
            name, url = await queue_audio(query)
            # If audio is playing, add this to the queue
            if voice_client.is_playing():
                await message.channel.send(f'Queued {name} for you...')
            # If nothing is playing, start playing
            else:
                await skip_track(message)

async def set_volume(message):
    global current_volume
    global voice_channel
    target_vol = int(message.content.replace(constants.VOLUME_CMD, ''))
    if 0 <= target_vol <= 100:
        current_volume = target_vol / 100.0
        voice_channel.source.volume = current_volume
    else:
        await message.channel.send('Volume must be between 0 and 100')

async def skip_track(message):
    global music_queue
    if len(music_queue) > 0:
        await message.channel.send(f'Playing {play_audio()} now....')
    else:
        await message.channel.send('The queue is empty')

async def resume_track(message):
    global music_queue
    await message.channel.send('Resuming audio...')
    await resume_audio()

async def pause_track(message):
    await message.channel.send("Audio paused...")
    await pause_audio()

async def stop_and_disconnect(message):
    global voice_client
    global music_queue
    music_queue = []
    await message.channel.send("No more music for you...\nI cleared the music queue too")
    await stop_audio()
    await voice_client.disconnect()

# Direct player interface functions --------------------------------------------

def play_audio():
    global voice_channel
    global voice_client
    global current_volume
    global music_queue
    if voice_client.is_playing():
        voice_client.pause()
    if len(music_queue) > 0:
        name, URL = music_queue.pop(0)
        voice_channel.play(discord.FFmpegPCMAudio(URL,**music_interface.FFMPEG_OPTIONS),
                            after = lambda e: play_audio())
        voice_channel.source = discord.PCMVolumeTransformer(voice_channel.source, volume=current_volume)
        voice_client.resume()
        return name

async def queue_audio(query):
    global music_queue
    name, url = music_interface.get_video_from_query(query)
    music_queue += [(name, url)]
    return name, url

async def pause_audio():
    global voice_client
    if voice_client and voice_client.is_playing():
        voice_client.pause()

async def resume_audio():
    global voice_client
    if voice_client and voice_client.is_paused():
        voice_client.resume()

async def stop_audio():
    global voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()

client.run('SOME SUPER SECRET TOKEN')
