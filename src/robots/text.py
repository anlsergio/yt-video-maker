import Algorithmia
import json
import re
import nltk
from nltk.tokenize import sent_tokenize

from decouple import config

# Used to download en package for nltk:
# nltk.download()

def fetchContentFromWikipedia(content):
    algorithmiaAuthenticated = Algorithmia.client(config('ALGORITHMIA_API_KEY'))
    wikipediaAlgorithm = algorithmiaAuthenticated.algo('web/WikipediaParser/0.1.2')
    try:
        print('trying....')
        wikipediaContent = wikipediaAlgorithm.pipe(content.searchTerm).result
        content.sourceContentOriginal = wikipediaContent['content']

    except Exception as error:
        print(error)

def removeDatesInParentheses(text):
    return re.sub(r'\([^)]*\)', '', text)

def clearContent(content):
    def removeBlankLinesAndMarkdown(text):
        allLines = text.split('\n')
        withoutBlankLinesAndMarkdown = []

        for x in allLines:
            stripped = x.strip()
            if len(stripped) > 0 and not stripped.startswith('='):
                withoutBlankLinesAndMarkdown.append(stripped)
        return str(" ".join(withoutBlankLinesAndMarkdown))
    
    withoutBlankLinesAndMarkdown = removeBlankLinesAndMarkdown(content.sourceContentOriginal)
    withoutDatesInParentheses = removeDatesInParentheses(withoutBlankLinesAndMarkdown)
    content.sourceContentClean = withoutDatesInParentheses

def breakContentInSentences(content):
    sent_tokenize_list = sent_tokenize(content.sourceContentClean)
    for sentence in sent_tokenize_list:
        content.sentences.append({'text': sentence, 'keywords': [], 'images': []})

def robot(content):

    print(f"I've received a content: { content }")
    fetchContentFromWikipedia(content)
    clearContent(content)
    breakContentInSentences(content)

    content_json = json.dumps(content.__dict__)
    print(content_json)