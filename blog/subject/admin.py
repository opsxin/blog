from django.contrib import admin
from .models import Article, Tag, Category, Contact

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "show_tag",
                    "read_num", "publish_time", "modify_time"]
    search_field = ("title", "author")
    filter_horizontal = ('tag',)
    date_hierarchy = "publish_time"

    def show_tag(self, obj):
        return ", ".join([a.name for a in obj.tag.all()])

    show_tag.short_description = '标签'


class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "publish_time"]
    date_hierarchy = "publish_time"


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Contact, ContactAdmin)
