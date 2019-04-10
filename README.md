# yt-video-maker
Open source project designed to make automated videos.

Main tasks overview: The robots define video text content which is processed by Watson AI, add video Tags based on the subject, seek and choose related images on Google Images, process chosen images, create sentences with images, create video Thumbnail, video rendering using After Effects and finally the video upload by OAauth authentication.


# Credentials format (Python Decouple)

## Algorithmia

File: `.env`

```
ALGORITHMIA_API_KEY=my_api_key
```

## Watson Natural Language Understanding

File: `.env`

```
WATSON_API_KEY=my_api_key
```

## Google Custom Search Engine API

File: `.env`

```
SEARCH_ENGINE_ID=my_api_key
```

## Static Files Directory

Directory: `./src/static/`

```
This is the directory where the robot should place all static files (e.g. *.png)
```