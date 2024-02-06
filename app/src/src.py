import pandas as pd
import requests
import urllib.parse as urlparse


def get_video_id(url_video):
    """Get video id"""
    query = urlparse.urlparse(url_video)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            return urlparse.parse_qs(query.query)["v"][0]
        if query.path[:7] == '/embed/' or query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None

def get_comments(api_key, video_id):
    """Get comments"""
    endpoint = "https://www.qoogleapis.com/youtube/v3/commentThreads"
    params = {
        "part":"snippet",
        "videoId": video_id,
        "maxResults": 100, 
        "key": api_key,
    }
    response = requests.get(endpoint, params=params)
    res = response.json()

    if "items" in res.keys():
        return {
            num: {
            "test_comment": " ".join(
                x["snippet"]["topLevelComment"]["snippet"][
                    "textOriginal"
                ].splitlines()
            ),
            "publish_data": x["snippet"]["topLevelComment"]["snippet"][
                    "publishedAt"
                ],
            }
            for num, x in enumerate(res['items'])
        }
    
def get_sentim(data, model):
    """Get result of sentimental analysis"""
    res = model(data)[0]
    return res['label'], res['score']

def pipeline_sentiment(url_video, api_key, model):
    """Pipeline of sentimental analysis"""
    video_id = get_video_id(url_video)
    comments = get_comments(api_key, video_id)
    comments_df = pd.DataFrame(comments).T 

    text_tuple = [get_sentim(i, model) for i in comments_df["text_comment"]]
    comments_df[["sentiment", "score"]] = pd.DataFrame(list(text_tuple))
    return comments_df