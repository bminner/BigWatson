__author__ = 'Brandon'

from ..NLU.seqtable import SeqTable
from ..NLU.analyzer import analyze, Entity, AnalyzeResult
from ..models import Article
from ..logic.helpers import WordNetHelper
from nltk.corpus import wordnet as wn
from ..logic.doctree import DocTree, LinkedIndex
import nltk

helper = WordNetHelper(wn)

def censor_results(discovery_results, u_censor_selection):
    """Censors Articles from Discovery query based on user censorship selection."""

    censored_articles = []

    for article in discovery_results:

        # generate doctree and censor
        censored_article = censor_title_and_summary(article, DocTree(article), u_censor_selection)

        # reconstruct censored article
        censored_articles.append(censored_article)

    return censored_articles

def censor_body(body, u_censor_selection):

    return ''

def censor_title_and_summary(original_article, doctree, u_censor_selection):

    censored_title = ''
    censored_summary = ''

    # get AnalyzeResult back from NLU
    analyze_result = analyze(doctree)

    for e in analyze_result.title_entities:
        # if it is the entity we are searching for
        # get WordNode of entity mention
        # based on that, find the sentence that Node is in
        # gather list of WordNodes/indices in entity phrase
        # pass that list to nltk, which will change content of each WordNode
        pass

    for e in analyze_result.summary_entities:
        pass

    censored = Article.Article(censored_title, Article.Article.from_article(original_article).url,
                       censored_summary, Article.Article.from_article(original_article).url.body,
                       Article.Article.from_article(original_article).sentiment_score)

    return censored
