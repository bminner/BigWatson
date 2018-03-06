__author__ = 'Brandon'

from ..NLU.seqtable import SeqTable
from ..NLU.analyzer import analyze, Entity
from ..models import Article
from nltk.tokenize import sent_tokenize

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
        locations = ce.mentions
        for location in locations:
            index_tuple = table.lookup(location)
            sent_index = sentences.index(index_tuple[0])
            sentences[sent_index] = '<del>' + index_tuple[0] + '</del>'
    
    return sentences

def censor_body(body, good_class):

    sentences = sent_tokenize(body)
    table = SeqTable(sentences)
    entity_generator = analyze(body)
    entities = list(entity_generator)

    sentences = censor_sentences(sentences, table, entities, good_class)

    return sentences

def censor_title_and_summary(article, good_class):

    censored = Article.Article.from_article(article)

    summary = censored.summary
    summary_sents = sent_tokenize(summary)
    summary_table = SeqTable(summary_sents)
    entity_generator = analyze(summary)
    summary_entities = list(entity_generator)
    summary_sents = censor_sentences(summary_sents, summary_table, summary_entities, good_class)

    title = censored.title
    title_sents = sent_tokenize(title)
    title_table = SeqTable(title_sents)
    entity_generator = analyze(title)
    title_entities = list(entity_generator)
    title_sents = censor_sentences(title_sents, title_table, title_entities, good_class)

    censored.summary = '. '.join(summary_sents)
    censored.title = '. '.join(title_sents)

    return censored

def __main__():
    text = "The president is a ball gargling idiot."
    good_class = 'positive'
    censor_body(text,good_class)