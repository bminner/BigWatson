from django.shortcuts import render
from .managers import query_manager as qm
from .managers import censor_manager as cm


# Create your views here.
def index(request):
    big_watson = 'Big Watson'

    return render(
        request,
        'index.html',
        context={'big_watson':big_watson}
    )

def results(request):
    query = request.GET.get('query', '')
    censorship = request.GET.get('censorship', '')
    censorship_dict = {'1':'negative', '2':'neutral', '3':'positive'}

    discovery_results = qm.query_discovery(query)
    censored_results = cm.censor_results(discovery_results, censorship_dict[censorship])
    
    result_bodies = []
    for r in censored_results:
        result_bodies.append(r.body)
    
    request.session['results'] = result_bodies

    return render(
        request,
        'results.html',
        context={'query':query, 'censorship':censorship_dict[censorship], 'discovery_results':censored_results}
    )

def result(request):
    result_bodies = request.session.get('results', '')
    index = request.GET.get('resultId', '')
    title = request.GET.get('title', '')

    body = result_bodies[int(index)]
    
    return render(
        request,
        'result.html',
        context={'title':title, 'body': body}
    )