from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
import io
import pytube as pt
from pytube.exceptions import *

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
    except AgeRestrictedError:
        raise HTTPException(status_code=400, detail="Video is age restricted, and cannot be accessed without OAuth.")
    except ExtractError:
        raise HTTPException(status_code=400, detail="Couldn't extract data from URL")
    except HTMLParseError:
        raise HTTPException(status_code=400, detail="HTML could not be parsed")
    except LiveStreamError:
        raise HTTPException(status_code=400, detail="Video is a live stream")
    except MaxRetriesExceeded:
        raise HTTPException(status_code=400, detail="Maximum number of retries exceeded")
    except MembersOnly:
        raise HTTPException(status_code=400, detail="Video is members-only")
    except RegexMatchError:
        raise HTTPException(status_code=400, detail="Regex pattern did not return any matches")
    except VideoPrivate:
        raise HTTPException(status_code=400, detail="Video is private")
    except VideoRegionBlocked:
        raise HTTPException(status_code=400, detail="Video is region blocked")
    except VideoUnavailable:
        raise HTTPException(status_code=400, detail="Video is unavailable")
        


@app.get("/playlist-urls")
async def get_songs(url:str):
    try:
        p = pt.Playlist(url)
        return p.video_urls
    except:
        raise HTTPException(status_code=400, detail="Invalid playlist url")
