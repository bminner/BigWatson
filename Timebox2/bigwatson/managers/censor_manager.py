from ..models import Article
from ..NLC.use_nlc import classify_sentence

# takes in discovery results in the form of an Article array from query_manager
# returns array of censored Article objects
def censor_results(discovery_results, good_class):
    censored_articles = []

    # call nlc analysis on each article
    for article in discovery_results:

        # for title, summary, and each body sentence
        # TODO call nlc analysis on different c_article components

        # add new article with changes
        censored_article = censor_article(article, good_class)
        censored_articles.append(censored_article)

    return censored_articles

###
### Start with an entire page, break it blocks to analyze, censor from there
###
def censor_article(article, good_class):
    print(good_class)
    POSSIBLE_CLASSES = ['positive', 'negative']

    censored = Article.Article.from_article(article)

    sentences = censored.body.split('.')
    for i in range(len(sentences)):
        sentence = sentences[i]
        cls = ''
        conf = -1

        #fragments from splitting on periods
        if len(sentence) > 0:
            cls, conf = classify_sentence(sentence)
            print(cls, conf)

        #basically if nuetral and very confident
        if good_class not in POSSIBLE_CLASSES:
            if conf > .9:
                try:
                    print("Strong Feelings: " + sentence)
                except UnicodeEncodeError:
                    print("unicode shit")
                sentences[i] = '<del>' + sentence + '</del>'
        #if not what we're aiming for
        elif cls != good_class and conf > .4:
            try:
                print("Bad hombre:" + sentence)
            except UnicodeEncodeError:
                print("unicode shit")
            sentences[i] = '<del>' + sentence + '</del>'

    censored_body = '. '.join(sentences)
    censored.body = censored_body
    return censored