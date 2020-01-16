from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic.list import ListView
from .models import Article, Category, Tag, Contact
from markdown import Markdown
from django.db.models import F
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.decorators.csrf import csrf_protect
from pure_pagination.mixins import PaginationMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

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
                              TocExtension(slugify=slugify), ])
    article.content = md.convert(article.content)
    article.toc = md.toc

    Article.objects.filter(pk=id).update(read_num=F('read_num') + 1)

    return render(request, "subject/article.html", context={"article": article})


class ArchiveView(IndexView):
    def get_queryset(self):
        return super().get_queryset().filter(modify_time__year=self.kwargs.get("year"),
                                             modify_time__month=self.kwargs.get(
                                                 "month")
                                             ).order_by('-modify_time')


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get("id"))
        return super().get_queryset().filter(category=cate).order_by('-modify_time')


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get("id"))
        return super().get_queryset().filter(tag=tag).order_by('-modify_time')


@csrf_protect
def search(request):
    if request.method == 'POST':
        query_text = request.POST.get("query_text")
        article_list = get_list_or_404(Article, title__icontains=query_text)
    else:
        return HttpResponseRedirect(reverse("subject:index"))

    return render(request, 'subject/index.html', context={'article_list': article_list})


class FullView(IndexView):
    template_name = "subject/full.html"


def about(request):
    return render(request, 'subject/about.html')


@csrf_protect
def contact(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        try:
            Contact.objects.create(name=name, email=email,
                                   subject=subject, message=message)
            messages.info(request, "留言成功")
        except:
            messages.error(request, "留言失败")
        return HttpResponseRedirect(reverse("subject:contact"))
    else:
        return render(request, 'subject/contact.html')
