from ..models import Article
from ..NLC import AnalyzePage as ap

# takes in discovery results in the form of an Article array from query_manager
# returns array of censored Article objects
def censor(articles):
    censored_articles = []

    # call nlc analysis on each article
    for article in articles:

        # for title, summary, and each body sentence
        # TODO call nlc analysis on different c_article components

        # add new article with changes
        censored_article = ap.censor_article(article)
        censored_articles.append(censored_article)

    return censored_articles