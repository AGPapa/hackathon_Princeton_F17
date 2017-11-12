import urllib
import json

def query(q):
    base_url = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/daf031ac-3b4e-4508-b0de-91f76fd0348f?subscription-key=7ec7b1d0fbb24d01bd1e20841e00bb15&spellCheck=true&verbose=true&timezoneOffset=-5.0&q="

    url = base_url + q

    response = urllib.urlopen(url)
    data = json.loads(response.read())
    
    intent = data["topScoringIntent"]["intent"]
    try:
        entity = data["entities"][0]["entity"]
    except:
        entity = ""
    return (intent, entity)

def subject(q):
    base_url = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/a98694fb-822c-447f-a106-e5734ca1c0b2?subscription-key=7ec7b1d0fbb24d01bd1e20841e00bb15&spellCheck=true&verbose=true&timezoneOffset=-5.0&q="
    
    url = base_url + q

    response = urllib.urlopen(url)
    data = json.loads(response.read())
    
    intent = data["topScoringIntent"]["intent"]
    return intent
