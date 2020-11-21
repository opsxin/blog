from django.contrib import admin
from .models import Paste

# Register your models here.
class PasteAdmin(admin.ModelAdmin):
    list_display = ["name", "message", "code_class", "valid_day", "publish_time"]
    date_hierarchy = "publish_time"


admin.site.register(Paste, PasteAdmin)
