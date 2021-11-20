import discord
import os
import requests
import json
import music_utils
import constants

client = discord.Client()
audio_paused = True
queue = []
current_song = ''

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # This message came from PinkMartini.
    if message.author == client.user:
        return
    # A command was sent to PinkMartini.
    elif message.content.startswith(constants.PREFIX):
        elif message.content.startswith(constants.PLAY_CMD):
            await play(message)
        elif message.content.startswith(constants.PAUSE_CMD):
            await pause(message)

async def join_if_not_joined(message):
    global voice_channel
    try:
        voice_channel
    except NameError:
        if not message.author.voice:
            await message.channel.send("{} is not connected to a voice channel".format(message.author.name))
            return
        else:
            channel = message.author.voice.channel
            voice_channel = await channel.connect()
    else:
        return

async def resume_playback(message):
    voice_client = message.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()
    else:
        await message.channel.send("Nothing was playing")

async def playGenericAudio(URL):
    global voice_channel
    voice_channel.play(discord.FFmpegPCMAudio(URL,**music_utils.FFMPEG_OPTIONS))

async def playYoutubeAudio(youtubeURL):
    global voice_channel
    voice_channel.play(
        discord.FFmpegPCMAudio(
            music_utils.youtubeUrlProcessor(youtubeURL),
        **music_utils.FFMPEG_OPTIONS)
    )

async def query(message):
    return


async def pause(message):
    await message.channel.send("Audio paused...")
    voice_client = message.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()


async def play(message):
    await join_if_not_joined(message)
    if message.content.__eq__(constants.PLAY_CMD): # User wants to resume
        await resume_playback(message)
        return
    user_query = message.content[len(constants.PLAY_CMD) + 1:]
    # If user is not in chat, don't do anything
    if not message.author.voice:
        return
    elif user_query.startswith('https://www.youtube.com'):
        await message.channel.send('Playing Youtube Audio...')
        await playYoutubeAudio(user_query)
    elif user_query.startswith('https://'):
        await message.channel.send('Playing Audio From the Internet...')
        await playGenericAudio(user_query)
    else:
        await message.channel.send('I don\'t think that was a URL, but I\'ll see if I can find that for you')
        await query(user_query)

async def leave(message):
    voice_client = message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await message.channel.send("The bot is not connected to a voice channel.")




client.run('API TOKEN HERE')

ytdl_format_options = {
    'format': 'bestaudio/best',
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
