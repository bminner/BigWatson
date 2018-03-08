__author__ = 'Kurtis'

import os
dir_path = os.path.dirname(os.path.realpath(__file__))
from ..models.Article import Article
from nltk.data import path as nltk_path
nltk_path.append(dir_path + '/nltk_data')
from nltk.corpus import wordnet as wn
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import asyncio


class QueryHelper:
    """
    Helper class initialized with extractor client to manage parsing and
    extracting Discovery result data.
    """

    def __init__(self, extractor_client):
        self.extractor = extractor_client

    def parse_discovery_results(self, results):
        """
        Parses results received from querying Watson Discovery.
        Returns list of Articles parsed from json results.
        """

        #async get article data
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        futures = [self.coro_get_article_data(results[i]['url'], i) for i in range(len(results))]
        loop_result = loop.run_until_complete(asyncio.wait(futures))
        tasks = loop_result[0]
        task_results = [task.result() for task in tasks]
        task_results.sort()
        loop.close()

        #create article objects with data
        discovery_results = []
        for i in range(len(results)):
            title = results[i]['title']
            url = results[i]['url']
            
            article_data = task_results[i][1]

            summary = article_data['summary']
            body = article_data['body']
            sentiment_score = results[i]['enriched_text']['sentiment']['document']['score']

            discovery_results.append(Article(title, url, summary, body, sentiment_score))

        return discovery_results

    async def coro_get_article_data(self, url, ind):
        """
        Extracts article data from provided url. Default extractor is Goose object.
        Returns dictionary of strings with keys summary and body.
        """

        # Extract article data
        article = self.extractor.extract(url=url)

        data = {'summary': '', 'body': ''}
        summary = article.meta_description
        body = article.cleaned_text

        # if no meta description, make summary first 200 characters of article body
        data['summary'] = summary if len(summary) > 0 else body[:200] + '...'
        data['body'] = body

        return ind, data


class WordNetHelper:
    """
    Helper class that uses WordNet to get replacement hypernyms/antonyms
    for words to be censored.
    """
    def __init__(self, wordnet_client):
        self.wordnet_client = wordnet_client

    def censor_text(self, text):
        """
        Censors given text by changing all adjectives to their antonyms and
        makes all nouns less polarized and more generic.
        NOTE: This is the main function you should be using with this helper.
        """

        self.wordnet_client.ensure_loaded()
        
        adjs_and_nouns = self.tag_text(text)
        modified_adjs = self.replace_adjectives_with_antonym(text, adjs_and_nouns['adjs'])
        modified_adjs_and_nouns = self.replace_nouns_with_hypernyms(modified_adjs, adjs_and_nouns['nouns'])

        return modified_adjs_and_nouns

    def tag_text(self, text):
        """ tags given text by POS and returns dictionary of adjectives and nouns for modification. """

        adjs_and_nouns = {'adjs': [], 'nouns': []}
        tagged_text = pos_tag(word_tokenize(text))
        
        for wordtag in tagged_text:
            if wordtag[1] == 'JJ':
                adjs_and_nouns['adjs'].append(wordtag[0])
            elif len(wordtag[0]) > 2 and (wordtag[1] == 'NN' or wordtag[1] == 'NNS'):
                    adjs_and_nouns['nouns'].append(wordtag[0])
        
        return adjs_and_nouns

    def replace_adjectives_with_antonym(self, text, adjective_seq):
        """ Replaces adjectives in given text with antonyms. """

        antonyms = []

        for adj in adjective_seq:
            syns = self.wordnet_client.synsets(adj, pos=['a','s'])
            antonym = '<del>' + adj + '</del>'
            
            try:
                for s in syns:
                    for l in s.lemmas():
                        if l.antonyms():
                            antonym = '<strong>' + l.antonyms()[0].name() + '</strong>'
                            raise AntonymFound
            except:
                pass

            antonyms.append((adj, antonym))

        for adjant in antonyms:
            text = text.replace(adjant[0], adjant[1], 1)
            
        return text

    def replace_nouns_with_hypernyms(self, text, noun_seq):
        """ Replaces nouns in text with hypernyms (more generic versions). """

        hypernyms = []

        for noun in noun_seq:
            syns = self.wordnet_client.synsets(noun, pos=['n'])
            hypernym = '<del>' + noun + '</del>'

            for s in syns:
                if s.hypernyms():
                    hypernym = '<strong>' + s.hypernyms()[0].name().split('.')[0] + '</strong>'
                    hypernym = hypernym.replace('_', ' ')
                    break
            
            hypernyms.append((noun, hypernym))
        
        for nounhyp in hypernyms:
            text = text.replace(nounhyp[0], nounhyp[1], 1)

        return text


class AntonymFound(Exception):
    """ used to break nested for loops. Yay python. """

    def __init__(self, message='AntonymFound'):
        self.message = message
        