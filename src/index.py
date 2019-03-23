import sys
import json

from robots.text import robot

class Content:
    def __init__(self):
        self.searchTerm = ""
        self.prefix = ""
        self.searchContentOriginal = ""
        self.sourceContentClean = ""
        self.sentences = []

    def __str__(self):
        return f"{ self.searchTerm }'s content"


def start():
    content = Content()

    def askAndReturnSearch():
        return input("Type a Wikipedia search term:")

    def askAndReturnPrefix():
        prefixes = ['Who is', 'What is', 'The history of']
        for index in range(0, 3):
            print(f"[{ index + 1 }] - { prefixes[index] }")
        print("[0] - exit")
        selectedPrefixIndex = int(input("Choose one option:")) - 1
        if selectedPrefixIndex >= 0:
            return prefixes[selectedPrefixIndex]
        sys.exit(1)

    
    content.searchTerm = askAndReturnSearch()
    content.prefix = askAndReturnPrefix()

    robot(content)

    print(content)

start()