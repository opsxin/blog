from django.urls import path, include
from . import views

app_name = "subject"
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('article/<int:id>/', views.article, name="article"),
    path('archive/<int:year>/<int:month>/',
         views.ArchiveView.as_view(), name="archive"),
    path('category/<int:id>/', views.CategoryView.as_view(), name="category"),
    path('tag/<int:id>/', views.TagView.as_view(), name="tag"),
    path('search/', views.search, name="search"),
    # path('full/', views.FullView.as_view(), name="full"),
    # path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
]
