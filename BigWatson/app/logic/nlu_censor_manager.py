__author__ = 'Brandon'

from ..NLU.seqtable import SeqTable
from ..NLU.analyzer import analyze, Entity, AnalyzeResult
from ..models import Article
from ..logic.helpers import WordNetHelper, CensorHelper
from nltk.corpus import wordnet as wn
from ..logic.doctree import DocTree, LinkedIndex, WordNode
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
    title_sentences_and_wordnodes = _find_word_nodes_to_censor(doctree, analyze_result.title_entities, u_query, DocTree.title_sentence_at)
    summary_sentences_and_wordnodes = _find_word_nodes_to_censor(doctree, analyze_result.summary_entities, u_query, DocTree.summary_sentence_at)

    # pass that list to nltk, which will change content of each WordNode
    # call Kurt's stuff here!
    # censor(title_sentences_and_wordnodes, u_censor_selection)
    # censor(summary_sentences_and_wordnodes, u_censor_selection)
    ch = CensorHelper()
    censored_title_wordnodes = ch.censor_wordnodes(title_sentences_and_wordnodes, u_censor_selection)
    censored_summary_wordnodes = ch.censor_wordnodes(summary_sentences_and_wordnodes, u_censor_selection)

    censored = Article.Article(doctree.get_title(), Article.Article.from_article(original_article).url,
                       doctree.get_summary(), Article.Article.from_article(original_article).body,
                       Article.Article.from_article(original_article).sentiment_score)

    return censored


def censor_body(original_article, u_censor_selection, u_query):
    """Censors Article body. Separate from title and summary to allow lazy censoring on click from views.py"""

    # recreate article and doctree
    doctree = DocTree(original_article)

    # get AnalyzeResult back from NLU
    analyze_result = analyze(doctree)

    # find WordNodes to censor
    body_sentences_and_wordnodes = _find_word_nodes_to_censor(doctree, analyze_result.body_entities, u_query, DocTree.body_sentence_at)
    print(body_sentences_and_wordnodes)
    # Perform censorship
    ch = CensorHelper()
    censored_body_wordnodes = ch.censor_wordnodes(body_sentences_and_wordnodes, u_censor_selection)
    print(str(censored_body_wordnodes))

    # censor(body_sentences_and_wordnodes, u_censor_selection)

    censored = doctree.get_body()

    return censored


def _find_word_nodes_to_censor(doctree, entity_list, u_query, sentence_at_callback):
    """Logic to find WordNodes to censor based on mentions and phrases in Entities"""

    word_nodes_to_censor = []
    sentence_and_wordnodes= []

    # for each entity
    for e in entity_list:
        # if it is the entity we are searching for
        if e.name == u_query or u_query in e.name:
            # for every mention
            for i, mention in enumerate(e.mentions):
                mention_wn = mention[1]
                # based on that, find the sentence that Node is in
                mention_sn = sentence_at_callback(doctree, mention_wn.get_start_index())
                # gather list of WordNodes in entity phrase
                words_to_censor = e.phrases[i].split(' ')
                for to_censor in words_to_censor:
                    matched_word_nodes = mention_sn.find(to_censor)
                    word_nodes_to_censor = word_nodes_to_censor + matched_word_nodes
                sentence_and_wordnodes.append((mention_sn.original_text, word_nodes_to_censor))

    return sentence_and_wordnodes
