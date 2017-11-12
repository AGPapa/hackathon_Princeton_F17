# -*- coding: utf-8 -*-
import http.client
import json
import re
import requests
import urllib
import urllib.parse
import sys

#####################
# Url Parsing
#####################

def parseUrls(urls, parseFunction):
    result = []
    for url in urls:
        words = parseFunction(url)
        if len(words) == 0:
            return -1
        title = words[0].title() + " "
        for word in words[1:]:
            if word in not_capitalized_in_titles:
                title += word + " "
            else:
                title += word.title() + " "
        result.append({
            "url": url,
            "title": title.strip()
        })
    return result

def parseKhanAcademy(url):
    return url.split("/")[-1].split("-")

def parsePaulsNotes(url):
    return re.findall('[A-Z][^A-Z]*', url.split("/")[-1].split(".")[0])

def parseMathPlayground(url):
    return url.split("/")[-1].split(".")[0].split("_")

def parseStudyDotCom(url):
    return url.split("/")[-1].split(".")[0].split("-")

def parseGrammarbook(url):
    return url.split("/")[-2].split("-")

#####################
# Search
#####################

# getHelpSites = [
#     "tutorial.math.lamar.edu", 
#     "khanacademy.org", 
#     "mathplayground.com"
#     # "grammarbook.com",
#     # "study.com"
#     ]
# searchingSitesGetHelp = "("
# for site in getHelpSites[:-1]:
#     searchingSitesGetHelp += "site:" + site
#     searchingSitesGetHelp += "%20OR%20"
# searchingSitesGetHelp += getHelpSites[-1] + ")"
# print(searchingSitesGetHelp)

def BingWebSearch(term):
    "Performs a Bing Web search and returns the results."

    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
    conn = http.client.HTTPSConnection(host)
    query = urllib.parse.quote(term)
    conn.request("GET", path + "?q=" + query, headers=headers)
    response = conn.getresponse()
    headers = [k + ": " + v for (k, v) in response.getheaders()
                   if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
    return headers, response.read().decode("utf8")

def parseResponse(response):
    links = response["webPages"]["value"][0]
    if "deepLinks" not in links:
        return -1
    deepLinkDicts = links["deepLinks"]
    deepLinks = []
    for item in deepLinkDicts:
        deepLinks.append(item["url"])
    return deepLinks

def determineSubjectFromTerm(term):
    for subject in subject_terms:
        if term in subject_terms[subject]:
            return subject

def correctSpelling(term):
    return term

def runSearch(entity, subject):
    searchResults = []
    for site in subjectToSites[subject]:
        currentTerm = entity + ' ' + site["site"]
        headers, result = BingWebSearch(currentTerm)
        response = json.loads(result)
        # print(response)
        urls = parseResponse(response)
        # print(urls)
        if urls == -1:
            continue
        urlsAndTitles = parseUrls(urls, site["function"])
        # print(urlsAndTitles)
        if urlsAndTitles == -1:
            continue
        for urlsAndTitle in urlsAndTitles:
            searchResults.append(urlsAndTitle)
    return searchResults

def extractIntentAndEntity(query):
    base_url = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/daf031ac-3b4e-4508-b0de-91f76fd0348f?subscription-key=7ec7b1d0fbb24d01bd1e20841e00bb15&spellCheck=true&verbose=true&timezoneOffset=-5.0&q="

    url = base_url + query

    page = requests.get(url).text
    data = json.loads(page)
    
    intent = data["topScoringIntent"]["intent"]
    try:
        entity = data["entities"][0]["entity"]
    except:
        entity = ""

    return (intent, entity)

def getSubjectForEntity(entity):
    base_url = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/a98694fb-822c-447f-a106-e5734ca1c0b2?subscription-key=7ec7b1d0fbb24d01bd1e20841e00bb15&spellCheck=true&verbose=true&timezoneOffset=-5.0&q="
    
    url = base_url + entity
    page = requests.get(url).text
    data = json.loads(page)
    
    subject = data["topScoringIntent"]["intent"]
    return subject

subscriptionID = 'bdcf9c7f-5abf-41cb-ae83-c5d23553e5d7'
subscriptionKey = '9a39601ea785453bb1eee78d77ece218'
host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/search"

term = "trigonometry" 
not_capitalized_in_titles = ["a","an","the","for","and","nor","but","or","yet","so","with","at","from","into","during","until","against","among","throughout","despite","towards","upon","of","to","in","on","by","about","like","through","over","before","between","after","since","without","under","within","along","across","behind","beyond","plus","but","up","out","around","down","off","above","near"]

subjectToSites = {
    "Math": 
        [{
            "site": "khan academy",
            "function": parseKhanAcademy
        },
        {
        "site": "paul's notes",
        "function": parsePaulsNotes
        },
        {
            "site": "math playground",
            "function": parseMathPlayground
        }],
    "English": 
        [{
            "site": "grammarbook.com",
            "function": parseGrammarbook
        }],
    "Chemistry": 
        [{
            "site": "khan academy",
            "function": parseKhanAcademy
        },
        {
            "site": "study.com",
            "function": parseStudyDotCom
        }
    ]
}

# searchResults = runSearch(term)
# print(searchResults)

for line in sys.stdin:
    (intent, entity) = extractIntentAndEntity(line)
    print((intent, entity))
    if len(entity) == 0:
        subject = "Blank"
    else:
        subject = getSubjectForEntity(entity)
    print(subject)
    
    if (intent == "Thank you"):
        print("You're welcome! Keep learning!")
    elif (intent == "None"):
        print("I'm sorry, I didn't understand that.")
    elif (intent == "Hello"):
        print("Hi!")
    elif (intent == "GetHelpWith"):
        print("Here's some information that might help")
        search = runSearch(entity, subject)
        for result in search:
            print(result["title"] + ": " + result["url"])
    elif (intent == "GetPracticeWith"):
        print("I'll find some practice problems")
        search = runSearch(entity + " practice problems", subject)
        for result in search:
            print(result["title"] + ": " + result["url"])