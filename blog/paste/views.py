import bleach
from .models import Paste
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


# Create your views here.
@require_http_methods(["POST"])
@csrf_exempt
def paste_upload(request, name):
    msg = request.body.decode('utf-8')
    p = Paste.objects.create(name=name, message=bleach.clean(msg))
    url = reverse('paste:paste_show', kwargs={'name': name, 'id': p.pk})

    return HttpResponse(request.build_absolute_uri(url))

@require_http_methods(["GET"])
def paste_show(requests, name, id):
    p = get_object_or_404(Paste, pk=id, name=name)

    return HttpResponse(p.message)
