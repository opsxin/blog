from django.shortcuts import render

# Create your views here.

import json
import whois
from django.http import JsonResponse


def domain_whois(request, domain):
    d = {"code": 1, "reason": "Succeed", "result": {}}
    try:
        w = whois.query(domain)
        d["result"]["name"] = w.name
        d["result"]["status"] = w.status.split()[0]
        d["result"]["registrar"] = w.registrar
        d["result"]["creation_date"] = w.creation_date
        d["result"]["expiration_date"] = w.expiration_date
        d["result"]["name_servers"] = [x for x in w.name_servers]
    except Exception as e:
        d["code"] = 0
        d["reason"] = str(e)
        print(e)

    return JsonResponse(d)
