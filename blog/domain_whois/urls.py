from django.urls import path, include
from . import views

app_name = "domain_whois"
urlpatterns = [
    path('whois/<str:domain>', views.domain_whois, name="domain_whois"),
    path('cert/<str:domain>', views.domain_cert, name="domain_cert"),
    path('cert/<str:domain>/<int:port>', views.domain_cert, name="domain_cert_port"),
]
