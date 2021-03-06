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
        censored_article = censor_title_and_summary(article, good_class)
        censored_articles.append(censored_article)

    return censored_articles

###
### Censors article body.
### Start with an entire page, break it blocks to analyze, censor from there
###
def censor_body(body, good_class):
    #print(good_class)
    POSSIBLE_CLASSES = ['positive', 'negative']

    sentences = body.split('.')
    for i in range(len(sentences)):
        sentence = sentences[i]
        cls = ''
        conf = -1

        #fragments from splitting on periods
        if len(sentence) > 0:
            cls, conf = classify_sentence(sentence)
            #print(cls, conf)

        #basically if nuetral and very confident
        if good_class not in POSSIBLE_CLASSES:
            if conf > .9:
                try:
                    #print("Strong Feelings: " + sentence)
                    pass
                except UnicodeEncodeError:
                    #print("unicode shit")
                    pass
                sentences[i] = '<del>' + sentence + '</del>'
        #if not what we're aiming for
        elif cls != good_class and conf > .4:
            try:
                #print("Bad hombre:" + sentence)
                pass
            except UnicodeEncodeError:
                #print("unicode shit")
                pass
            sentences[i] = '<del>' + sentence + '</del>'

    censored_body = '. '.join(sentences)
    return censored_body


def censor_title_and_summary(article, good_class):
    """ censors and returns an article's title and summary. """

    #print(good_class)
    POSSIBLE_CLASSES = ['positive', 'negative']

    censored = Article.Article.from_article(article)

    summary_sents = censored.summary.split('.')
    for i in range(len(summary_sents)):
        sentence = summary_sents[i]
        cls = ''
        conf = -1

        #fragments from splitting on periods
        if len(sentence) > 0:
            cls, conf = classify_sentence(sentence)
            #print(cls, conf)

        #basically if nuetral and very confident
        if good_class not in POSSIBLE_CLASSES:
            if conf > .9:
                try:
                    #print("Strong Feelings: " + sentence)
                    pass
                except UnicodeEncodeError:
                    #print("unicode shit")
                    pass
                summary_sents[i] = '<del>' + sentence + '</del>'
        #if not what we're aiming for
        elif cls != good_class and conf > .4:
            try:
                #print("Bad hombre:" + sentence)
                    pass
            except UnicodeEncodeError:
                #print("unicode shit")
                    pass
            summary_sents[i] = '<del>' + sentence + '</del>'

    title_sents = censored.title.split('.')
    for i in range(len(title_sents)):
        sentence = title_sents[i]
        cls = ''
        conf = -1

        #fragments from splitting on periods
        if len(sentence) > 0:
            cls, conf = classify_sentence(sentence)
            #print(cls, conf)

        #basically if nuetral and very confident
        if good_class not in POSSIBLE_CLASSES:
            if conf > .9:
                try:
                    #print("Strong Feelings: " + sentence)
                    pass
                except UnicodeEncodeError:
                    #print("unicode shit")
                    pass
                title_sents[i] = '<del>' + sentence + '</del>'
        #if not what we're aiming for
        elif cls != good_class and conf > .4:
            try:
                #print("Bad hombre:" + sentence)
                    pass
            except UnicodeEncodeError:
                #print("unicode shit")
                    pass
            title_sents[i] = '<del>' + sentence + '</del>'

    censored_summary = '. '.join(summary_sents)
    censored.summary = censored_summary
    censored_title = '. '.join(title_sents)
    censored.title = censored_title
    return censored