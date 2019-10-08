import random
import codecs
import gensim
import nltk
import string
from nltk.stem.porter import PorterStemmer


file = "/Users/Fredrik/Documents/Skole/H19/TDT4117/TDT4117_Assignmet3/pg3300.txt"
solution = "/Users/Fredrik/Documents/Skole/H19/TDT4117/TDT4117_Assignmet3/solutions.txt"

# Task 1.0
stemmer = PorterStemmer()
random.seed(123)

# Task 1.1
def openFile(file):
    return codecs.open(file, "r", "utf-8")

# Task 1.2
def paragraphSplitter(file):
    fil = openFile(file)
    paragraphs = []
    paragraph = ""
    for line in fil.readlines():
        paragraph += line
        if line.isspace():
            if line != "":
                paragraphs.append(paragraph)
            paragraph = ""
            continue
    return paragraphs

# Task 1.3
def wordRemover(paragraphs, word):
    paraList = []
    for p in paragraphs:
        if word.casefold() not in p.casefold():
            paraList.append(p)
    return paraList

# Task 1.4
def tokenizeParagraphs(paragraphs):
    for i, p in enumerate(paragraphs):
        paragraphs[i] = p.split(" ")
    return paragraphs

# Task 1.5
def lower(paragraphs):
    for p in paragraphs:
        for w in p:
            p.append(w.lower())
    return paragraphs

def removePunctuation(words):
    cword = []
    for word in words:
        w = ""
        for letter in word:
            if(string.punctuation + "\n\r\t").__contains__(letter):
                if w != "":
                    cword.append(w)
                    w = ""
                continue
            w += letter
        if w != "":
            cword.append(w)
    return cword

def getParagraphs(paragraphs):
    for i, words in enumerate(paragraphs):
        words = removePunctuation(words)
        paragraphs[i] = words
    return paragraphs

# Task 1.6
def stemWords(paragraphs):
    stemmedP = []
    for p in paragraphs:
        stemmedW = []
        for w in p:
            stemmed.append(stemmer.stem(w).lower())
    return paragraphs

# Task 1.7

# Task 1 - solutions

textFile = paragraphSplitter(file)
paragraphList = wordRemover(textFile, "Gutenberg")
paragraphList = tokenizeParagraphs(paragraphList)
paragraphList = lower(paragraphList)


print(paragraphList[1])

