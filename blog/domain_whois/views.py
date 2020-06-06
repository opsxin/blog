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
        cmd = "curl -vs -m 3 https://{}:{}/ -o /dev/null".format(domain, port)
        text = subprocess.getstatusoutput(cmd)
        if "SSL certificate problem" in text[1]:
            cmd_skip_cert = "curl -svk -m 3 https://{}:{}/ -o /dev/null".format(domain, port)
            text = subprocess.getstatusoutput(cmd_skip_cert)
        if text[0] == 0:
            GMT_FORMAT = '%b %d %H:%M:%S %Y GMT'
            pattern = re.compile(
                r'^\*\s+subject:\s(?P<subject>.*)\s\*\s+start date: (?P<start>.*)\s\*\s+expire date: (?P<expire>.*)\s(\*\s+subjectAltName: host\s.*\smatched cert\'s "(?P<cert>[^"]*)"\s)?\*\s+issuer: .*\s\*\s+SSL certificate verify\s(?P<status>[^(.]+)', re.M)
            issuer_O = re.compile(r'\*\s+issuer:.*O=(?P<O>[\w\s]+)[\s;]')
            issuer_CN = re.compile(r'\*\s+issuer:.*CN=(?P<CN>[\w\s]+)[\s;]')
            content = pattern.search(text[1])
            organization = issuer_O.search(text[1])
            common_name = issuer_CN.search(text[1])
            start = datetime.datetime.strptime(content.group(
                "start"), GMT_FORMAT)+datetime.timedelta(hours=8)
            expire = datetime.datetime.strptime(content.group(
                "expire"), GMT_FORMAT)+datetime.timedelta(hours=8)
            d["result"]["name"] = domain
            if content.group("cert"):
                d["result"]["matched_cert"] = content.group("cert")
            d["result"]["start_date"] = start
            d["result"]["expiration_date"] = expire
            d["result"]["validity"] = (expire - datetime.datetime.now()).days
            d["result"]["subject"] = content.group("subject")
            if organization:
                d["result"]["issuer_organization"] = organization.group("O")
            if common_name:
                d["result"]["issuer_common_name"] = common_name.group("CN")
            d["result"]["status"] = content.group("status").strip()
        else:
            raise ValueError(
                "The query failed. Please check whether the domain or port is correct.")
    except Exception as e:
        d["code"] = 0
        d["reason"] = str(e)
        print(e)

    return JsonResponse(d)
