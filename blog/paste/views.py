import json
import bleach
from .models import Paste
from datetime import datetime, timedelta
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


# Create your views here.
@require_http_methods(["POST"])
@csrf_exempt
def paste_upload(request, name):
    try:
        paste = json.loads(request.body.decode('utf-8'))
        valid_day = paste.get("validity", 3)
        code_class = paste.get("class", "nohighlight")
        msg = paste.get("message")

        if len(code_class) > 15:
            code_class = "nohighlight"
        if valid_day > 31:
            valid_day = 31

        p = Paste.objects.create(name=name, message=bleach.clean(
            msg), valid_day=valid_day, code_class=code_class.lower())
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
        html = '''<link rel="stylesheet" href="//cdn.jsdelivr.net/gh/highlightjs/cdn-release@10.4.0/build/styles/atom-one-light.min.css">
<script src="//cdn.jsdelivr.net/gh/highlightjs/cdn-release@10.4.0/build/highlight.min.js"></script>
<script>hljs.initHighlightingOnLoad();</script>
<pre><code class="{}" style="font-size: 1.6em;">{}</code></pre>'''.format(p.code_class, p.message)

        return HttpResponse(html)
