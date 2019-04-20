import settings
import json
import requests
import os
import textwrap
from io import BytesIO

from robots.state import load, save;

from googleapiclient.discovery import build
from PIL import Image, ImageFilter, ImageFont, ImageDraw

current_directory = os.path.dirname(__file__)

def robot():
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

    
    def convert_image(sentence_index):
        img_original = False
        input_image_path = f"{ current_directory }/../static/{ sentence_index }_raw.png"
        output_image_path = f"{ current_directory }/../static/{ sentence_index }_converted.png"
        width = 1920
        height = 1080

        try:
            img_original = Image.open(input_image_path).convert('RGBA')
        except FileNotFoundError as err:
            print(f"Image '{ sentence_index }_raw.png' doesn't exist on file system")
        print(input_image_path)
        
        if img_original:
            try:
                img_resized = img_original.resize((width, height))
                img_resized.filter(ImageFilter.GaussianBlur(30)).save(output_image_path)

                print(">Successfuly converted")
            except AttributeError as err:
                print(f"Couldn't convert image '{ sentence_index }_raw.png': { err }")

            try:
                img_original.thumbnail((height, height))
                img_w, img_h = img_original.size

                background_img = Image.open(output_image_path).convert('RGBA')
                bkg_w, bkg_h = background_img.size

                offset = ((bkg_w - img_w) // 2, (bkg_h - img_h) // 2)

                background_img.paste(img_original, offset, img_original)
                background_img.save(output_image_path)
                print(">Successfuly merged")
            except AttributeError as err:
                print(f"Couldn't blur and merge image '{ sentence_index }_raw.png': { err }")

    def convert_all_images(content):
        print("> Transforming images...")

        for index in range(len(content.sentences)):
            convert_image(index)

    def create_sentence_image(sentence_index, sentence_text):
        img_path = f"{ current_directory }/../static/{ sentence_index }_converted.png"
        output_image_path = f"{ current_directory }/../static/{ sentence_index }_sentence.png"
        img = False

        # It wraps a whole string into separated lines as a list for every 80 chars long
        text_lines = textwrap.wrap(sentence_text, width=80)

        try:
            img = Image.open(img_path)
        except FileNotFoundError as err:
            print(f"Image '{ sentence_index }_raw.png' doesn't exist on file system: { err }")

        if img:
            try:
                img_w, img_h = img.size

                # Template for positioning text on image using 2 different positions for every index iteration
                template = {
                    '0': {
                        'position': (100, 50)
                    },
                    '1': {
                        'position': (100, img_h - 350)
                    },
                    '2': {
                        'position': (100, 50)
                    },
                    '3': {
                        'position': (100, img_h - 350)
                    },
                    '4': {
                        'position': (100, 50)
                    },
                    '5': {
                        'position': (100, img_h - 350)
                    },
                    '6': {
                        'position': (100, 50)
                    },
                    '7': {
                        'position': (100, img_h - 350)
                    }
                }

                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("arial.ttf", 48)
                position = template[str(sentence_index)]['position']
                width_pos, height_pos = position
                shadow_weight = 2

                for line in text_lines:
                    font_width, font_height = font.getsize(line)
                    # For every line of the sentence add the corresponding font size height value to the 
                    # Height position of the text, so it doesn't overlap on the past added line
                    # Draws text into the image (position tuple, text, color and font)
                    draw.text((width_pos+shadow_weight, height_pos+shadow_weight), line, (0,0,0), font=font)
                    draw.text((width_pos-shadow_weight, height_pos-shadow_weight), line, (0,0,0), font=font)
                    draw.text((width_pos+shadow_weight, height_pos-shadow_weight), line, (0,0,0), font=font)
                    draw.text((width_pos-shadow_weight, height_pos+shadow_weight), line, (0,0,0), font=font)
                    draw.text((width_pos, height_pos), line, (255,255,255), font=font)
                    height_pos += font_height
                img.save(output_image_path)
            except AttributeError:
                print(f"Couldn't add text to image { sentence_index }_converted.png")

    def create_all_sentence_images(content):
        print("> Drawing sentences text into related images...")
        sentence_index = 0
        for sentence in content.sentences:
            create_sentence_image(sentence_index, sentence.text)
            sentence_index += 1


    def create_youtube_thumbnail():
        img_path = f"{ current_directory }/../static/0_converted.png"
        output_img = f"{ current_directory }/../static/youtube_thumbnail.jpg"

        print("> Creating Youtube Thumbnail...")

        try:
            img = Image.open(img_path).convert('RGB')
            img.save(output_img)
        except FileNotFoundError as err:
            print(f"Couldn't generate Youtube Thumbnail: { err }")

    fetch_images_of_all_sentences(content)
    download_all_images(content)
    save(content.__dict__)


    # Print the final result of the content object structure
    # content_json = json.dumps(content, indent=2)
    # print(content_json)

    convert_all_images(content)

    create_all_sentence_images(content)
    create_youtube_thumbnail()