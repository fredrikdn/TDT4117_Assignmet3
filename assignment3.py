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

# remove punctuation of all words in each doc the corpus


def remove_punctuation(paragraphs):
    paras = []
    # goes through each word in the paragraph and removes whitespace, etc.
    for p in paragraphs:
        words = remove_punctuation_word(p)
        paras.append(words)
    return paras

# aiding function to remove the punctuation of each paragraph

punc = list(string.punctuation)
punc.append('\r\n')


def remove_punctuation_word(paragraph):
    words = []
    for word in paragraph:
        temp = replace_multiple(word, punc, ' ')
        templist = temp.split(' ')
        for i in templist:
            if i == '':
                continue
            else:
                words.append(i)
    return words


# aiding function to remove multiple chars


def replace_multiple(w, toBeRemoved, r):
    for elem in toBeRemoved:
        if elem in w:
            w = w.replace(elem, r)
    return w

# Task 1.6

# stem paragraphs


def stem(paragraphs):
    stemmed_paras = []
    # for each paragraph, stem each word in the paragraph
    for p in paragraphs:
        stemmed_words = stem_word(p)
        stemmed_paras.append(stemmed_words)
    return stemmed_paras

# stem each word in paragraph


def stem_word(p):
    stemmed_words = []
    for word in p:
        stemmed_words.append(stemmer.stem(word).lower())
    return stemmed_words

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
split = paragraph_splitter(tex_file)
noGuten = word_remover(split, "Gutenberg")
tokenizedParas = tokenize_paragraphs(noGuten)
lowered = lower(tokenizedParas)
remParas = remove_punctuation(lowered)
stemParas = stem(remParas)
print("Printout of the stemmed paragraphs (example):\n")
print("{},{}".format(stemParas[14],stemParas[37]))



# runs the word_frequency-function with the given word on the documents
w = "consumer"
c = word_frequency(remParas, w)
print("Word Frequency ({}): {}".format(w,c))


# #### TASK 2 ####


# stop words extracted from common-english-words.txt
stopwords = 'a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,' \
             'cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,' \
             'how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,' \
             'not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,' \
             'their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,' \
             'who,whom,why,will,with,would,yet,you,your'

stopword_list = stopwords.split(',')

# Building a dictionary based on the corpus from Task 1
dictionary = gensim.corpora.Dictionary(stemParas)

# Finds the ids for the stopwords from the dictionary


def stopword_ids(stopwords, dictionary):
    ids = []
    for word in stopwords:
        try:
            ids.append(dictionary.token2id[word])
        except:
            pass
    return ids


# list of the ids
stopword_ids = stopword_ids(stopword_list, dictionary)

# filter out the "bad ids" from the dictionary
dictionary.filter_tokens(stopword_ids)

# runs through each document(paragraph) of the corpus and adds the given words to the BoW
def to_bow(paragraphs):
    bow = []
    for p in paragraphs:
        bow.append(dictionary.doc2bow(p))
    return bow

bow = to_bow(stemParas)
#print(bow)


# #### TASK 3 ####


# Task 3.1, 3.2, 3.3
# the TF-IDF model based on BoW
tfidf_model = gensim.models.TfidfModel(bow)

# the BoW on the following format for each word: (index, weight)
tfidf_corpus = tfidf_model[bow]

# matrix similarity of the corpus
matrix_sim = gensim.similarities.MatrixSimilarity(tfidf_corpus)

# Task 3.4
# this will group documents and words, based on their tf-idf-weight, together into topics (serializing)
lsi_model = gensim.models.LsiModel(tfidf_corpus, id2word=dictionary, num_topics=100)
lsi_corpus = lsi_model[bow]
lsi_matrix = gensim.similarities.MatrixSimilarity(lsi_corpus)

# Task 3.5
# printing the first three topics
topic1 = lsi_model.show_topic(1)
topic2 = lsi_model.show_topic(2)
topic3 = lsi_model.show_topic(3)
print("\n\nTOPICS: ", "\n")
print(topic1)
print(topic2)
print(topic3, "\n")

print("The three topics are related in the way that they are structured such that\n"
      "each cluster of docs and similar words in the occurence matrix represents the topics."
      "\nEach topic includes the most important words in defining the topic in the output, "
      "\nalong with their contribution to the topic.\n")


# #### TASK 4 ####

# pre-processing of the query

def preprocessing(query):
    query = query.lower()
    query = query.split()
    query = remove_punctuation_word(query)
    query = stem_word(query)
    return query

# Task 4.1
#preprocessing of the query
q = "How taxes influence Economics?"
query = preprocessing(q)
query = dictionary.doc2bow(query)
#print(query)

# Task 4.2
# BoW to TF-IDF
tfidf_index = tfidf_model[query]

# This function will structure the output (tf-idf) the way it is described in the assignment
def bow_to_tfidf(index, dictionary):
    list=[]
    for word in index:
        word_index = word[0]
        word_weight = word[1]
        str = "index: {} , word: {} , weight: {}".format(word_index, dictionary.get(word_index, word_weight), word_weight)
        list.append(str)
    return list


tf_form = bow_to_tfidf(tfidf_index, dictionary)
print("TF-IDF representation of the query: \n{}\n".format(tf_form))

# Task 4.3

# helper to split into readable paragraphs (list of all docs)


docsim = enumerate(matrix_sim[tfidf_index])
# sorting the docs
top_res = sorted(docsim, key=lambda x: x[1], reverse=True)[:3]

# return the top 3 most relevant docs
print("The top 3 most relevant documents:")
for res in top_res:
    doc = noGuten[res[0]]
    print("\n[Document: {}]".format(res[0]))
    for line in range(5):
        try:
            print(doc[line])
        except:
            pass


# Task 4.4

# Finds the 3 most significant topics
lsi_query = lsi_model[tfidf_index]
topic_sort = sorted(lsi_query, key=lambda x: -abs(x[1]))[:3]
print("\nThe top 3 topics with most significant weight:\n")
for topic in enumerate(topic_sort):
    t = topic[1][0]
    print("[Topic {}]".format(t))
    print(lsi_model.show_topics()[t])

