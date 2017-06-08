#contributors Daniel Wood, Brian Wolk

from bs4 import BeautifulSoup, SoupStrainer
from newspaper import Article
import re
import nltk
from nltk import *
from tkinter import *
import webbrowser

output = 0;

###########TAG MODIFIERS#############
BASE_WEIGHT = 100 #The initial weighting for tags

HEAD_MOD = 10000     #The weight modifier for tags in the headline

VERB_MOD = 100     #the weight modifier for verb tags
NOUN_MOD = 150     #the weight modifier for noun tags

MOD = -100         #the weight modifier for non verb/noun/change tags
#######################################

###########BIGRAM MODIFIERS#############
HEAD_BOOST = 2000;
UNIQUENESS = -10;
#######################################

POS_VALUE = {
    'CC': BASE_WEIGHT,  # coordinating conjunction
    'CD': BASE_WEIGHT,  # cardinal digit
    'DT': BASE_WEIGHT,  # determiner
    'EX': BASE_WEIGHT,  # existential there (like: "there is" ... think of it like "there exists")
    'FW': BASE_WEIGHT,  # foreign word
    'IN': BASE_WEIGHT,  # preposition/subordinating conjunction
    'JJ': BASE_WEIGHT,  # adjective    'big'
    'JJR': BASE_WEIGHT,  # adjective, comparative    'bigger'
    'JJS': BASE_WEIGHT,  # adjective, superlative    'biggest'
    'LS': BASE_WEIGHT,  # list marker    1)
    'MD': BASE_WEIGHT,  # WEIGHTal    could, will
    'PDT': BASE_WEIGHT,  # predeterminer    'all the kids'
    'POS': BASE_WEIGHT,  # possessive ending    parent's
    'PRP': BASE_WEIGHT,  # personal pronoun    I, he, she
    'PRP$': BASE_WEIGHT,  # possessive pronoun    my, his, hers
    'RB': BASE_WEIGHT,  # adverb    very, silently,
    'RBR': BASE_WEIGHT,  # adverb, comparative    better
    'RBS': BASE_WEIGHT,  # adverb, superlative    best
    'RP': BASE_WEIGHT,  # particle    give up
    'TO': BASE_WEIGHT,  # to    go 'to' the store.
    'UH': BASE_WEIGHT,  # interjection    errrrrrrrm
    'WDT': BASE_WEIGHT,  # wh-determiner    which
    'WP': BASE_WEIGHT,  # wh-pronoun    who, what
    'WP$': BASE_WEIGHT,  # possessive wh-pronoun    whose
    'WRB': BASE_WEIGHT,  # wh-abverb    where, when
    'NN': BASE_WEIGHT,  # noun, singular 'desk'
    'NNS': BASE_WEIGHT,  # noun plural    'desks'
    'NNP': BASE_WEIGHT,  # proper noun, singular    'Harrison'
    'NNPS': BASE_WEIGHT,  # proper noun, plural    'Americans'
    'VB': BASE_WEIGHT,  # verb, base form    take
    'VBD': BASE_WEIGHT,  # verb, past tense    took
    'VBG': BASE_WEIGHT,  # verb, gerund/present participle    taking
    'VBN': BASE_WEIGHT,  # verb, past participle    taken
    'VBP': BASE_WEIGHT,  # verb, sing. present, non-3d    take
    'VBZ': BASE_WEIGHT,  # verb, 3rd person sing. present    takes
}


BIGRAMS = {
          }

NOUN_VALUE = {
    'NN': NOUN_MOD,  # noun, singular 'desk'
    'NNS': NOUN_MOD,  # noun plural    'desks'
    'NNP': NOUN_MOD,  # proper noun, singular    'Harrison'
    'NNPS': NOUN_MOD,  # proper noun, plural    'Americans'
}

VERB_VALUE = {
    'VB': VERB_MOD,  # verb, base form    take
    'VBD': VERB_MOD,  # verb, past tense    took
    'VBG': VERB_MOD,  # verb, gerund/present participle    taking
    'VBN': VERB_MOD,  # verb, past participle    taken
    'VBP': VERB_MOD,  # verb, sing. present, non-3d    take
    'VBZ': VERB_MOD,  # verb, 3rd person sing. present takes
}


