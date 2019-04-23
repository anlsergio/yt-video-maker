import os
import textwrap

from robots.state import load

from PIL import Image, ImageFilter, ImageFont, ImageDraw

def robot():
    current_directory = os.path.dirname(__file__)

    content = load()   

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
        text_lines = textwrap.wrap(sentence_text, width=75)

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
                shadow_offset = 2

                for line in text_lines:
                    font_width, font_height = font.getsize(line)
                    # For every line of the sentence add the corresponding font size height value to the 
                    # Height position of the text, so it doesn't overlap on the past added line
                    # Draws text into the image (position tuple, text, color and font)
                    draw.text((width_pos+shadow_offset, height_pos+shadow_offset), line, (0,0,0), font=font)
                    draw.text((width_pos-shadow_offset, height_pos-shadow_offset), line, (0,0,0), font=font)
                    draw.text((width_pos+shadow_offset, height_pos-shadow_offset), line, (0,0,0), font=font)
                    draw.text((width_pos-shadow_offset, height_pos+shadow_offset), line, (0,0,0), font=font)
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

    convert_all_images(content)

    create_all_sentence_images(content)
    create_youtube_thumbnail()