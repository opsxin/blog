from django.shortcuts import render

# Create your views here.

import re
import json
import whois
import datetime
import subprocess
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


def domain_cert(request, domain, port=443):
    d = {"code": 1, "reason": "Succeed", "result": {}}
    try:
        cmd = "curl -v -m 3 https://{}:{}/ -o /dev/null".format(domain, port)
        text = subprocess.getstatusoutput(cmd)
        if text[0] == 0:
            GMT_FORMAT = '%b %d %H:%M:%S %Y GMT'
            pattern = re.compile(
                r'^\*\s+subject:\s(?P<subject>.*)\s\*\s+start date: (?P<start>.*)\s\*\s+expire date: (?P<expire>.*)\s\*\s+subjectAltName: host "(?P<host>[^"]*)"\smatched cert\'s "(?P<cert>[^"]*)"\s\*\s+issuer: C=([^;]*);\sO=(?P<O>[^;]*);\s(OU=.*)?CN=(?P<CN>.*)\s\*\s+SSL certificate verify\s(?P<status>.*).$', re.M)
            content = pattern.search(text[1])
            start = datetime.datetime.strptime(content.group(
                "start"), GMT_FORMAT)+datetime.timedelta(hours=8)
            expire = datetime.datetime.strptime(content.group(
                "expire"), GMT_FORMAT)+datetime.timedelta(hours=8)
            d["result"]["name"] = content.group("host")
            d["result"]["matched_cert"] = content.group("cert")
            d["result"]["start_date"] = start
            d["result"]["expiration_date"] = expire
            d["result"]["validity"] = (expire - datetime.datetime.now()).days
            d["result"]["subject"] = content.group("subject")
            d["result"]["issuer_organization"] = content.group("O")
            d["result"]["issuer_common_name"] = content.group("CN")
            d["result"]["status"] = content.group("status")
        else:
            raise ValueError("The query failed. Please check whether the domain or port is correct.")
    except Exception as e:
        d["code"] = 0
        d["reason"] = str(e)
        print(e)

    return JsonResponse(d)