# sets the values of tags based on the tags in the headline and in the article
def setTagValues(headline_tagged, article_tagged):
    for word in headline_tagged:
        if word[1] in POS_VALUE:
            POS_VALUE[word[1]] = POS_VALUE[word[1]] + HEAD_MOD
        BIGRAMS[word] = HEAD_BOOST

    for sent in article_tagged:
        for word in sent:
            if word[1] in POS_VALUE:
                if word[1] in NOUN_VALUE:
                    POS_VALUE[word[1]] = POS_VALUE[word[1]] + NOUN_MOD
                elif word[1] in VERB_VALUE:
                    POS_VALUE[word[1]] = POS_VALUE[word[1]] + VERB_MOD
                else:
                    POS_VALUE[word[1]] = POS_VALUE[word[1]] + MOD
            if word in BIGRAMS:
                BIGRAMS[word] = BIGRAMS[word] + UNIQUENESS
            else:
                BIGRAMS[word] = UNIQUENESS

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
    topStories = soup.find_all("div", id="latest-stories-tab-container")
    urls = []
    numUrls = 0
    for into in topStories:
        links = re.findall(r'href=[\'"]?([^\'" >]+)', str(into))
        for each in links:
            if (ord(each[len(each)-1]) < 97):
                url = "http://www.bbc.com" + each
                if(numUrls < 5):
                    urls.append(url)
                    numUrls += 1
                else:
                    return urls
    # return urls
    pass




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
    sentences = getParsedSentencesForSampleText(text)
    textTokenizedAndTagged = nltk.pos_tag(word_tokenize(text))

    return [title, titleTokenizedAndTagged,getParsedSentencesForSampleText(text), getParsedSentences(textTokenizedAndTagged)]

def getSentenceValue(sentence):
    value = 0
    for word in sentence:
         value += getWordValue(word[1])
         # value += BIGRAMS[word]

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

#Method that takes in story and splits it up into lists of sentences.
#Returns a list of sentences; list of lists
def getParsedSentencesForSampleText(text):
    #print(text)
    sentencesInStory = []
    wordsInSentence = []
    word = ""

    last = ""
    for i in text:
        if(last == '.' or last == '\"'):
            sentencesInStory.append(word)
            word = ""
        elif(i == '.'):
            word += i
            sentencesInStory.append(word)
            word = ""
            last = ""
        else:
            word += i
            last = i

    return sentencesInStory

#Takes in every sentence in a story and returns a list of sentence values.
def getListOfSentenceValues(sentences):
    sentenceValues = []
    for sentence in sentences:
        sentenceValues.append(getSentenceValue(sentence))
    return sentenceValues

#Takes in a list of urls and for each url it gets the story details using getStoryDetails()
def getStoryData(urls):
    storyData = []
    for story in urls:
        storyData.append(getstorydetails(story))
    return storyData


# Calculates the weight of each sentence in the story according to its tags. uses the getSentenceValue()
def calculatesentenceweights(stories):
    title_summary = []
    for story in stories:
        weightedSentence = []
        i = 0
        for tokenizedAndTaggedSentences in story[
            3]:  # Story[0] is title, story[1] is tokenized and tagged title, story[2] is story text, story[3] is tokenized and tagged text of story.
            weightedSentence.append([getSentenceValue(tokenizedAndTaggedSentences), tokenizedAndTaggedSentences, i])
            i += 1
        weightedSentence.sort()
        sent1 = weightedSentence[len(weightedSentence) - 1][1]
        sent2 = weightedSentence[len(weightedSentence) - 2][1]
        sent3 = weightedSentence[len(weightedSentence) - 3][1]
        string1 = ''
        string2 = ''
        string3 = ''
        for word in sent1:
            string1 += (word[0] + " ")
        for word in sent2:
            string2 += (word[0] + " ")
        for word in sent3:
            string3 += (word[0] + " ")
        indices = []
        indices.append((weightedSentence[len(weightedSentence) - 1][2], string1))
        indices.append((weightedSentence[len(weightedSentence) - 2][2], string2))
        indices.append((weightedSentence[len(weightedSentence) - 3][2], string3))
        indices.sort()
        summary = [story[0]]
        for i in range(3):
            summary.append(indices[i][1])
        title_summary.append(summary)
    return title_summary


