from django.http import HttpResponse

def hello_contact(request):
    return HttpResponse("bonjour contact !!")
