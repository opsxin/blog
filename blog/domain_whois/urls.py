from django.urls import path, include
from . import views

app_name = "domain_whois"
urlpatterns = [
    path('whois/<str:domain>', views.domain_whois, name="domain_whois"),
]
