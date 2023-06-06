
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import requests
import json


app = FastAPI()



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
Helaman = "helaman"
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
def generateWordCloud(text, title):
    wordcloud = WordCloud( max_words=100, background_color="white").generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    #plt.show()
    outputFile = "output/" + title + ".png"
    wordcloud.to_file(outputFile)
def GetWordCloudVerse(book, chapter, verse):
    scripture = get(book, chapter, verse)
    text = scripture["text"]
    title = book + chapter + "_" + verse
    generateWordCloud(text, title)

def GetWordCloudBook(book):
    scripture = get(book, "1", "1")
    text = scripture["text"]
    text = getBook(text, scripture, book)
    generateWordCloud(text, book)


def GetWordCloudChapter(book, chapter):
    scripture = get(book, chapter, "1")
    text = scripture["text"]
    text = getChapter(text, scripture, book, chapter)
    title = book + chapter
    generateWordCloud(text, title)

#GetWordCloudBook(Alma)

def ConsoleProgram():
    print("My program can give you a word cloud of a single verse, a chapter, or a whole book of the Book of Mormon")
    choice = input("What would you like to do? Input 1 for a verse, 2 for a chapter, and 3 for a book: ")
    if choice == "1":
        book = input("Which book: ")
        chapter = input("Which chapter: ")
        verse = input("Which verse: ")
        GetWordCloudVerse(book, chapter, verse)
    if choice == "2":
        book = input("Which book: ")
        chapter = input("Which chapter: ")
        GetWordCloudChapter(book, chapter)
    else:
        book = input("Which book: ")
        GetWordCloudBook(book)


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/wordcloud")
async def get_word_cloud(book: str, chapter: str, verse: str):
    # Call the function to generate the word cloud
    GetWordCloudVerse(book, chapter, verse)

    # Return the word cloud image file
    return FileResponse("output/{}{}_{}.png".format(book, chapter, verse))

@app.get("/wordcloud2")
async def get_word_cloud(book: str, chapter: str):
    # Call the function to generate the word cloud
    GetWordCloudChapter(book, chapter)

    # Return the word cloud image file
    return FileResponse("output/{}{}.png".format(book, chapter))

@app.get("/wordcloud1")
async def get_word_cloud(book: str):
    # Call the function to generate the word cloud
    GetWordCloudBook(book)

    # Return the word cloud image file
    return FileResponse("output/{}.png".format(book))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
