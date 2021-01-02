# yt-video-maker 

**IMPORTANT:** This project is currently put on-hold because I'm focusing my time on other things at the moment but I'll surely get back to finish it as soon as I can. In the meanwhile, feel free to send me your suggestions in form of a issue and even a PR, so I can review it.

Thanks so much for the patience!

<br />

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
SEARCH_ENGINE_ID=my_id
GOOGLE_SEARCH_API_KEY=my_api_key
```

# Structure

## Static Files Directory

Directory: `./src/static/`

```
This is the directory where the robot should place all static files (e.g. *.png)
```

# O.S. Dependencies

## Fonts

You need to install the following font on your O.S. in order to correct run the image processing feature:

```
arial (True Type Font)
``` 
