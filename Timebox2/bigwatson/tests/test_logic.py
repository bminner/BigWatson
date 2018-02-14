__author__ = 'Kurtis'

from django.test import TestCase
import json
from ..logic.helpers import QueryHelper


class HelpersTest(TestCase):
    """ Tests methods called in helpers.py """

    def create_mock_query_helper(self, meta_description='summary', cleaned_text='body'):
        """ Creates mock extractor with given attributes """
        extractor = MockExtractor(meta_description, cleaned_text)
        return QueryHelper(extractor)
    
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
            
    def test_get_article_data(self):
        helper = self.create_mock_query_helper()
        data = helper.get_article_data(url='')

        self.assertEqual('summary', data['summary'])
        self.assertEqual('body', data['body'])
    
    def test_get_article_data_no_meta_description_returns_body(self):
        helper = self.create_mock_query_helper(meta_description='')
        data = helper.get_article_data('')

        self.assertEqual('body...', data['summary'])
        self.assertEqual('body', data['body'])

    def test_get_article_data_truncates_body_as_meta_description(self):
        long_string = ''
        for _i in range(300):
            long_string += 'a'
        truncated_string = long_string[:200] + '...'

        helper = self.create_mock_query_helper(meta_description='', cleaned_text=long_string)
        data = helper.get_article_data('')

        self.assertEqual(300, len(long_string))
        self.assertEqual(203, len(truncated_string))
        self.assertEqual(truncated_string, data['summary'])
        self.assertEqual(long_string, data['body'])
    
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
    

class MockExtractor():
    """ Object used in place of Goose to unit test get_article_data() """

    def __init__(self, meta_description, cleaned_text):
        self.meta_description = meta_description
        self.cleaned_text = cleaned_text
    
    def extract(self, url):
        return self
 