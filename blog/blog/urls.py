"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from subject.models import Article, Category, Tag
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
# from django.contrib.staticfiles.views import serve


article_dict = {
    'queryset': Article.objects.all(),
    'date_field': 'modify_time',
}

category_dict = {
    'queryset': Category.objects.all(),
    'date_field': 'publish_time',
}

tag_dict = {
    'queryset': Tag.objects.all(),
    'date_field': 'publish_time',
}

urlpatterns = [
    path('ba/', admin.site.urls),
    path('', include("subject.urls")),
    path('', include("domain_whois.urls")),
    path('', include("paste.urls")),
    # path('favicon.ico', serve, {'path': 'subject/img/favicon.ico'}),
    path('sitemap.xml', sitemap,
         {'sitemaps': {'article': GenericSitemap(article_dict, priority=0.6), 
             'tag': GenericSitemap(tag_dict, priority=0.4),
             'category': GenericSitemap(category_dict, priority=0.5)}},
         name='django.contrib.sitemaps.views.sitemap'),
]

handler404 = 'subject.views.page_not_found'
