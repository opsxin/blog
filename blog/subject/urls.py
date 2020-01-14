from django.urls import path, include
from . import views

app_name = "subject"
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('article/<int:id>/', views.article, name="article"),
    path('archive/<int:year>/<int:month>/', views.archive, name="archive"),
    path('category/<int:id>/', views.category, name="category"),
    path('tag/<int:id>/', views.tag, name="tag"),
    path('full/', views.full, name="full"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
]
