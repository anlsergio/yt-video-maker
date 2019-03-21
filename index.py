import sys

class Question:
    def __init__(self, searchTerm, prefix):
        self.searchTerm = searchTerm
        self.prefix = prefix

def start():
    question = Question("data", "data")

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

    
    question.searchTerm = askAndReturnSearch()
    question.prefix = askAndReturnPrefix()
    print(question.searchTerm)
    print(question.prefix)

start()