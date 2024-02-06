import config
from src import pipeline_sentiment

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import uvicorn

sentiment_model = pipeline(config.sentiment_model)
app = FastAPI()

class YouTubeUrl(BaseModel):
    url_video: str

@app.get('/')
def read_root():
    return {'message': 'FastAPI+HuggingFace app sentiment + summarize YouTube comments'}

@app.post('/comments')
def get_comments(url_video: YouTubeUrl):
    data = pipeline_sentiment(url_video.url_video, config.API_KEY, sentiment_model)
    data.to_csv(f"{config.DATA_FILE}", index=False)
    return {'message': 'Success'}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=80)