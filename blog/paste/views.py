import json
import bleach
from .models import Paste
from datetime import datetime, timedelta
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


code_classes = ["plaintext", "bash", "c++", "c#", "css", "dockerfile", "go", "html", "java",
                "javascript", "json", "markdown", "php", "python", "sql", "typescript", "xml", "yaml"]


def paste(request):
    if request.method == "GET":
        return render(request, 'paste/paste.html')
    if request.method == "POST":
        name = request.POST.get("name")

        code_class = request.POST.get("code_class")
        if code_class not in code_classes:
            code_class = "nohighlight"

        valid_day = request.POST.get("validity")
        if int(valid_day) <= 0 or int(valid_day) > 30:
            valid_day = 30

        msg = request.POST.get("message")

        p = Paste.objects.create(name=name, message=bleach.clean(
            msg, tags=[], strip_comments=False), valid_day=valid_day, code_class=code_class.lower())
        url = reverse('paste:paste_show', kwargs={'name': name, 'id': p.pk})

        return redirect(request.build_absolute_uri(url))
    return redirect(reverse("subject:index"))


@require_http_methods(["POST"])
@csrf_exempt
def paste_upload(request, name):
    try:
        paste = json.loads(request.body.decode('utf-8'))
        valid_day = paste.get("validity", 1)
        code_class = paste.get("code_class", "nohighlight")
        msg = paste.get("message")

        if code_class not in code_classes:
            code_class = "nohighlight"
        if int(valid_day) <= 0 or int(valid_day) > 30:
            valid_day = 30

        p = Paste.objects.create(name=name, message=bleach.clean(
            msg, tags=[], strip_comments=False), valid_day=valid_day, code_class=code_class.lower())
        url = reverse('paste:paste_show', kwargs={'name': name, 'id': p.pk})

        return HttpResponse(request.build_absolute_uri(url))
    except Exception as e:
        print(e)
        return HttpResponse("Internal Error!")


@require_http_methods(["GET"])
def paste_show(requests, name, id):
    p = get_object_or_404(Paste, pk=id, name=name)

    varidity = p.publish_time + timedelta(days=p.valid_day)
    if datetime.now() > varidity:
        return HttpResponse("Link Expired!")
    else:
        return render(requests, 'paste/paste_show.html', {"contents": p})
