---
title: Sentiment Summarize Youtube Comms
emoji: 👀
colorFrom: red
colorTo: indigo
sdk: docker
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# Sentiment and summarize russian YouTube-video comments

This is web-server on [![FastAPI](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)](https://fastapi.tiangolo.com/) for sentiment analysis and summarization of russian YouTube comments

## End-Points

| Endpoint          | Description             |
|-------------------|-------------------------|
| `/comments`       | Get comments and sentimental analysis |
| `/stats`          | Get comments sentiment statistics |
| `/summarization`  | Get summarization of comments |

## Model for sentiment analysis

[![Hugging Face](https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo.svg)](https://huggingface.co/MonoHime/rubert-base-cased-sentiment-new)

## Model for summarization

[![Hugging Face](https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo.svg)](https://huggingface.co/IlyaGusev/mbart_ru_sum_gazeta)

## Demo Server App

[![Hugging Face](https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo.svg)](https://macrdel-sentiment-summarize-youtube-comms.hf.space)
