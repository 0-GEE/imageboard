from re import L
from .models import *
from django.http import JsonResponse
from django.utils.html import conditional_escape

def get_all_tagnames(request):
    tags = Tag.objects.distinct('name')
    l = []
    for tag in tags:
        l.append(conditional_escape(tag.name))

    rdata = {'tags': l}

    return JsonResponse(rdata)

def get_all_tagnames_sqlite3(request):
    tags = Tag.objects.order_by('name')
    l = []
    for i in range(len(tags)):
        try:
            if tags[i].name != tags[i-1].name:
                l.append(conditional_escape(tags[i-1].name))
        except:
            continue
    l.append(conditional_escape(tags[len(tags)-1].name))
    rdata = {'tags': l}

    return JsonResponse(rdata)