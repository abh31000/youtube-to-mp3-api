from fastapi import FastAPI
from fastapi.responses import Response
import io
import pytube as pt

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Nothing to see here"}

@app.get("/converter",
    responses={
        200: {
            "content": {"audio/mpeg": {}}
        }
    },
    response_class=Response
)
async def get_song(url:str):
    try:
        yt = pt.YouTube(url)
        song = yt.streams.filter(only_audio=True).first()
        buffer = io.BytesIO()
        song.stream_to_buffer(buffer)

        return Response(content=buffer.getvalue(), media_type="audio/mpeg")
    except:
        return "Invalid url"


@app.get("/playlist-urls")
async def get_songs(url:str):
    try:
        p = pt.Playlist(url)
        return p.video_urls
    except:
        return "Invalid playlist url"
