import random
import codecs
import gensim
import nltk
import string
from nltk.stem.porter import PorterStemmer
from nltk.probability import FreqDist
import re


tex_file = "/Users/Fredrik/Documents/Skole/H19/TDT4117/TDT4117_Assignmet3/pg3300.txt"
solution = "/Users/Fredrik/Documents/Skole/H19/TDT4117/TDT4117_Assignmet3/solutions.txt"

# #### Task 1 ####

# Task 1.0
stemmer = PorterStemmer()
random.seed(123)
fdist = FreqDist()

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
    paras_lowered = []
    for p in paragraphs:
        word_lowered = []
        for w in p:
            word_lowered.append(w.lower())
        paras_lowered.append(word_lowered)
    return paras_lowered


def removePunctuation(paragraphs):
    paras = []
    #goes through each word in the paragraph and removes whitespace, etc.
    for p in paragraphs:
        words = []
        for word in p:
            temp = replaceMultiple(word, ['.',',',';',':','\r\n'], ' ')
            templist = temp.split(' ')
            for i in templist:
                if i == '':
                    continue
                else:
                    words.append(i)
        paras.append(words)
    return paras

# aiding function to remove multiple chars


def replaceMultiple(w, toBeRemoved, r):
    for elem in toBeRemoved:
        if elem in w:
            w = w.replace(elem, r)
    return w

# Task 1.6


def stem(paragraphs):
    stemmed_paras = []
    #for each paragraph, stem each word in the paragraph
    for p in paragraphs:
        stemmed_words = []
        for word in p:
            stemmed_words.append(stemmer.stem(word).lower())
        stemmed_paras.append(stemmed_words)
    return stemmed_paras

# Task 1.7


def wordFrequency(paragraphs, word):
    #searching the word in question
    #word = stemmer.stem(word)
    for p in paragraphs:
        for w in p:
            if w == word:
                fdist[w] += 1
    return fdist


# Task 1 - run
paragraphs = paragraphSplitter(tex_file)
paragraphList = wordRemover(paragraphs, "Gutenberg")
tokenizedParas = tokenizeParagraphs(paragraphList)
paragraphList = lower(tokenizedParas)
remParas = removePunctuation(paragraphList)
paragraphList = stem(remParas)

#print(paragraphList[1800])
c = wordFrequency(remParas, "consumer")
print(c)

# #### Task 2 ####

# creating the dictionary with the edited list of paragraphs
dictionary = gensim.corpora.Dictionary(paragraphList)
print(dictionary)

# stopwords_file
stopwords_file = "/Users/Fredrik/Documents/Skole/H19/TDT4117/TDT4117_Assignmet3/common-english-words.txt"

# creating a list of stopwords from the attached file:


def stopwordList(stopwords_file):
    stopwordList = []
    fil = openFile(stopwords_file)
    stopwords_read = fil.read()
    stopwordList = stopwords_read.split(',')
    return stopwordList

# finding the ids for the stopwords in the dictionary:


def stopword_id(stopwords, dictionary):
    ids = []
    for word in stopwords:
        try:
            ids.append(dictionary.tokend2id[word])
        except:
            pass
    return ids

# converting the paragraphlist to bag-of-words:


def convert_bow(paragraphs):
    for p in paragraphs:
        bags.append(dictionary.doc2bow(p))


# bag of words
bags = []

# the stopword-list
stopwords = stopwordList(stopwords_file)
print(stopwords)

# getting the list of stopword IDs
stopword_ids = stopword_id(stopwords, dictionary)

# filter out stopwords from the dictionary
dictionary.filter_tokens(stopword_ids)

# converted to BoW
b_o_w = convert_bow(paragraphList)
print(bags)