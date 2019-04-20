import sys

from robots.state import save

def robot(content):
    # function designed to ask and return search term and prefix from the user
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

    save(content.__dict__)