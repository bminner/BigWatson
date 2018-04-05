__author__ = 'Kurtis'

import logging
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .logic import discovery_manager as dm
#from .logic import censor_manager as cm
from .logic import nlu_censor_manager as nlu
from .models import Article
from django.views.decorators.cache import cache_page
import logging


def index(request):
    """ index.html template """

    return render(request, 'index.html')


#@cache_page(60 * 15)
def results(request):
    """ results.html template """

    query = request.GET.get('query', '')
    censorship = request.GET.get('censorship', '')

    query = query.lstrip()
    query = query.rstrip()
    if query == '':
        return render(request, 'index.html')

    # Dictionary for easy conversion from censorship value to description
    censorship_dict = {'1':'negative', '2':'neutral', '3':'positive'}

    censorship_desc = ''
    try:
        censorship_desc = censorship_dict[censorship]
    except KeyError:
        censorship = '2'
        censorship_desc = 'neutral'
        logging.exception('Invalid censorship value provided')
    except:
        raise

    discovery_results = []
    try:
        discovery_results = dm.query_discovery(query)
    except LookupError:
        print("Unknown UTF Encoding")
    except Exception:
        pass
    
    censored_results = []
    if len(discovery_results) > 0:
        #censored_results = cm.censor_results(discovery_results, censorship_desc.lower())
        censored_results = nlu.censor_results(discovery_results, censorship_desc.lower(), query)

        result_titles = {}
        result_summaries = {}
        result_bodies = {}
        result_urls = {}
        for i_i in range(0, len(censored_results)):
            i = str(i_i)
            result_titles[i] = censored_results[i_i].title
            result_summaries[i] = censored_results[i_i].summary
            result_bodies[i] = censored_results[i_i].body
            result_urls[i] = censored_results[i_i].url


        # Store body data in session for use across different views
        request.session['titles'] = result_titles
        request.session['summaries'] = result_summaries
        request.session['bodies'] = result_bodies
        request.session['urls'] = result_urls
        request.session['query'] = query

        request.session['censorship'] = censorship_desc

    return render(
        request,
        'results.html',
        context={'query':query, 'censorship':censorship_desc.title(), 'discovery_results':censored_results}
    )


#@cache_page(60 * 15)
def result(request):
    """ result.html template """

    censorship = request.session.get('censorship', '')
    resultId = request.GET.get('resultId', '')
    title = request.GET.get('title', '')
    query = request.session.get('query', '')
    result_titles = request.session.get('titles', '')
    result_summaries = request.session.get('summaries', '')
    result_bodies = request.session.get('bodies', '')
    result_urls = request.session.get('urls', '')

    body = ''
    article = None
    try:
        article = Article.Article(result_titles[resultId], result_urls[resultId], result_summaries[resultId], result_bodies[resultId])
    except IndexError:
        body = 'ERROR: No article text found for result ID'
        logging.exception('Invalid result ID provided')
    except:
        raise

    body = nlu.censor_body(article, censorship, query)
    body = '<p>' + body.replace('\n', '</p><p>')
    body += '</p>'

    return render(
        request,
        'result.html',
        context={'title':result_titles[resultId], 'body': body}
    )
