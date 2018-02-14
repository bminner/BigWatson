__author__ = 'Kurtis'

from django.test import TestCase
from django.urls import reverse


class IndexViewTest(TestCase):
    """ Test cases for index view """

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/bigwatson/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_uses_correct_template(self):
        response = self.client.get('/bigwatson/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class ResultsViewTest(TestCase):
    """
    Test cases for results view.
    NOTE: reverse lookup does not work with url params,
    explaining lack of accessible_by_name test.
    """

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/bigwatson/results/?query=&censorship=')
        self.assertEqual(response.status_code, 200)

    def test_view_url_uses_correct_template(self):
        response = self.client.get('/bigwatson/results/?query=&censorship=')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'results.html')
    
    def test_view_url_absorbs_invalid_censorship_input(self):
        response = self.client.get('/bigwatson/results/?query=&censorship=10')
        self.assertEqual(response.status_code, 200)


class ResultViewTest(TestCase):
    """ Test cases for result view """

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/bigwatson/result/?resultId=&title=')
        self.assertEqual(response.status_code, 200)

    def test_view_url_uses_correct_template(self):
        response = self.client.get('/bigwatson/result/?resultId=&title=')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'result.html')

    def test_view_url_absorbs_invalid_resultId(self):
        response = self.client.get('/bigwatson/result/?resultId=10&title=')
        self.assertEqual(response.status_code, 200)
