__author__ = 'Nicholas'

from LanguageUnderstanding import parse_categories, analyze_sentence

###
### Start with an entire page, break it blocks to analyze, censor from there
###

def __main__():
    response = analyze_sentence("Trump is going to start a war and become dictator")
    labels = parse_categories(response)
    print(labels)

__main__()