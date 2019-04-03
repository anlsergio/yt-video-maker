import json
import re
import settings

from robots.state import save, load

import Algorithmia
import nltk
from nltk.tokenize import sent_tokenize
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, KeywordsOptions

# Uncomment the line below to download 'en' package for nltk:
# nltk.download()

def fetch_content_from_wikipedia(content):
    # This function uses algorithmia API to fetch data from Wikipedia source based on search term and
    # stores it in source_content_original

    algorithmia_authenticated = Algorithmia.client(settings.ALGORITHMIA_API_KEY)
    wikipedia_algorithm = algorithmia_authenticated.algo('web/WikipediaParser/0.1.2')
    try:
        print('trying....')
        wikipedia_content = wikipedia_algorithm.pipe(content.search_term).result
        content.source_content_original = wikipedia_content['content']

    except Exception as error:
        print(error)

def remove_dates_in_parentheses(text):
    """ Remove content between parentheses

        Remove anything between parentheses from the given text using Regex.
    """
    return re.sub(r'\([^)]*\)', '', text)

def clear_content(content):
    """ Remove blank lines and Wikipedia markdown characteres

        Remove any blank lines and ugly Wikipedia markdowns from a given text.
    """
    def remove_blank_lines_and_markdown(text):
        all_lines = text.split('\n')
        without_blank_lines_and_markdown = []

        for x in all_lines:
            stripped = x.strip()
            if len(stripped) > 0 and not stripped.startswith('='):
                without_blank_lines_and_markdown.append(stripped)
        return str(" ".join(without_blank_lines_and_markdown))
    
    # These lines are designed to process the text clean up chain
    without_blank_lines_and_markdown = remove_blank_lines_and_markdown(content.source_content_original)
    without_dates_in_parentheses = remove_dates_in_parentheses(without_blank_lines_and_markdown)
    content.source_content_clean = without_dates_in_parentheses

def break_content_in_sentences(content):
    # This function uses nltk IA library to recognize and break text in separated sentences (Sentence Boundary Detection)
    # Also it initializes the data structure of content.sentences atribute
    sent_tokenize_list = sent_tokenize(content.source_content_clean)
    for sentence in sent_tokenize_list:
        content.sentences.append({'text': sentence, 'keywords': [], 'images': [], 'googleSearchQuery': []})

def fetch_watson_and_return_keywords(sentence):
    """ Use IBM Watson IA for applying tags

        Provides IBM Watson a sentece and returns a list of tags
    """
    NLU = NaturalLanguageUnderstandingV1(
        version='2018-11-16',
        iam_apikey=settings.WATSON_API_KEY,
        url='https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2018-11-16'
    )

    try:
        response = NLU.analyze(
            text = sentence,
            features=Features(
                keywords=KeywordsOptions(
                    limit=5
                )
            )
        ).get_result()

        # It gets all texts from the response and turn each of them into an element of the keywords list
        refined_response = response.get("keywords")
        keywords = [x.get("text") for x in refined_response]

        return keywords
    except Exception as error:
        print(error)


def limit_max_sentences(content):
    # This function slices the array of sentences to the number previously defined
    content.sentences = content.sentences[0:content.max_sentences]


def fetch_sentences_keywords(content):
    for sentence in content.sentences:
        sentence['keywords'] = fetch_watson_and_return_keywords(sentence.get('text'))

def robot():
    """ Text Robot
        These function gives live to the text robot
    """ 
    print("Pre loading data from JSON...")

    content = load()

    fetch_content_from_wikipedia(content)
    clear_content(content)
    break_content_in_sentences(content)
    limit_max_sentences(content)
    fetch_sentences_keywords(content)

    save(content.__dict__)

    # It prints the content object as a JSON format
    # content_json = json.dumps(content.__dict__, indent=2)
    # print(content_json)