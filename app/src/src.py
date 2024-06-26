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
    endpoint = "https://www.googleapis.com/youtube/v3/commentThreads"
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
            "text_comment": " ".join(
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
    
def get_sentim(data, headers, url):
    """Get result of sentimental analysis"""
    res = requests.post(url, headers=headers, json=data)
    res = res.json()[0][0]
    return res['label'], res['score']

def pipeline_sentiment(url_video, api_key, headers, url):
    """Pipeline of sentimental analysis"""
    video_id = get_video_id(url_video)
    comments = get_comments(api_key, video_id)
    comments_df = pd.DataFrame(comments).T 

    text_tuple = [get_sentim(i, headers, url) for i in comments_df["text_comment"]]
    comments_df[["sentiment", "score"]] = pd.DataFrame(list(text_tuple))
    return comments_df

def pipeline_stats(data):
    """Get statistic of sentiment"""
    return data['sentiment'].value_counts(normalize=True).mul(100).round(2)

def pipeline_summarize(data, headers, url, length=2000, max_length=35):
    """Get summarization result"""
    text = " ".join(data)
    result_text = []

    for i in range(0, len(text), length):
        new_text = text[i : i + length]
        payload = {
            "inputs": new_text,
            "parameters": {
                "max_length": max_length
            }       
        }
        res = requests.post(url, headers=headers, json=payload)
        result_text.append(res.json()[0]["summary_text"])

    return " ".join(result_text)
