import settings
import json

from robots.state import load, save;

from googleapiclient.discovery import build

def robot():
    content = load()

    def google_search(search_term, api_key, cse_id, **kwargs):
        service = build("customsearch", "v1", developerKey=api_key)
        response = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        return response['items']

    def fetchGoogleAndReturnImagesLinks(query):
        imagesUrl = []
        results = google_search(
            query, 
            settings.GOOGLE_SEARCH_API_KEY, 
            settings.SEARCH_ENGINE_ID, 
            searchType="image",
            imgSize="huge", 
            num=2)

        for result in results:
            imagesUrl.append(result['link'])

        return imagesUrl

    def fetchImagesOfAllSentences(content):
        for sentence in content.sentences:
            query = f"{ content.search_term } { sentence.keywords[0] }"
            sentence.images = fetchGoogleAndReturnImagesLinks(query)

            sentence.googleSearchQuery = query

    fetchImagesOfAllSentences(content)

    # Print the final result of the content object structure
    content_json = json.dumps(content, indent=2)
    print(content_json)