from django.contrib.syndication.views import Feed
from .models import Article


class ArticleFeed(Feed):
    title = "opsxin site articles"
    link = "/"
    description = "dev and ops articles."

    def items(self):
        return Article.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt
