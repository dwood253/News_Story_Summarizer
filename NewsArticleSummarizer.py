from bs4 import BeautifulSoup, SoupStrainer
from newspaper import Article
import re
import nltk
from nltk import *

POS_VALUE = {
        'CC': 10,   #	coordinating conjunction
        'CD': 10,   #	cardinal digit
        'DT': 10,   #	determiner
        'EX': 10,   #	existential there (like: "there is" ... think of it like "there exists")
        'FW': 10,   #	foreign word
        'IN': 10,   #	preposition/subordinating conjunction
        'JJ': 10,   #	adjective	'big'
        'JJR': 10,  #	adjective, comparative	'bigger'
        'JJS': 10,  #	adjective, superlative	'biggest'
        'LS': 10,   #	list marker	1)
        'MD': 10,   #	modal	could, will
        'NN': 10,   #	noun, singular 'desk'
        'NNS': 10,  #	noun plural	'desks'
        'NNP': 10,  #	proper noun, singular	'Harrison'
        'NNPS': 10, #	proper noun, plural	'Americans'
        'PDT': 10,  #	predeterminer	'all the kids'
        'POS': 10,  #	possessive ending	parent's
        'PRP': 10,  #	personal pronoun	I, he, she
        'PRP$': 10, #	possessive pronoun	my, his, hers
        'RB': 10,   #	adverb	very, silently,
        'RBR': 10,  #	adverb, comparative	better
        'RBS': 10,  #	adverb, superlative	best
        'RP': 10,   #	particle	give up
        'TO': 10,   #	to	go 'to' the store.
        'UH': 10,   #	interjection	errrrrrrrm
        'VB': 10,   #	verb, base form	take
        'VBD': 10,  #	verb, past tense	took
        'VBG': 10,  #	verb, gerund/present participle	taking
        'VBN': 10,  #	verb, past participle	taken
        'VBP': 10,  #	verb, sing. present, non-3d	take
        'VBZ': 10,  #	verb, 3rd person sing. present	takes
        'WDT': 10,  #	wh-determiner	which
        'WP': 10,   #	wh-pronoun	who, what
        'WP$': 10,  #	possessive wh-pronoun	whose
        'WRB': 10   #	wh-abverb	where, when
             }

#Grab all the urls in huffington post's top stories section.
#return list of urls to huffington posts top stories.
def getHuffHeadlineUrls(rootUrl):
    article = Article(rootUrl)
    article.download()
    html = article.html
    soup = BeautifulSoup(html, "html.parser")
    linksToTopStories = []
    topStories = soup.find_all("div", class_="card__headlines")
    urls = []
    i = 1
    for story in topStories:
        urls.append(re.findall('"(http.*?)"', str(story), re.IGNORECASE))
        i+=1
        if i > 5:
            break
    for url in urls:
        for link in url:
            if link not in linksToTopStories:
                linksToTopStories.append(link)

    return linksToTopStories

#Grab all the urls in the Guardians post's top stories section.
#return list of urls to theGuardians posts top stories.
def getGuardianHeadlineUrls(rootUrl):
    article = Article(rootUrl)
    article.download()
    html = article.html
    soup = BeautifulSoup(html, "html.parser")
    linksToTopStories = []
    topStories = soup.find_all("footer", class_="fc-item__footer--horizontal")
    urls = []
    i = 1
    for story in topStories:
        urls.append(re.findall('"(http.*?)"', str(story), re.IGNORECASE))
        i+=1
        if i > 4:
            break
    for url in urls:
        for link in url:
            if link not in linksToTopStories:
                linksToTopStories.append(link)

    return linksToTopStories

#Grab all the urls on the BBC's top stories section.
#return list of urls to the BBC's posts top stories.
def getBbcHeadlineUrls(rootUrl):
    article = Article(rootUrl)
    article.download()
    html = article.html
    soup = BeautifulSoup(html, "html.parser")
    linksToTopStories = []
    topStories = soup.find_all("div", id="news-top-stories-body-inline-international")
    urls = []
    i = 1
    for story in topStories:
        urls.append(re.findall('"(http.*?)"', str(story), re.IGNORECASE))
        i+=1
        if i > 4:
            break
    for url in urls:
        for link in url:
            if link not in linksToTopStories:
                linksToTopStories.append(link)

    return linksToTopStories




#Create article object from url, retrieve title and text, tokenized and tagged text and parsed tokenized sentences
def getstorydetails(url):
    article = Article(url)
    article.download()
    article.parse()
    # title = article.title
    # text = article.text

    title = article.title
    titleTokenizedAndTagged = nltk.pos_tag(word_tokenize(title))
    text = article.text
    textTokenizedAndTagged = nltk.pos_tag(word_tokenize(text))
    print(url)

    print(title)
    print(titleTokenizedAndTagged)

    return [title, titleTokenizedAndTagged,text, getParsedSentences(textTokenizedAndTagged)]

def getSentenceValue(sentence):
    value = 0
    for word in sentence:
         value += getWordValue(word[1])
    return value

def getWordValue(word):
    value = 0;
    if word in POS_VALUE:
        value = POS_VALUE[word]
    return value

#Method that takes in tokenized story and splits it up into lists of sentences.
#Returns a list of sentences; list of lists
def getParsedSentences(text):
    sentencesInStory = []
    wordsInSentence = []

    for i in text:
        if(i[0] == '.'):
            wordsInSentence.append(i)
            sentencesInStory.append(wordsInSentence)
            wordsInSentence = []
        else:
            wordsInSentence.append(i)

    return sentencesInStory


#Takes in every sentence in a story and returns a list of sentence values.
def getListOfSentenceValues(sentences):
    sentenceValues = []
    for sentence in sentences:
        sentenceValues.append(getSentenceValue(sentence))
    return sentenceValues

#Takes in a list of urls and for each url it gets the story details using getStoryDetails()
def getHuffData(urls):
    huffData = []
    for story in urls:
        huffData.append(getstorydetails(story))
    return huffData

#Calculates the weight of each sentence in the story according to its tags. uses the getSentenceValue()
def calculatesentenceweights(stories):
    for story in stories:
        weightedSentence = []
        for tokenizedAndTaggedSentences in story[3]:#Story[0] is title, story[1] is tokenized and tagged title, story[2] is story text, story[3] is tokenized and tagged text of story.
            weightedSentence.append([getSentenceValue(tokenizedAndTaggedSentences), tokenizedAndTaggedSentences])
        print (weightedSentence)

# Gets the top story urls from Huffington post, The Guardian, and BBC news.
# Parses the story, tokenizes each word, and calculates the importance of each sentence.
def main():

    huffTopStoryUrls = getHuffHeadlineUrls('http://www.huffingtonpost.com/')
    guardianTopStoryUrls = getGuardianHeadlineUrls("https://www.theguardian.com/us")
    bbcTopStoryUrls = getBbcHeadlineUrls("http://www.bbc.com/news")
    print(bbcTopStoryUrls)
    print(guardianTopStoryUrls)
    huffData = getHuffData(huffTopStoryUrls)
    calculatesentenceweights(huffData)



    # for url in huffTopStoryUrls:
    #     huffData.append(getStoryDetails(url))

    # print(huffData[0])

if __name__ == '__main__':
     main()