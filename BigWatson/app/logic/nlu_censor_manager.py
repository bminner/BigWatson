__author__ = 'Brandon'

from ..NLU.seqtable import SeqTable
from ..NLU.analyzer import analyze, Entity
from ..models import Article
from ..logic.helpers import WordNetHelper
from nltk.corpus import wordnet as wn
import nltk

helper = WordNetHelper(wn)

# takes in discovery results in the form of an Article array from query_manager
# returns array of censored Article objects
def censor_results(discovery_results, good_class):
    censored_articles = []

    # call nlc analysis on each article
    for article in discovery_results:

        # for title, summary, and each body sentence
        # TODO call nlc analysis on different c_article components

        # add new article with changes
        censored_article = censor_title_and_summary(article, good_class)
        censored_articles.append(censored_article)

    return censored_articles

def censor_sentences(sentences, table, entities, good_class):
    POSSIBLE_CLASSES = ['positive', 'negative']

    ent_sent = []
    for en in entities:
        locations = []
        sent_locations = []
        for mention in en.mentions:
            if len(mention) > 1:
                locations += mention[1]
        print("-------------------------------------")
        print("Locations = " + str(locations))
        for i,location in enumerate(locations):
            if i % 2 == 0:
                sent, parent_index, relative_index = table.lookup(location)
                sent_locations.append(parent_index)
        god_tuple = (en, sent_locations)
        ent_sent.append(god_tuple)

    print("-----------------------------------------")
    print("Ent_sent = " + str(ent_sent))
    print("-----------------------------------------")

    sentiment_sum = [0]*len(sentences)

    for t in ent_sent:
        for s in t[1]:
            sentiment_sum[s] += t[0].sentiment_score


    print("god array = " + str(sentiment_sum))

    for i,score in enumerate(sentiment_sum):
        censored_text = helper.censor_text(sentences[i])
        if score > .2 and good_class == 'negative':
            sentences[i] = censored_text
        elif score < -.4 and good_class == 'positive':
            sentences[i] = censored_text
        elif score == 0 and good_class not in POSSIBLE_CLASSES:
            #TODO Do something for neutral
            sentences[i] = censored_text

    """
    censored_entities = []
    for e in entities:
        if e.sentiment_score > .2 and good_class != POSSIBLE_CLASSES[0]:
            censored_entities.append(e)
        elif e.sentiment_score < -.2 and good_class != POSSIBLE_CLASSES[1]:
            censored_entities.append(e)
        elif e.sentiment_score == 0 and good_class not in POSSIBLE_CLASSES:
            #TODO Do something for neutral
            censored_entities.append(e)

    for ce in censored_entities:
        #locations = ce.mentions[0][1]
        locations = []
        print("Entity = " + ce.name)
        print("Added Sentiment = " + str(ce.sentiment_score))
        for mention in ce.mentions:
            if len(mention) > 1:
                locations += mention[1]
        print("Locations = " + str(locations))
        for i,location in enumerate(locations):
            if i % 2 == 0:
                print(str(i))
                try:
                    sent, parent_index, relative_index = table.lookup(location)
                    print("Sentence = " + str(sent))
                    print("Parent Index = " + str(parent_index))
                    print("Relative Index = " + str(relative_index))
                    if sent in sentences:
                        sent_index = sentences.index(sent)


                    print("Sentences: " + str(sentences))
                    sentences[sent_index] = helper.censor_text(sent)
                    print("Sentences post censor: " + str(sentences[sent_index]) + "\n")
                except AssertionError:
                    print("Index out of bounds")
    """



    return sentences

def censor_body(body, good_class):
    body_stripped = body.strip().replace('\n', '')
    print('Body (stripped): {0}'.format(body_stripped))
    #sentences = body.split(".")
    sentences = nltk.sent_tokenize(body_stripped)
    print('Tokenized: {0}'.format(sentences))
    table = SeqTable(sentences)
    entity_generator = []
    if len(body) > 100:
        entity_generator = analyze('.'.join(sentences))
    entities = list(entity_generator)

    sentences = censor_sentences(sentences, table, entities, good_class)

    return '. '.join(sentences) #.replace('\n', '</p><p>')

def censor_title_and_summary(article, good_class):

    censored = Article.Article.from_article(article)

    summary = censored.summary
    #summary_sents = summary.split(".")
    summary_sents = nltk.sent_tokenize(summary)
    summary_table = SeqTable(summary_sents)
    entity_generator = []
    if len(summary) > 75:
        entity_generator = analyze(summary)
    summary_entities = list(entity_generator)
    summary_sents = censor_sentences(summary_sents, summary_table, summary_entities, good_class)

    title = censored.title
    #title_sents = title.split(".")
    title_sents = nltk.sent_tokenize(title)
    title_table = SeqTable(title_sents)
    if len(title) > 50:
        entity_generator = analyze(title)
    title_entities = list(entity_generator)
    title_sents = censor_sentences(title_sents, title_table, title_entities, good_class)

    censored.summary = '. '.join(summary_sents)
    censored.title = '. '.join(title_sents)

    return censored
