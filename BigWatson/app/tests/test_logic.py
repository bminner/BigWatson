__author__ = 'Kurtis'

import asyncio
from django.test import TestCase
import json
from nltk.corpus import wordnet as wn
from ..logic.helpers import QueryHelper, WordNetHelper, CensorHelper
from ..logic.nlu_censor_manager import censor_body, _censor_title_and_summary, _find_word_nodes_to_censor
from ..logic.doctree import WordNode, LinkedIndex, DocTree
from ..models import Article
from ..logic import doctree as dt
from ..NLU import analyzer
from ..NLU.analyzer import Entity, AnalyzeResult


class HelpersTest(TestCase):
    """ Tests methods called in helpers.py """

    def create_mock_query_helper(self, meta_description='summary', cleaned_text='body'):
        """ Creates mock extractor with given attributes """
        extractor = MockExtractor(meta_description, cleaned_text)
        return QueryHelper(extractor)

    def create_mock_wordnet_helper(self, wordnet_client=wn):
        return WordNetHelper(wordnet_client)

    def create_mock_results(self):
        """ Creates list of results in the format of a Discovery query result """
        results = []
        for i in range(3):
            result = {
                'title': 'title' + str(i),
                'url': 'url' + str(i),
                'enriched_text': {
                    'sentiment': {
                        'document': {
                            'score': i
                        }
                    }
                }
            }
            results.append(result)

        return results
    
    def test_censor_wordnodes_censors_to_be_positive(self):
        helper = CensorHelper()
        sentence = 'Nick Meyer is a sexy man with brilliant skin'
        wordnodes = [
                 WordNode('a', LinkedIndex(0)),
                 WordNode('sexy', LinkedIndex(0)),
                 WordNode('man', LinkedIndex(0)),
                 WordNode('with', LinkedIndex(0)),
                 WordNode('brilliant', LinkedIndex(0)),
                 WordNode('skin', LinkedIndex(0))
        ]
        sentence_and_wordnodes = [(sentence, wordnodes, wordnodes[0], wordnodes[5])]
        censored = helper.censor_wordnodes(sentence_and_wordnodes, 'negative')

    def create_mock_article(self):
        """Creates a mock article for use in tests"""
        return Article.Article('The Ohio State University is the best college in the land', 'http://www.sampleurl.com',
                               'This is an article saying that the Ohio State University is great. '
                               'The school is horrible.', 'This is an article saying that the Ohio State '
                               'University is great. The school is horrible. Also this is an extra line to '
                                                          'talk about Brutus. Finally, Urban Meyer is great.', 0.0)

    def test_get_article_data(self):
        helper = self.create_mock_query_helper()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        futures = [helper.coro_get_article_data('', 0)]
        loop_result = loop.run_until_complete(asyncio.wait(futures))
        tasks = loop_result[0]
        task_results = [task.result() for task in tasks]
        task_results.sort()
        loop.close()

        self.assertEqual('summary', task_results[0][1]['summary'])
        self.assertEqual('body', task_results[0][1]['body'])

    def test_get_article_data_no_meta_description_returns_body(self):
        helper = self.create_mock_query_helper(meta_description='')

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        futures = [helper.coro_get_article_data('', 0)]
        loop_result = loop.run_until_complete(asyncio.wait(futures))
        tasks = loop_result[0]
        task_results = [task.result() for task in tasks]
        task_results.sort()
        loop.close()

        self.assertEqual('body...', task_results[0][1]['summary'])
        self.assertEqual('body', task_results[0][1]['body'])

    def test_get_article_data_truncates_body_as_meta_description(self):
        long_string = ''
        for _i in range(300):
            long_string += 'a'
        truncated_string = long_string[:200] + '...'

        helper = self.create_mock_query_helper(meta_description='', cleaned_text=long_string)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        futures = [helper.coro_get_article_data('', 0)]
        loop_result = loop.run_until_complete(asyncio.wait(futures))
        tasks = loop_result[0]
        task_results = [task.result() for task in tasks]
        task_results.sort()
        loop.close()

        self.assertEqual(300, len(long_string))
        self.assertEqual(203, len(truncated_string))
        self.assertEqual(truncated_string, task_results[0][1]['summary'])
        self.assertEqual(long_string, task_results[0][1]['body'])

    def test_parse_discovery_results(self):
        results = self.create_mock_results()
        helper = self.create_mock_query_helper()
        discovery_results = helper.parse_discovery_results(results)

        self.assertEqual(3, len(discovery_results))
        suffix = 0 # Article object isn't iterable, hence the suffix index variable
        for result in discovery_results:
            title = 'title' + str(suffix)
            url = 'url' + str(suffix)
            self.assertEqual(title, result.title)
            self.assertEqual(url, result.url)
            self.assertEqual('summary', result.summary)
            self.assertEqual('body', result.body)
            self.assertEqual(suffix, result.sentiment_score)
            suffix += 1

    def test_tag_text_tags_text(self):
        helper = self.create_mock_wordnet_helper()
        text = 'the cat wears a red hat'

        adjs_and_nouns = helper.tag_text(text)
        adjs = adjs_and_nouns['adjs']
        nouns = adjs_and_nouns['nouns']

        self.assertEqual(1, len(adjs))
        self.assertEqual('red', adjs[0])
        self.assertEqual(2, len(nouns))
        self.assertEqual('cat', nouns[0])
        self.assertEqual('hat', nouns[1])

    def test_replace_adjective_with_antonym_replaces_adjective(self):
        helper = self.create_mock_wordnet_helper()
        positive_text = 'the dog is a good boy'
        negative_text = 'the dog is a bad boy'
        pos_adjective_seq = ['good']
        neg_adjective_seq = ['bad']

        edited_to_be_negative = helper.replace_adjectives_with_antonym(positive_text, pos_adjective_seq)
        edited_to_be_positive = helper.replace_adjectives_with_antonym(negative_text, neg_adjective_seq)


        self.assertEqual('the dog is a <div class="tooltip"><strong>bad</strong><span class="tooltiptext">good</span></div> boy', edited_to_be_negative)
        self.assertEqual('the dog is a <div class="tooltip"><strong>good</strong><span class="tooltiptext">bad</span></div> boy', edited_to_be_positive)

    """
    # these tests use hypernyms, which we won't be using quite yet, so they're commented out.
    def test_replace_noun_with_hypernyms_replaces_noun(self):
        helper = self.create_mock_wordnet_helper()
        text = 'the dog is a good boy'
        noun_seq = ['dog', 'boy']

        edited_text = helper.replace_nouns_with_hypernyms(text, noun_seq)

        self.assertEqual('the <strong>canine</strong> is a good <strong>male</strong>', edited_text)

    def test_censor_text_censors_adjectives_and_nouns(self):
        helper = self.create_mock_wordnet_helper()
        text = 'the dog is a good boy'

        censored_text = helper.censor_text(text)

        self.assertEqual('the <strong>canine</strong> is a <strong>bad</strong> <strong>male</strong>', censored_text)
    """

    """
    class NLUTest(TestCase):
        def test_censor_body(self):
            body = "Tom Brady is amazing.Donald Trump is an idiot and awful president and Tom Brady is my hero.North Korea is the worst country in the world."
            good_class = 'positive'
            results = censor_body(body, good_class)
            print("First results = " + str(results))
            censored_result = "<del>Donald Trump is an idiot and awful president</del>. Cats are cool and I like bunnies. <del>North Korea is the worst country in the world</del>. "

            print("censored = " + str(censored_result))
            print("results given = " + str(results))
            self.assertEqual(censored_result,results)"""

    def test_parse_entities(self):
        article = self.create_mock_article()
        doctree = dt.DocTree(article)
        nlu_result = analyzer._query_nlu(Article.Article.from_article(article).body)
        body_gen = analyzer._parse_entities(nlu_result, doctree.body_word_at)
        entity_list = []
        for entity in body_gen:
            entity_list.append(entity)
        assert(len(entity_list) == 3)
        assert(entity_list[0].name == 'Ohio State University')
        assert(entity_list[1].mentions[0][2])
        assert(entity_list[1].phrases[0] == 'great Urban Meyer')

    def test_analyze(self):
        article = self.create_mock_article()
        doctree = dt.DocTree(article)
        result = analyzer.analyze(doctree)
        entity_list = []
        for entity in result.body_entities:
            entity_list.append(entity)
        assert(len(entity_list) == 3)

    # def test_censor_title_and_summary(self):
    #    pass

    # def test_censor_body(self):
    #    pass

    def test_find_word_nodes_to_censor(self):
        article = self.create_mock_article()
        doctree = DocTree(article)
        result = analyzer.analyze(doctree)
        sentence_and_wordnodes = _find_word_nodes_to_censor(doctree, result.body_entities, 'Urban Meyer', DocTree.body_sentence_at)
        assert(len(sentence_and_wordnodes) == 1)
        assert(sentence_and_wordnodes[0][0] == 'Finally, Urban Meyer is great.')
        assert(sentence_and_wordnodes[0][1][0].text == 'great')

class MockExtractor():
    """ Object used in place of Goose to unit test get_article_data() """

    def __init__(self, meta_description, cleaned_text):
        self.meta_description = meta_description
        self.cleaned_text = cleaned_text

    def extract(self, url):
        return self
