# Start with one review:
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import requests
import json


#constants
apiUrl = "https://book-of-mormon-api.vercel.app/"
FirstNephi = "1nephi"
SecondNephi = "2nephi"
Jacob = "jacob"
Enos = "enos"
Jarom = "jarom"
Omni = "omni"
WordsofMormon = "wordsofmormon"
Mosiah = "mosiah"
Alma = "alma"
Heleman = "helaman"
ThirdNephi = "3nephi"
FourthNephi = "4nephi"
Mormon = "mormon"
Ether = "ether"
Moroni = "moroni"

def get(book, chapter, verse):
    requestURL = apiUrl + book + "/" + chapter + "/" + verse
    response = requests.get(requestURL)
    if len(response.content) == 0:
        return None
    content = response.content.decode('utf-8')
    return json.loads(content)
def getBook(text, scripture, book):
    counter = 1
    chapterCounter = 1
    while scripture is not None:
        while scripture is not None:
            counter += 1
            scripture = get(book, str(chapterCounter), str(counter))
            if scripture is None:
                break
            text += " "
            text += scripture["text"]
        chapterCounter += 1
    return text
def getChapter(text, scripture, book, chapter):
    counter = 1
    while scripture is not None:
        counter += 1
        scripture = get(book, chapter, str(counter))
        if scripture is None:
            break
        text += " "
        text += scripture["text"]
    return text
def generateWordCloud(text):
    wordcloud = WordCloud( max_words=100, background_color="white").generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

def GetWordCloudVerse(book, chapter, verse):
    scripture = get(book, chapter, verse)
    text = scripture["text"]
    generateWordCloud(text)

def GetWordCloudBook(book):
    scripture = get(book, "1", "1")
    text = scripture["text"]
    text = getBook(text, scripture, book)
    generateWordCloud(text)

def GetWordCloudChapter(book, chapter):
    scripture = get(book, chapter, "1")
    text = scripture["text"]
    text = getChapter(text, scripture, book, chapter)
    generateWordCloud(text)

GetWordCloudVerse(Alma, "2", "29")


