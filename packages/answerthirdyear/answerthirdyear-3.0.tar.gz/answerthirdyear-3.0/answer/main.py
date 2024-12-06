def nlp(num):
    if num == 1:
        print("""from nltk.corpus import brown
import nltk
nltk.download('brown')

print ('Total Categories:', len(brown.categories()))

print (brown.categories())

# tokenized sentences
brown.sents(categories='mystery')

# POS tagged sentences
brown.tagged_sents(categories='mystery')

# get sentences in natural form
sentences = brown.sents(categories='mystery')
print (sentences)


# get tagged words
tagged_words = brown.tagged_words(categories='mystery')
print (tagged_words)

# get nouns from tagged words
nouns = [(word, tag) for word, tag in tagged_words if any(noun_tag in tag for noun_tag in ['NP', 'NN'])]
# prints the first 10 nouns
print (nouns[0:10])

# build frequency distribution for nouns
nouns_freq = nltk.FreqDist([word for word, tag in nouns])
print (nouns_freq)

# print top 10 occurring nouns
print (nouns_freq.most_common(10))

# REUTERS CORPUS
from nltk.corpus import brown
import nltk
nltk.download('reuters')
print ('Total Categories:', len(reuters.categories()))
print (reuters.categories())

from nltk.corpus import wordnet as wn

word = 'hike' # taking hike as our word of interest

# get word synsets
word_synsets = wn.synsets(word)
print (word_synsets)

# get details for each synonym in synset
for synset in word_synsets:
    print ('Synset Name:', synset.name())
    print ('POS Tag:', synset.pos())
    print ('Definition:', synset.definition())
    print ('Examples:', synset.examples())""")
    elif num == 2:
        print("""simple_string = 'hello' + " I'm a simple string"
print (simple_string)
multi_line_string = \"\"\"Hello I'm
a multi-line
string!\"\"\"
multi_line_string
print (multi_line_string)
raw_string = r'D:\\2023-24 Even\\NLP Lab\file.txt'
print (raw_string)
print ('Hello' + ' and welcome ' + 'to AI!')
print ('Hello' ' and welcome ' 'to AI-ML!')
s1 = 'AI!'
print ('Hello ' + s1)
s2 = '--Machine Learning--'
s2 * 5
s1 + s2
print ((s1 + s2)*3)
s3 = ('This '
      'is another way '
      'to concatenate '
      'several strings!')
print (s3)
print ('way' in s3)
print ('python' in s3)
len(s3)
s = 'PYTHON'
for index, character in enumerate(s):
    print ('Character', character+':', 'has index:', index)
print (s[0], s[1], s[2], s[3], s[4], s[5])
print (s[-1], s[-2], s[-3], s[-4], s[-5], s[-6])
print (s[:])
print (s[1:4])
print (s[:3])
print (s[3:])
print (s[-3:])
print (s[:3] + s[3:])
print(s[:3] + s[-3:])
s = 'python is great'
print (s.capitalize())
print (s.upper())
print (s.replace('python', 'analytics'))
s = 'I,am,a,comma,separated,string'
print (s.split(','))
print (' '.join(s.split(',')))
s = '   I am surrounded by spaces    '
print (s)
print (s.strip())
s = 'this is in lower case'
print (s.title())
import re
print (re.findall(r'\w+', s))
s = u'H\u00e8llo'
s
print (s)
print (re.findall(r'\w+', s, re.UNICODE))
pattern = 'Python'
s1 = 'Python is an excellent language'
s2 = 'I love the Python language. I also use Python to build applications at work!'
print (re.match(pattern, s1))
pattern = 'python'
s1 = 'Python is an excellent language'
s2 = 'I love the Python language. I also use Python to build applications at work!'
print (re.match(pattern, s1))
print (re.match(pattern, s1, flags=re.IGNORECASE))
print (re.search(pattern, s2, re.IGNORECASE))
print (re.findall(pattern, s2, re.IGNORECASE))
print (re.sub(pattern, 'Java', s2, flags=re.IGNORECASE))
print (re.subn(pattern, 'Java', s2, flags=re.IGNORECASE))""")

    elif num == 3:
        print("""import nltk
nltk.download('gutenberg')
nltk.download('punkt')
from nltk.corpus import gutenberg
alice = gutenberg.raw(fileids='carroll-alice.txt')
sample_text = 'We will discuss briefly about the basic syntax,\
 structure and design philosophies. \
 There is a defined hierarchical syntax for Python code which you should remember \
 when writing code! Python is a really powerful programming language!'
print (len(alice))
print (alice[0:100])
default_st = nltk.sent_tokenize
alice_sentences = default_st(text=alice)
sample_sentences = default_st(text=sample_text)
print ('Total sentences in sample_text:', len(sample_sentences))
print (sample_sentences)
print ('\nTotal sentences in alice:', len(alice_sentences))
print(alice_sentences[0:5])
punkt_st = nltk.tokenize.PunktSentenceTokenizer()
sample_sentences = punkt_st.tokenize(sample_text)
print(sample_sentences)


SENTENCE_TOKENS_PATTERN = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<![A-Z]\.)(?<=\.|\?|\!)\s'
regex_st = nltk.tokenize.RegexpTokenizer(
            pattern=SENTENCE_TOKENS_PATTERN,
            gaps=True)
sample_sentences = regex_st.tokenize(sample_text)
print(sample_sentences)

# 3b. Word Tokenization
sentence = "The brown fox wasn't that quick and he couldn't win the race"
default_wt = nltk.word_tokenize
words = default_wt(sentence)
print (words)
treebank_wt = nltk.TreebankWordTokenizer()
words = treebank_wt.tokenize(sentence)
print (words)
TOKEN_PATTERN = r'\w+'
regex_wt = nltk.RegexpTokenizer(pattern=TOKEN_PATTERN,
                                gaps=False)
words = regex_wt.tokenize(sentence)
print (words)
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')
sentence = 'The brown fox is quick and he is jumping over the lazy dog'
tokens = nltk.word_tokenize(sentence)
tagged_sent = nltk.pos_tag(tokens, tagset='universal')
print (tagged_sent)
""")
    elif num == 4:
        print("""CORPUS = [
'the sky is blue',
'sky is blue and sky is beautiful',
'the beautiful sky is so blue',
'i love blue cheese'
]
new_doc = ['loving this blue sky today']
pip install scikit-learn
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
vectorizer
CORPUS = [
'the sky is blue',
'sky is blue and sky is beautiful',
'the beautiful sky is so blue',
'love blue cheese'
]
X = vectorizer.fit_transform(CORPUS)
X
vocabulary=vectorizer.get_feature_names_out()
print (vocabulary)
X.toarray()
vectorizer.vocabulary_.get('beautiful')
bigram_vectorizer = CountVectorizer(ngram_range=(1, 2))
analyze = bigram_vectorizer.build_analyzer()
analyze('the sky is blue')
X1= bigram_vectorizer.fit_transform(CORPUS).toarray()
X1
feature_index = bigram_vectorizer.vocabulary_.get('is blue')
feature_index
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
pipe = Pipeline([('count', CountVectorizer(vocabulary=vocabulary)),('tfid', TfidfTransformer())]).fit(CORPUS)
pipe['count'].transform(CORPUS).toarray()
pipe['tfid'].idf_
from sklearn.feature_extraction.text import TfidfVectorizer
corpus = [
     'This is the first document.',
     'This document is the second document.',
     'And this is the third one.',
     'Is this the first document?',
 ]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)
print (X)
print (vectorizer.get_feature_names_out())
print(X.shape)""")

    elif num == 5:
        print("""import pandas as pd
data = pd.read_csv('https://raw.githubusercontent.com/mohitgupta-omg/Kaggle-SMS-Spam-Collection-Dataset-/master/spam.csv', encoding='latin-1')
data.head()

data.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
data.columns = ['label', 'text']
data.head()

data.isna().sum()

data.shape

data['label'].value_counts(normalize = True).plot.bar()

import nltk
nltk.download('all')
text = list(data['text'])
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
corpus = []
for i in range(len(text)):
    r = re.sub('[^a-zA-Z]', ' ', text[i])
    r = r.lower()
    r = r.split()
    r = [word for word in r if word not in stopwords.words('english')]
    r = [lemmatizer.lemmatize(word) for word in r]
    r = ' '.join(r)
    corpus.append(r)
data['text'] = corpus
data.head()

X = data['text']
y = data['label']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=123)
print('Training Data :', X_train.shape)
print('Testing Data : ', X_test.shape)

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X_train_cv = cv.fit_transform(X_train)
X_train_cv.shape

from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(X_train_cv, y_train)
X_test_cv = cv.transform(X_test)
predictions = lr.predict(X_test_cv)
predictions

import pandas as pd
from sklearn import metrics
df = pd.DataFrame(metrics.confusion_matrix(y_test,predictions), index=['ham','spam'], columns=['ham','spam'])
df""")
    elif num == 6:
        print("""import pandas as pd
data = pd.read_csv('/content/Tweets.csv', encoding='latin-1')
data.head()

data.drop(['tweet_id', 'airline_sentiment_confidence', 'negativereason','negativereason_confidence','airline','airline_sentiment_gold','name','negativereason_gold','retweet_count','tweet_coord','tweet_created','tweet_location','user_timezone'], axis=1, inplace=True)
data.columns = ['airline_sentiment', 'text']
data.head()

data.isna().sum()

data.shape

data['airline_sentiment'].value_counts(normalize = True).plot.bar()

import nltk
nltk.download('all')
text = list(data['text'])
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
corpus = []
for i in range(len(text)):
    r = re.sub('[^a-zA-Z]', ' ', text[i])
    r = r.lower()
    r = r.split()
    r = [word for word in r if word not in stopwords.words('english')]
    r = [lemmatizer.lemmatize(word) for word in r]
    r = ' '.join(r)
    corpus.append(r)
data['text'] = corpus
data.head()

X = data['text']
y = data['airline_sentiment']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=123)
print('Training Data :', X_train.shape)
print('Testing Data : ', X_test.shape)
print('Training Label:',y_train.shape)
print('Test Label:',y_test.shape)

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X_train_cv = cv.fit_transform(X_train)
X_train_cv.shape

from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(X_train_cv, y_train)

X_test_cv = cv.transform(X_test)
predictions = lr.predict(X_test_cv)
predictions

import pandas as pd
from sklearn import metrics
df =pd.DataFrame(metrics.confusion_matrix(y_test,predictions),index=['neutral','positive','negative'], columns=['neutral','positive','negative'])
df

from sklearn.metrics import classification_report, confusion_matrix
print(classification_report(y_test, predictions, target_names=['neutral','positive','negative']))
print(confusion_matrix(y_test, predictions))

X_test_cv = cv.transform(X_test)
predictions = lr.predict(X_test_cv)
predictions

import pandas as pd
from sklearn import metrics
df = pd.DataFrame(metrics.confusion_matrix(y_test,predictions),index=['neutral','positive','negative'], columns=['neutral','positive','negative'])
df""")

    elif num == 7:
        print("""from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
text = \"\"\"he Elder Scrolls V: Skyrim is an open world action role-playing video game
developed by Bethesda Game Studios and published by Bethesda Softworks.
It is the fifth installment in The Elder Scrolls series, following
The Elder Scrolls IV: Oblivion. Skyrim's main story revolves around
the player character and their effort to defeat Alduin the World-Eater,
a dragon who is prophesied to destroy the world.
The game is set two hundred years after the events of Oblivion
and takes place in the fictional province of Skyrim. The player completes quests
and develops the character by improving skills.
Skyrim continues the open world tradition of its predecessors by allowing the
player to travel anywhere in the game world at any time, and to
ignore or postpone the main storyline indefinitely. The player may freely roam
over the land of Skyrim, which is an open world environment consisting
of wilderness expanses, dungeons, cities, towns, fortresses and villages.
Players may navigate the game world more quickly by riding horses,
or by utilizing a fast-travel system which allows them to warp to previously
Players have the option to develop their character. At the beginning of the game,
players create their character by selecting one of several races,
including humans, orcs, elves and anthropomorphic cat or lizard-like creatures,
and then customizing their character's appearance.discovered locations. Over the
course of the game, players improve their character's skills, which are numerical
representations of their ability in certain areas. There are eighteen skills
divided evenly among the three schools of combat, magic, and stealth.
Skyrim is the first entry in The Elder Scrolls to include Dragons in the game's
wilderness. Like other creatures, Dragons are generated randomly in the world
and will engage in combat.\"\"\"

import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Tokenizing the text
stopWords = set(stopwords.words("english"))
words = word_tokenize(text)

# Creating a frequency table to keep the score of each word

freqTable = dict()
for word in words:
    word = word.lower()
    if word in stopWords:
        continue
    if word in freqTable:
        freqTable[word] += 1
    else:
        freqTable[word] = 1
# Creating a dictionary to keep the score of each sentence
sentences = sent_tokenize(text)
sentenceValue = dict()

for sentence in sentences:
    for word, freq in freqTable.items():
        if word in sentence.lower():
            if sentence in sentenceValue:
                sentenceValue[sentence] += freq
            else:
                sentenceValue[sentence] = freq
sumValues = 0
for sentence in sentenceValue:
    sumValues += sentenceValue[sentence]

# Average value of a sentence from the original text

average = int(sumValues / len(sentenceValue))

# Storing sentences into our summary.
summary = ''
for sentence in sentences:
    if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
        summary += " " + sentence
print(summary)""")
    elif num == 8:
        print("""import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
doc1 = "Sugar is bad to consume. My sister likes to have sugar, but not my father."
doc2 = "My father spends a lot of time driving my sister around to dance practice."
doc3 = "Doctors suggest that driving may cause increased stress and blood pressure."
doc4 = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
doc5 = "Health experts say that Sugar is not good for your lifestyle."
doc_complete = [doc1, doc2, doc3, doc4, doc5]
print('\n\nData\n\n')
print(doc_complete)
stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized
doc_clean = [clean(doc).split() for doc in doc_complete]
print('\n\nCleaned Data\n\n')
print(doc_clean)

import gensim
from gensim import corpora
dictionary = corpora.Dictionary(doc_clean)

doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
Lda = gensim.models.ldamodel.LdaModel

ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=50)
print(ldamodel.print_topics(num_topics=3, num_words=3))
""")
    elif num == 9:
        print("""def jaccard_similarity(x,y):
  \"\"\" returns the jaccard similarity between two lists \"\"\"
  intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
  union_cardinality = len(set.union(*[set(x), set(y)]))
  return intersection_cardinality/float(union_cardinality)
sentences = ["The bottle is empty",
"There is nothing in the bottle"]
sentences = [sent.lower().split(" ")
for sent in sentences]
jaccard_similarity(sentences[0], sentences[1])
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
X ="I love horror movies"
Y ="Lights out is a horror movie"
X_list = word_tokenize(X)
Y_list = word_tokenize(Y)
sw = stopwords.words('english')
l1 =[];l2 =[]
X_set = {w for w in X_list if not w in sw}
Y_set = {w for w in Y_list if not w in sw}
rvector = X_set.union(Y_set)
for w in rvector:
    if w in X_set: l1.append(1)
    else: l1.append(0)
    if w in Y_set: l2.append(1)
    else: l2.append(0)
c = 0
for i in range(len(rvector)):
        c+= l1[i]*l2[i]
cosine = c / float((sum(l1)*sum(l2))**0.5)
print("similarity: ", cosine)""")