from fastapi import FastAPI
from pydantic import BaseModel
from fetch_data import Trending

app = FastAPI()

class Item(BaseModel):
    link: str

@app.post('/')
async def get_url(video_link: Item):
    trending = Trending()
    return trending.getVideoInfo(Trending.extractVideoId(video_link.link))
    