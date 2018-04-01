__author__ = 'Brandon'

from ..NLU.seqtable import SeqTable
from ..NLU.analyzer import analyze, Entity, AnalyzeResult
from ..models import Article
from ..logic.helpers import WordNetHelper
from nltk.corpus import wordnet as wn
from ..logic.doctree import DocTree, LinkedIndex
import nltk

helper = WordNetHelper(wn)


def censor_results(discovery_results, u_censor_selection, u_query):
    """Censors Articles from Discovery query based on user censorship selection."""

    censored_articles = []

    for article in discovery_results:

        # generate doctree and censor
        censored_article = _censor_title_and_summary(article, DocTree(article), u_censor_selection, u_query)

        # reconstruct censored article
        censored_articles.append(censored_article)

    return censored_articles


def _censor_title_and_summary(original_article, doctree, u_censor_selection, u_query):
    """Censors Article title and summary"""

    # get AnalyzeResult back from NLU
    analyze_result = analyze(doctree)

    # find WordNodes to censor
    title_nodes_to_censor = _find_word_nodes_to_censor(analyze_result.title_entities, u_query, DocTree.title_sentence_at())
    summary_nodes_to_censor = _find_word_nodes_to_censor(analyze_result.summary_entities, u_query, DocTree.summary_sentence_at())

    # pass that list to nltk, which will change content of each WordNode
    # call Kurt's stuff here!
    # censor(title_nodes_to_censor, u_censor_selection)
    # censor(summary_nodes_to_censor, u_censor_selection)

    censored = Article.Article(doctree.get_title(), Article.Article.from_article(original_article).url,
                       doctree.get_summary(), Article.Article.from_article(original_article).body,
                       Article.Article.from_article(original_article).sentiment_score)

    return censored


def censor_body(original_article, doctree, u_censor_selection, u_query):
    """Censors Article body. Separate from title and summary to allow lazy censoring on click from views.py"""

    # get AnalyzeResult back from NLU
    analyze_result = analyze(doctree)

    # find WordNodes to censor
    body_nodes_to_censor = _find_word_nodes_to_censor(analyze_result.title_entities, u_query, DocTree.body_sentence_at())

    # pass that list to nltk, which will change content of each WordNode
    # call Kurt's stuff here!
    # censor(body_nodes_to_censor, u_censor_selection)

    censored = Article.Article(Article.Article.from_article(original_article).title, Article.Article.from_article(original_article).url,
                       Article.Article.from_article(original_article).summary, doctree.get_body(),
                       Article.Article.from_article(original_article).sentiment_score)

    return censored


def _find_word_nodes_to_censor(entity_list, u_query, sentence_at_callback):
    """Logic to find WordNodes to censor based on mentions and phrases in Entities"""

    word_nodes_to_censor = []

    # for each entity
    for e in entity_list:
        # if it is the entity we are searching for
        if e.name == u_query:
            # for every mention
            for mention_index in range(len(e.mentions)):
                # get WordNode in mention
                mention_wn = e.mentions[mention_index][1]
                # based on that, find the sentence that Node is in
                mention_sn = sentence_at_callback(mention_wn.get_start_index())
                # gather list of WordNodes in entity phrase
                words_to_censor = e.phrases[mention_index].split(' ')
                for word_index in range(len(mention_sn)):
                    if mention_sn.word_at(word_index).text in words_to_censor:
                        word_nodes_to_censor.append(mention_sn.word_at(word_index))

    return word_nodes_to_censor
