import json

from munch import munchify

file = "./content.json"

def save(content):
    """ Store content to JSON

    It waits for a dict and stores it into a JSON file
    """
    with open(file, 'w') as outfile:
        json.dump(content, outfile)

def load():
    """ Load data from JSON

    It loads JSON file data and returns it
    """
    with open(file) as json_file:
        content = json.load(json_file)
        # munchify provides attribute style access to dict objects
        # So we can still access attributes as a normal python object. E.g.: content.some_attribute 
        # Since content read from JSON file is no longer the original content object
    return munchify(content)