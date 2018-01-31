from django.shortcuts import render

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

    # dictionary to change censorship value to representative word
    censorship_dict = {'1':'Negative', '2':'Neutral', '3':'Positive'}

    return render(
        request,
        'results.html',
        context={'query':query, 'censorship':censorship_dict[censorship]}
    )
