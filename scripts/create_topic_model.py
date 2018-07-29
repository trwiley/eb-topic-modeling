# create_topic_model.py
# purpose: create a topic model from a text file.

# import in the English parser from spacy, a natural language processing toolkit.
import spacy 
spacy.load('en')
from spacy.lang.en import English
parser = English()

# tokenize: clean texts and return a list of tokens.
def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

# wordnet is used to find the meanings of words, synonyms, antonyms, etc.
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn

def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

# get the root word
from nltk.stem.wordnet import WordNetLemmatizer
def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

# filter out stop words
nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))

# prepare the text for topic modeling
def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

import random
text_data = []
with open('eb_script_clean.txt') as f:
    for line in f:
        tokens = prepare_text_for_lda(line)
        if random.random() > .99:
            #print(tokens)
            text_data.append(tokens)

#create a dictionary from the data
from gensim import corpora
dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]
# create bag-of-words
import pickle
pickle.dump(corpus, open('corpus.pk1', 'wb'))

# save the dictionary
dictionary.save('dictionary.gensim')

# find 5 topics in the data
import gensim
NUM_TOPICS = 5
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word = dictionary, passes=15)
ldamodel.save('model5.gensim')
topics = ldamodel.print_topics(num_words=4)
for topic in topics:
    print(topic)

# visualizing 5 topics with pyLDAvis
dictionary = gensim.corpora.Dictionary.load('dictionary.gensim')
corpus = pickle.load(open('corpus.pk1', 'rb'))
lda = gensim.models.ldamodel.LdaModel.load('model5.gensim')

import pyLDAvis.gensim
lda_display = pyLDAvis.gensim.prepare(lda, corpus, dictionary, sort_topics=False)
pyLDAvis.save_html(lda_display, "topic_mod.html")