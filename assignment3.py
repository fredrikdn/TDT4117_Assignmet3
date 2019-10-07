import random
import codecs
import gensim
import nltk

file = "/Users/Fredrik/Documents/Skole/H19/TDT4117/TDT4117_Assignmet3/pg3300.txt"
solution = "/Users/Fredrik/Documents/Skole/H19/TDT4117/TDT4117_Assignmet3/solutions.txt"

# Task 1.0
random.seed(123)

# Task 1.1
def openFile(file):
    return codecs.open(file, "r", "utf-8")

# Task 1.2
def paragraph_splitter(file):
    fil = openFile(file)
    paragraphs = []
    paragraph = ""
    for line in fil.readlines():
        paragraph += line
        if line.isspace():
            if line != "":
                paragraphs.append("[Paragraph: {}]\n{}".format(line, paragraph))
            paragraph = ""
            continue
    return paragraphs

# Task 1.3
def gutenbergRemover(word):
    paragraphs = paragraph_splitter(file)
    paraList = []
    for p in paragraphs:
        if word.casefold() not in p.casefold():
            paraList.append(p)
    print(paraList)
    return paraList

# Task 1.4


# Task 1 - solutions

# Task 1.2
paragrafListe = paragraph_splitter(file)

# Task 1.3
gutenbergRemover("Gutenberg")

# Task 1.4
