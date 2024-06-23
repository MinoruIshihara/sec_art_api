from django.http import HttpResponseNotFound

def root_not_found(request):
    return HttpResponseNotFound()