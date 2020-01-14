from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic.list import ListView
from .models import Article, Category, Tag
from markdown import Markdown
from django.db.models import F
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.decorators.csrf import csrf_protect
from pure_pagination.mixins import PaginationMixin
from pure_pagination import Paginator

# Create your views here.


class IndexView(PaginationMixin, ListView):
    model = Article
    template_name = "subject/index.html"
    context_object_name = "article_list"
    paginate_by = 5


def article(request, id):
    article = get_object_or_404(Article, pk=id)
    md = Markdown(extensions=['markdown.extensions.extra',
                              'markdown.extensions.codehilite',
                              #   'markdown.extensions.toc',
                              TocExtension(slugify=slugify), ])
    article.content = md.convert(article.content)
    article.toc = md.toc

    Article.objects.filter(pk=id).update(read_num=F('read_num') + 1)

    return render(request, "subject/article.html", context={"article": article})


def archive(request, year, month):
    article_list = Article.objects.filter(modify_time__year=year,
                                          modify_time__month=month
                                          ).order_by('-modify_time')
    return render(request, 'subject/index.html', context={'article_list': article_list})


def category(request, id):
    cate = get_object_or_404(Category, pk=id)
    article_list = Article.objects.filter(
        category=cate).order_by('-modify_time')
    return render(request, 'subject/index.html', context={'article_list': article_list})


def tag(request, id):
    tag = get_object_or_404(Tag, pk=id)
    article_list = Article.objects.filter(
        tag=tag).order_by('-modify_time')
    return render(request, 'subject/index.html', context={'article_list': article_list})


@csrf_protect
def search(request):
    if request.method == 'POST':
        query_text = request.POST.get("query_text")
        article_list = get_list_or_404(Article, title__icontains=query_text)

    return render(request, 'subject/index.html', context={'article_list': article_list})


def full(request):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    article_list = Article.objects.all()
    p = Paginator(article_list, request=request, per_page=5)
    article_list = p.page(page)
    return render(request, 'subject/full.html', context={'article_list': article_list})


def about(request):
    return render(request, 'subject/about.html')


def contact(request):
    return render(request, 'subject/contact.html')
