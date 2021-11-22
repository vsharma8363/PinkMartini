from typing import Tuple
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
    'source_address': '0.0.0.0'
}

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

'''
Converts a user query (Either a URL or search term, to a URL that can be played).
Returns [name, URL].
'''
def get_video_from_query(user_query) -> Tuple[str, str]:
    if user_query.startswith('https://'): # URL was provided
        if user_query.startswith('https://www.youtube.com'):
            return get_yt_video_from_url(user_query)
        else:
            return 'something from the internet', user_query
    # The user did not provide a URL, so just try to find the video on Youtube.
    else:
        return get_yt_video_from_search(user_query)

'''
Get a Youtube video name and URL from an original Youtube URL.
'''
def get_yt_video_from_url(originalYoutubeURL: str) -> Tuple[str, str]:
    with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
        info = ydl.extract_info(originalYoutubeURL, download=False)
        return info['title'], info['formats'][0]['url']

'''
Get a Youtube video from a search query.
'''
def get_yt_video_from_search(query: str) -> Tuple[str, str]:
    output = dict()
    with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
        result = ydl.extract_info(f"ytsearch1:{query}", download=False)['entries'][0]
        return result['title'], result['url']
