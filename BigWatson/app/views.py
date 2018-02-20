__author__ = 'Kurtis'

import logging
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .logic import discovery_manager as dm
from .logic import censor_manager as cm


def index(request):
    """ index.html template """

    return render(request, 'index.html')


@cache_page(60 * 15)
def results(request):
    """ results.html template """

    query = request.GET.get('query', '')
    censorship = request.GET.get('censorship', '')
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

    discovery_results = dm.query_discovery(query)
    censored_results = cm.censor_results(discovery_results, censorship_desc)

    result_bodies = []
    for r in censored_results:
        result_bodies.append(r.body)

    # Store body data in session for use across different views
    request.session['results'] = result_bodies
    request.session['censorship'] = censorship_desc

    return render(
        request,
        'results.html',
        context={'query':query, 'censorship':censorship_desc.title(), 'discovery_results':censored_results}
    )


@cache_page(60 * 15)
def result(request):
    """ result.html template """

    result_bodies = request.session.get('results', '')
    censorship = request.session.get('censorship', '')
    resultId = request.GET.get('resultId', '0')
    title = request.GET.get('title', '')

    body = ''
    try:
        body = result_bodies[int(resultId)] if resultId != '' else None
    except IndexError:
        body = 'ERROR: No article text found for result ID'
        logging.exception('Invalid result ID provided')
    except:
        raise

    body = cm.censor_body(body, censorship)

    return render(
        request,
        'result.html',
        context={'title':title, 'body': body}
    )
