import json

from robots.state import load
from robots.text import robot as robot_text
from robots.input import robot as robot_input

class Content:
    def __init__(self):
        self.search_term = ""
        self.prefix = ""
        self.search_content_original = ""
        self.source_content_clean = ""
        self.sentences = []
        self.max_sentences = 0

    def __str__(self):
        return f"{ self.search_term }'s content"


def start():
    # Function designed to orchestrate the robots calls

    content = Content()

    robot_input(content)

    # Starts the text robot passing the content object to it
    robot_text()

    # Gets the JSON content in order to show the file's content
    content_json = load()
    print("Loading JSON file....")
    print(content_json)

# Initialize the robots orchestrator
start()