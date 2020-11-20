from django.urls import path, include
from . import views

app_name = "paste"
urlpatterns = [
        path('paste/<str:name>', views.paste_upload, name="paste_upload"),
        path('paste/<str:name>/<int:id>', views.paste_show, name="paste_show"),
]
