import random
import codecs
import gensim
import nltk
import string
from nltk.stem.porter import PorterStemmer
from nltk.probability import FreqDist


tex_file = "/Users/Fredrik/Documents/Skole/H19/TDT4117/TDT4117_Assignmet3/pg3300.txt"

# #### TASK 1 ####


# Task 1.0
stemmer = PorterStemmer()
random.seed(123)
fdist = FreqDist()

# Task 1.1


def open_file(file):
    return codecs.open(file, "r", "utf-8")

# Task 1.2

# splits each paragraph into separate "documents"


def paragraph_splitter(file):
    fil = open_file(file)
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


def word_remover(paragraphs, word):
    paraList = []
    for p in paragraphs:
        if word.casefold() not in p.casefold():
            paraList.append(p)
    return paraList

# Task 1.4

# each paragraph is tokenized on " "


def tokenize_paragraphs(paragraphs):
    for i, p in enumerate(paragraphs):
        paragraphs[i] = p.split(" ")
    return paragraphs

# Task 1.5

# each word in the corpus is lower-cased


def lower(paragraphs):
    paras_lowered = []
    for p in paragraphs:
        word_lowered = []
        for w in p:
            word_lowered.append(w.lower())
        paras_lowered.append(word_lowered)
    return paras_lowered


def remove_punctuation(paragraphs):
    paras = []
    # goes through each word in the paragraph and removes whitespace, etc.
    for p in paragraphs:
        words = []
        for word in p:
            temp = replace_multiple(word, ['.', ',', ';', ':', '\r\n'], ' ')
            templist = temp.split(' ')
            for i in templist:
                if i == '':
                    continue
                else:
                    words.append(i)
        paras.append(words)
    return paras

# aiding function to remove multiple chars


def replace_multiple(w, toBeRemoved, r):
    for elem in toBeRemoved:
        if elem in w:
            w = w.replace(elem, r)
    return w

# Task 1.6


def stem(paragraphs):
    stemmed_paras = []
    # for each paragraph, stem each word in the paragraph
    for p in paragraphs:
        stemmed_words = []
        for word in p:
            stemmed_words.append(stemmer.stem(word).lower())
        stemmed_paras.append(stemmed_words)
    return stemmed_paras

# Task 1.7


def word_frequency(paragraphs, word):
    # searching the word in question and counts it
    # word = stemmer.stem(word)
    for p in paragraphs:
        for w in p:
            if w == word:
                fdist[w] += 1
    return fdist


# Task 1 - structure and edit corpus
paragraphs = paragraph_splitter(tex_file)
noGuten = word_remover(paragraphs, "Gutenberg")
tokenizedParas = tokenize_paragraphs(noGuten)
lowered = lower(tokenizedParas)
remParas = remove_punctuation(lowered)
stemParas = stem(remParas)


# runs the word_frequency-function on the documents before stemming
c = word_frequency(remParas, "consumer")
print("Word Frequency: {}".format(c))

# runs the word_frequency-function on the documents after stemming
d = word_frequency(stemParas, "consumer")
print("Word Frequency: {}".format(d))

# ==> works both before and after stemming


# #### TASK 2 ####


# creating the dictionary with the edited list of paragraphs
dictionary = gensim.corpora.Dictionary(stemParas)
#print(dictionary)

# stopwords_file
stopwords_file = "/Users/Fredrik/Documents/Skole/H19/TDT4117/TDT4117_Assignmet3/common-english-words.txt"

# creating a list of stopwords from the attached file:


def stopword_list(stopwords_file):
    stopwordList = []
    fil = open_file(stopwords_file)
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

# converting the paragraphlist(corpus) to bag-of-words:


def convert_bow(paragraphs):
    for p in paragraphs:
        bags.append(dictionary.doc2bow(p))


# bag of words
bags = []

# the stopword-list
stopwords = stopword_list(stopwords_file)
#print(stopwords)

# getting the list of stopword IDs
stopword_ids = stopword_id(stopwords, dictionary)

# filter out stopwords from the dictionary
dictionary.filter_tokens(stopword_ids)

# converted to BoW
convert_bow(stemParas)
print(bags)


# #### TASK 3 ####


# Task 3.1, 3.2, 3.3
# the TF-IDF model based on BoW
tfidf_model = gensim.models.TfidfModel(bags)

# the BoW on the following format for each word: (index, weight)
tfidf_corpus = tfidf_model[bags]

# matrix similarity of the corpus
matrix_sim = gensim.similarities.MatrixSimilarity(tfidf_corpus)

# Task 3.4
# this will group documents and words, based on their tf-idf-weight, together into topics (serializing)
lsi_model = gensim.models.LsiModel(tfidf_corpus, id2word=dictionary, num_topics=100)
lsi_corpus = lsi_model[bags]
lsi_matrix = gensim.similarities.MatrixSimilarity(lsi_corpus)

# Task 3.5
# printing the first three topics
topic1 = lsi_model.show_topic(1)
topic2 = lsi_model.show_topic(2)
topic3 = lsi_model.show_topic(3)
print(topic1)
print("\n")
print(topic2)
print("\n")
print(topic3)

# The three topics are related in the way that they are all about economy
# one possible division between the three can be:
#   - topic1: content about the workforce and production value/cost
#   - topic2: content about the specific produce(what is produced), the quantity and value/price
#   - topic3: content about trade/tax and foreign affairs
# Each topic includes the most important words in defining the topic are included
# in the output, along with their contribution to the topic


# #### TASK 4 ####

# Task 4.1

queries = []


