import discord
import os
import requests
import json
import music_utils
import constants

client = discord.Client()

@client.event
async def on_ready():
    global queried_videos
    print('We have logged in as {0.user}'.format(client))
    queried_videos = None

@client.event
async def on_message(message):
    # This message came from PinkMartini.
    if message.author == client.user:
        return
    elif message.content.startswith(constants.PREFIX):
        if message.content.startswith(constants.PLAY_CMD):
            await play(message)
        elif message.content.startswith(constants.PAUSE_CMD):
            await pause(message)
        elif message.content.startswith(constants.STOP_CMD):
            await stop(message)
        elif message.content.startswith(constants.LEAVE_CMD):
            await leave(message)
        else:
            await message.channel.send("That wasn't a valid command")

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

async def play(message):
    # Join the voice channel if the bot is not already there.
    await join_if_not_joined(message)
    # If music is playing right now, stop it.
    if message.guild.voice_client.is_playing():
        message.guild.voice_client.stop()
    # The player most likely wants to resume.
    if message.content.__eq__(constants.PLAY_CMD) and message.guild.voice_client.is_paused():
        await resume(message)
        return
    # The player is not in the voice chat
    elif not message.author.voice:
        return
    else:
        user_query = message.content[len(constants.PLAY_CMD) + 1:]
        # The user provided a Youtube URL.
        if user_query.startswith('https://www.youtube.com'):
            await message.channel.send('Playing Youtube Audio...')
            await playYoutubeAudio(user_query)
        # The user provided a non-Youtube URL.
        elif user_query.startswith('https://'):
            await message.channel.send('Playing Audio From the Internet...')
            await playGenericAudio(user_query)
        # The user did not provide a URL, so just try to find the video on Youtube.
        else:
            videoURL, videoName = music_utils.getYoutubeVideoSearch(user_query)
            await message.channel.send(f'I found \'{videoName}\' on Youtube. I\'ll play it now')
            await playYoutubeAudio(videoURL)

async def resume(message):
    voice_client = message.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()
        await message.channel.send("Resuming audio playback")
    elif voice_client.is_playing():
        await message.channel.send("Music is playing right now, can't you hear it?")
    else:
        await message.channel.send("Nothing was playing")

async def pause(message):
    await message.channel.send("Audio paused...")
    voice_client = message.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()

async def stop(message):
    await message.channel.send("No more music for you...")
    voice_client = message.guild.voice_client
    voice_client.stop()

async def leave(message):
    voice_client = message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await message.channel.send("The bot is not connected to a voice channel.")

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

client.run('SUPER SECRET TOKEN GOES HERE')
