from django.shortcuts import render

# Create your views here.
def index(request):
    big_watson='Big Watson'

    return render(
        request,
        'index.html',
        context={'big_watson':big_watson}
    )