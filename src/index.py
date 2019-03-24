import sys
import json

from robots.text import robot

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

    # New instance of content object
    content = Content()

    # Maximum amount of sentences to be processed by Watson IA
    content.max_sentences = 7

    def ask_and_return_search():
        # Asks for the Wikipedia search term and returns it
        return input("Type a Wikipedia search term:")

    def ask_and_return_prefix():
        # Lists the search prefix pre-defined options and asks for the user to choose between them
        prefixes = ['Who is', 'What is', 'The history of']
        for index in range(0, 3):
            print(f"[{ index + 1 }] - { prefixes[index] }")
        print("[0] - exit")
        selected_prefix_index = int(input("Choose one option:")) - 1
        if selected_prefix_index >= 0:
            return prefixes[selected_prefix_index]
        sys.exit(1)

    # Stores the data provided from the user
    content.search_term = ask_and_return_search()
    content.prefix = ask_and_return_prefix()

    # Starts the text robot passing the content object to it
    robot(content)

    # print(content)

# Initialize the robots orchestrator
start()