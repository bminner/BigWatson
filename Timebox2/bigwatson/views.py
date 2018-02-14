__author__ = 'Kurtis'

from django.shortcuts import render
from .logic import discovery_manager as dm
from django.views.decorators.cache import cache_page
import logging


def index(request):
    big_watson = 'Big Watson'

    return render(
        request,
        'index.html',
        context={'big_watson':big_watson}
    )


@cache_page(60 * 15)
def results(request):
    query = request.GET.get('query', '')
    censorship = request.GET.get('censorship', '')
    # Dictionary for easy conversion from censorship value to description
    censorship_dict = {'1':'Negative', '2':'Neutral', '3':'Positive'}

    censorship_desc = ''
    try:
        censorship_desc = censorship_dict[censorship]
    except KeyError:
        censorship = '2'
        censorship_desc = 'Neutral'
        logging.exception('Invalid censorship value provided')
    except:
        raise

    discovery_results = dm.query_discovery(query)
    
    result_bodies = []
    for r in discovery_results:
        result_bodies.append(r.body)
    
    # Store body data in session for use across different views
    request.session['results'] = result_bodies

    return render(
        request,
        'results.html',
        context={'query':query, 'censorship':censorship_desc, 'discovery_results':discovery_results}
    )


@cache_page(60 * 15)
def result(request):
    result_bodies = request.session.get('results', '')
    index = request.GET.get('resultId', '0')
    title = request.GET.get('title', '')

    body = ''
    try:
        body = result_bodies[int(index)] if index != '' else None
    except IndexError:
        body = 'ERROR: No article text found for result ID'
        logging.exception('Invalid result ID provided')
    except:
        raise
    
    return render(
        request,
        'result.html',
        context={'title':title, 'body': body}
    )