from typing import Dict
import youtube_dl

YDL_OPTS = {
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
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

def youtubeUrlProcessor(originalYoutubeURL: str) -> str:
    with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
        info = ydl.extract_info(originalYoutubeURL, download=False)
        return info['formats'][0]['url']

def getYoutubeVideoSearch(query: str) -> str:
    output = dict()
    with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
        result = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        return result['url'], result['title']
