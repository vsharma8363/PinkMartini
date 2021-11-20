import youtube_dl

YDL_OPTS = {'format': 'bestaudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

def youtubeUrlProcessor(originalYoutubeURL: str) -> str:
    with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
        info = ydl.extract_info(originalYoutubeURL, download=False)
        return info['formats'][0]['url']
