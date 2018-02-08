from goose3 import Goose
import requests


def get_article_data(url):
    """
    Uses Goose to get article data from url.
    Returns dictionary of summary as a string and body as a list of strings (paragraphs)
    """

    g = Goose()
    article = g.extract(url=url)
    data = {'summary': '', 'body': ''}
    summary = article.meta_description
    body = article.cleaned_text
    data['summary'] = summary if len(summary) > 0 else body[:200] + '...'
    data['body'] = article.cleaned_text

    return data


def trim_summary(summary):
    summary = (summary[:160] + '...') if len(summary) > 160 else summary

    return summary
