import settings
import json
import requests
import os
from io import BytesIO

from robots.state import load, save;

from googleapiclient.discovery import build
from PIL import Image

def robot():
    current_directory = os.path.dirname(__file__)
    content = load()

    def google_search(search_term, api_key, cse_id, **kwargs):
        service = build("customsearch", "v1", developerKey=api_key)
        response = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        return response['items']

    def fetch_google_and_return_images_links(query):
        images_url = []
        results = google_search(
            query, 
            settings.GOOGLE_SEARCH_API_KEY, 
            settings.SEARCH_ENGINE_ID, 
            searchType="image",
            imgSize="huge", 
            num=2)

        for result in results:
            images_url.append(result['link'])

        return images_url

    def fetch_images_of_all_sentences(content):
        print("> Getting image URLs from Google Images...")

        for sentence in content.sentences:
            query = f"{ content.search_term } { sentence.keywords[0] }"
            sentence.images = fetch_google_and_return_images_links(query)

            sentence.google_search_query = query

    def download_and_save_image(image_url, file_name):
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        response.raw.decode_content = True # Required to decompress gzip/deflate compressed responses
        
        with Image.open(response.raw) as img:
            img.save(f"{ current_directory }/../static/{ file_name }")

    def download_all_images(content):
        downloaded_images = []
        sentence_index = 0

        print("> Downloading images...")

        for sentence in content.sentences:
            images = sentence.images

            for image in images:
                image_url = image

                try:
                    if image_url in str(downloaded_images):
                        raise FileExistsError("Image already downloaded!")
                    download_and_save_image(image_url, f"{ sentence_index }_raw.png")
                    downloaded_images.append(image_url)
                    print(f"Image download successfuly! URL: { image_url }")
                    break
                except Exception as error:
                    print(f"Error: Couldn't download image. URL: { image_url } - { error }")

            sentence_index += 1
        content.downloaded_images = downloaded_images

    fetch_images_of_all_sentences(content)
    download_all_images(content)
    save(content.__dict__)


    # Print the final result of the content object structure
    # content_json = json.dumps(content, indent=2)
    # print(content_json)