from config import config
from app.src.src import pipeline_sentiment, pipeline_stats, pipeline_summarize

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
# from transformers import pipeline
# import uvicorn
import pandas as pd
import os

# sentiment_model = pipeline(model=config.sentiment_model)
# sum_model = pipeline(model=config.sum_model, use_fast=True)
headers = {"Authorization": f"Bearer {os.environ.get('API_TOKEN')}"}
SENT_API_URL = f"https://api-inference.huggingface.co/models/{config.sentiment_model}"
SUM_API_URL = f"https://api-inference.huggingface.co/models/{config.sum_model}"

app = FastAPI()

class YouTubeUrl(BaseModel):
    url_video: str

@app.get('/')
def read_root():
    return {'message': 'FastAPI+HuggingFace app sentiment + summarize YouTube comments'}

@app.post('/comments')
def get_comments(url_video: YouTubeUrl):
    data = pipeline_sentiment(url_video.url_video, os.environ.get("API_KEY"), headers, SENT_API_URL)
    data.to_csv(f"{config.DATA_FILE}", index=False)
    return data # {'message': 'Success'}

@app.get('/stats')
def get_stats_sent():
    if f"{config.NAME_DATA}" in os.listdir(f"{config.PATH_DATA}"):
        data = pd.read_csv(f"{config.DATA_FILE}")
        return pipeline_stats(data)

@app.get('/summarization')
def get_summarize():
    if f"{config.NAME_DATA}" in os.listdir(f"{config.PATH_DATA}"):
        data = pd.read_csv(f"{config.DATA_FILE}")
        return pipeline_summarize(data['text_comment'], headers, SUM_API_URL)
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)


#if __name__ == '__main__':
#    uvicorn.run(app, host='127.0.0.1', port=80)