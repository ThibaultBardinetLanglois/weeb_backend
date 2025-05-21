from django.http import HttpResponse

def hello_articles(request):
    return HttpResponse("bonjour les articles !!")
