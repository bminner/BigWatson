__author__ = 'Brandon'

from ..NLU.seqtable import SeqTable
from ..NLU.analyzer import analyze, Entity
from ..models import Article
import nltk

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

    censored_entities = []
    for e in entities:
        if e.sentiment_score > 0 and good_class != POSSIBLE_CLASSES[0]:
            censored_entities.append(e)
        elif e.sentiment_score < 0 and good_class != POSSIBLE_CLASSES[1]:
            censored_entities.append(e)
        elif e.sentiment_score == 0 and good_class not in POSSIBLE_CLASSES:
            #TODO Do something for neutral
            censored_entities.append(e)

    for ce in censored_entities:
        #locations = ce.mentions[0][1]
        locations = []
        print("Entity = " + ce.name)
        print("Sentiment = " + ce.sentiment_score)
        print("\nMentions = " + str(ce.mentions))
        for mention in ce.mentions:
            if len(mention) > 1:
                locations += mention[1]
        print("Locations = " + str(locations))
        for i,location in enumerate(locations):
            if i % 2 == 0:
                print(str(i))
                sent, parent_index, relative_index = table.lookup(location)
                print("Sentence = " + str(sent))
                if sent in sentences:
                    sent_index = sentences.index(sent)
                #TODO Censor by specific word using Kurt's stuff
                #censor_words(sentences[sent_index]) 
                print("Sentences: " + str(sentences))
                sentences[sent_index] = '<del>' + sent + '</del>'
                print("Sentences post censor: " + str(sentences) + "\n")
    
    return sentences

def censor_body(body, good_class):

    print("Body original = " + body)
    sentences = body.split(".")
    #sentences = nltk.sent_tokenize(body)
    print("BODY SENTENCES = " + str(sentences))
    table = SeqTable(sentences)
    entity_generator = analyze(body)
    entities = list(entity_generator)

    sentences = censor_sentences(sentences, table, entities, good_class)

    return sentences

def censor_title_and_summary(article, good_class):

    censored = Article.Article.from_article(article)

    summary = censored.summary
    summary_sents = summary.split(".")
    #summary_sents = nltk.sent_tokenize(summary)
    summary_table = SeqTable(summary_sents)
    entity_generator = analyze(summary)
    summary_entities = list(entity_generator)
    summary_sents = censor_sentences(summary_sents, summary_table, summary_entities, good_class)

    title = censored.title
    title_sents = title.split(".")
    #title_sents = nltk.sent_tokenize(title)
    title_table = SeqTable(title_sents)
    entity_generator = analyze(title)
    title_entities = list(entity_generator)
    title_sents = censor_sentences(title_sents, title_table, title_entities, good_class)

    censored.summary = '. '.join(summary_sents)
    censored.title = '. '.join(title_sents)

    return censored