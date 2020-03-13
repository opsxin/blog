from django import template
from ..models import Article, Category, Tag

register = template.Library()


@register.inclusion_tag('subject/inclusions/_recent_article.html', takes_context=True)
def show_recent_article(context, num=5):
    return {
        "recent_article_list": Article.objects.order_by("-publish_time")[:num]
    }


@register.inclusion_tag('subject/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Article.objects.dates('modify_time', 'month', order='DESC'),
    }


@register.inclusion_tag('subject/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    from django.db.models.aggregates import Count
    categorys = Category.objects.annotate(num_article=Count("article")).filter(
        num_article__gt=0).order_by("-num_article")
    return {
        'category_list': categorys,
    }


@register.inclusion_tag('subject/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list': Tag.objects.all(),
    }
