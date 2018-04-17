__author__ = 'Kurtis'

import os
dir_path = os.path.dirname(os.path.realpath(__file__))
from ..models.Article import Article
from nltk.data import path as nltk_path
nltk_path.append(dir_path + '/nltk_data')
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from watson_developer_cloud import NaturalLanguageClassifierV1
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
                print('I FOUND AN ADJECTIVE. IT IS: ' + wordtag[0])
                adjs_and_nouns['adjs'].append(wordtag[0])
            elif len(wordtag[0]) > 2 and (wordtag[1] == 'NN' or wordtag[1] == 'NNS'):
                print('I FOUND A NOUN. IT IS: ' + wordtag[0])
                adjs_and_nouns['nouns'].append(wordtag[0])
        
        return adjs_and_nouns

    def replace_adjectives_with_antonym(self, text, adjective_seq):
        """ Replaces adjectives in given text with antonyms. """

        antonyms = []
        prefix = '<div class=\"tooltip\">'

        for adj in adjective_seq:
            suffix = '<span class=\"tooltiptext\">' + adj + '</span></div>'
            syns = self.wordnet_client.synsets(adj, pos=['a','s'])
            antonym = '<del>' + adj + '</del>'
            
            try:
                for s in syns:
                    for l in s.lemmas():
                        if l.antonyms():
                            antonym = prefix + '<strong>' + l.antonyms()[0].name() + '</strong>' + suffix
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
        prefix = '<div class=\"tooltip\">'

        for noun in noun_seq:
            suffix = '<span class=\"tooltiptext\">' + noun + '</span></div>'
            syns = self.wordnet_client.synsets(noun, pos=['n'])
            hypernym = '<del>' + noun + '</del>'

            for s in syns:
                if s.hypernyms():
                    hypernym = prefix + '<strong>' + s.hypernyms()[0].name().split('.')[0] + '</strong>' + suffix
                    hypernym = hypernym.replace('_', ' ')
                    break
            
            hypernyms.append((noun, hypernym))
        
        for nounhyp in hypernyms:
            text = text.replace(nounhyp[0], nounhyp[1], 1)

        return text


class CensorHelper:

    def __init__(self):
        self.classifier_id = '719427x293-nlc-242'
        self.classifier = NaturalLanguageClassifierV1(
            username='4d49cfca-bcdc-4ed9-a673-5d561faac440',
            password='GbojuhoOT5rG')

    def censor_wordnodes(self, sentence_and_wordnodes, censorship):
        """
        Censors words in wordnodes dict depending on the censorship level.
        """

        total_censored = []

        if censorship == 'neutral':
            censor = self.censor_neutral
        else:
            censor = self.censor_pos_neg

        for swse in sentence_and_wordnodes:
            sentence = swse[0]
            nodes = swse[1]
            startnode = swse[2]
            endnode = swse[3]
            adjectives = []
            nouns = []

            tagged_text = pos_tag(word_tokenize(sentence))
            for wordtag in tagged_text:
                if wordtag[1] == 'JJ' or wordtag[1] == 'JJS':
                    for node in nodes:
                        if wordtag[0] == node.text:
                            adjectives.append(node)
                            break
                elif len(wordtag[0]) > 2 and (wordtag[1] == 'NN' or wordtag[1] == 'NNS'):
                    for node in nodes:
                        if wordtag[0] == node.text:
                            nouns.append(node)
                            break

            censored = censor(adjectives, nouns, censorship)

            if not censored:
                classes = self.classifier.classify(self.classifier_id, sentence)
                top_class = classes['top_class']
                confidence = classes['classes'][0]['confidence']
                if top_class != censorship and confidence >= 0.92:
                    new_start = '<del>' + startnode.text
                    new_end = endnode.text + '</del>'
                    startnode.update_text(new_start)
                    endnode.update_text(new_end)
            else:
                total_censored += censored

        # get list of censored wordnodes
        
        return total_censored
    
    def censor_pos_neg(self, adjectives, nouns, censorship):
        """ positive/negative censorship. returns list of censored WordNodes """

        censored = []

        for node in adjectives:
            new_node = self.replace_word(node, 'a', self.find_antonym, censorship)
            censored.append(new_node)

        for node in nouns:
            new_node = self.replace_word(node, 'n', self.find_hypernym, censorship)
            censored.append(node)
        
        return censored

    def censor_neutral(self, adjectives, nouns, censorship):
        """ neutral censorship. returns list of censored WordNodes. """

        censored = []

        for node in adjectives:
            word = node.text

            formatted_word = word+'.a.01'
            try:
                sentiment = swn.senti_synset(formatted_word)
                obj_score = float(sentiment.obj_score())

                if obj_score < 0.5:
                    replacement = '<del>' + word + '</del>'
                    node.update_text(replacement)
                    censored.append(node)
            except:
                classes = self.classifier.classify(self.classifier_id, word)
                confidence = classes['classes'][0]['confidence']
                if confidence >= 0.92:
                    replacement = 'prefix + ''<del>' + word + '</del>'
                    node.update_text(replacement)
                    censored.append(node)

        for node in nouns:
            word = node.text
            formatted_word = word+'.n.01'
            try:
                sentiment = swn.senti_synset(formatted_word)
                obj_score = float(sentiment.obj_score())

                if obj_score < 0.5:
                    hypernym = self.find_hypernym(word)
                    node.update_text(hypernym)
                    censored.append(node)
            except:
                classes = self.classifier.classify(self.classifier_id, word)
                confidence = classes['classes'][0]['confidence']
                if confidence >= 0.92:
                    hypernym = self.find_hypernym(word)
                    node.update_text(hypernym)
                    censored.append(node)
        
        return censored

    def replace_word(self, node, pos, replace, swap_class):
        word = node.text
        formatted_word = word+'.'+pos+'.01'

        try:
            sentiment = swn.senti_synset(formatted_word)
            pos_score = float(sentiment.pos_score())
            neg_score = float(sentiment.neg_score())

            if word == 'great':
                classification = 'positive'
            elif pos_score > neg_score:
                classification = 'positive'
            elif neg_score > pos_score:
                classification = 'negative'
            else:
                classification = 'neutral'

            if classification != swap_class and classification != 'neutral':
                replacement = replace(word)
                node.update_text(replacement)
        except:
            classes = self.classifier.classify(self.classifier_id, word)
            top_class = classes['top_class']
            confidence = classes['classes'][0]['confidence']
            if top_class != swap_class and confidence >= 0.92:
                replacement = replace(word)
                node.update_text(replacement)

        return node

    def find_antonym(self, adjective):
        """ finds antonym for given adjective. """

        prefix = '<span class=\"tooltip\">'
        suffix = '<span class=\"tooltiptext\">' + adjective + '</span></span>'
        syns = wn.synsets(adjective, pos=['a','s'])
        antonym = '<del>' + adjective + '</del>'
            
        try:
            for s in syns:
                for l in s.lemmas():
                    if l.antonyms():
                        antonym = prefix + '<strong>' + l.antonyms()[0].name() + '</strong>' + suffix
                        raise AntonymFound
        except:
            pass

        return antonym

    def find_hypernym(self, noun):
        """ finds hypernym for given noun. """

        prefix = '<span class=\"tooltip\">'
        suffix = '<span class=\"tooltiptext\">' + noun + '</span></span>'
        syns = wn.synsets(noun, pos=['n'])
        hypernym = '<del>' + noun + '</del>'

        for s in syns:
            if s.hypernyms():
                hypernym = prefix + '<strong>' + s.hypernyms()[0].name().split('.')[0] + '</strong>' + suffix
                hypernym = hypernym.replace('_', ' ')
                break

        return hypernym


class AntonymFound(Exception):
    """ used to break nested for loops. Yay python. """

    def __init__(self, message='AntonymFound'):
        self.message = message
        