#Launch the browser for the article
def launchBrowser(url):
    webbrowser.open_new(url)


# Gets the top story urls from Huffington post, The Guardian, and BBC news.
# Parses the story, tokenizes each word, and calculates the importance of each sentence.
def main():

    huffTopStoryUrls = getHuffHeadlineUrls('http://www.huffingtonpost.com/')
    guardianTopStoryUrls = getGuardianHeadlineUrls("https://www.theguardian.com/us")
    bbcTopStoryUrls = getBbcHeadlineUrls("http://www.bbc.com/news")

    huffData = []
    for url in huffTopStoryUrls:
        huffData.append(getstorydetails(url))
    setTagValues(huffData[1][1], huffData[1][3])
    list_of_huff_summaries = (calculatesentenceweights(huffData))


    bbcData = []
    for url in bbcTopStoryUrls:
        bbcData.append(getstorydetails(url))
    list_of_bbc_summaries = (calculatesentenceweights(bbcData))

    siteInfo = [huffData, bbcData]

    # for entry in list_of_huff_summaries:
    #     print(entry[0] + ':\n')
    #     print(entry[1] + "\n")
    #     print(entry[2] + "\n")
    #     print(entry[3] + '\n\n')
    #
    #
    #
    # for entry in list_of_bbc_summaries:
    #     print(entry[0] + ':\n')
    #     print(entry[1] + "\n")
    #     print(entry[2] + "\n")
    #     print(entry[3] + '\n\n')



    root = Tk()
    root.title("Informed")
    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)
    textwidget = Text(root)
    textBoxes = []
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"


    # news = [huffData]
    #
    # for site in news:
    #     i = 0
    #     for story in site:
    #
    #         summary = story[0] +"\n"
    #
    #         t = Text(textwidget, font=("Helvetica", 16), height=7, width=40)
    #         #t = Text(listBox, font=("Helvetica", 16), height=7, width=40)
    #         t.insert(END, summary)
    #         t.config(state=DISABLED)
    #         textBoxes.append(t)
    #         button = Button(text="source", command=lambda: launchBrowser(huffTopStoryUrls[i-1]))
    #         # print( "%d\n" %i)
    #         # print(huffTopStoryUrls[i])
    #         # print("\n")
    #         textBoxes.append(button)
    #         i += 1
    #     i = 0;

    news = [list_of_huff_summaries, list_of_bbc_summaries]
    source = 0
    sources = [bbcTopStoryUrls, huffTopStoryUrls]
    sources.reverse()
    for site in news:
        i = 0
        for story in site:

            summary = story[0] +"\n\n"
            first = story[1] +"\n"
            second = story[2] + "\n"
            third = story[3] + "\n"
            spacer = "\n"

            # print("------------------")
            # print(summary)
            # print(first)
            # print(second)
            # print(third)

            t = Text(textwidget, font=("Helvetica", 16), height=7, width=40)
            #t = Text(listBox, font=("Helvetica", 16), height=7, width=40)
            t.insert(END, summary)
            t.insert(END, first)
            t.insert(END, spacer)
            t.insert(END, second)
            t.insert(END, spacer)
            t.insert(END, third)
            t.insert(END, spacer)
            t.config(state=DISABLED)
            textBoxes.append(t)
            urls = sources[source]
            button = Button(text="source", command=lambda: launchBrowser(urls[i]))
            # print(sources[source][i])
            # print( "%d\n" %i)
            # print(huffTopStoryUrls[i])
            # print("\n")
            textBoxes.append(button)
            i += 1
        i = 0;
        source += 1

    for f in textBoxes:
        textwidget.window_create(INSERT, window = f)
    textwidget.pack()
    root.wm_maxsize(350,800)
    scrollbar.config(command=textwidget.yview)

    mainloop()

if __name__ == '__main__':
     main()