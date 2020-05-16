import re
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic.list import ListView
from .models import Article, Category, Tag, Contact
from markdown import Markdown
from django.db.models import F, Q
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.decorators.csrf import csrf_protect
from pure_pagination.mixins import PaginationMixin
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator


class IndexView(PaginationMixin, ListView):
    model = Article
    template_name = "subject/index.html"
    context_object_name = "article_list"
    paginate_by = 5


def article(request, id):
    article = get_object_or_404(Article, pk=id)
    md = Markdown(extensions=['markdown.extensions.extra',
                              'pymdownx.superfences',
                              TocExtension(slugify=slugify), ])
    article.content = md.convert(article.content)
    article.toc = md.toc

    article.tags = [{"name": tag.name, "id": tag.id}
                    for tag in article.tag.all()]

    recomment_article = Article.objects.filter(
        Q(category__name=article.category) & ~Q(title=article.title))[:5]

    try:
        pre_article = Article.objects.get(pk=id-1)
    except ObjectDoesNotExist:
        pre_article = {"id": 0, "title": "没有上一篇了"}

    try:
        next_article = Article.objects.get(pk=id+1)
    except ObjectDoesNotExist:
        next_article = {"id": 0, "title": "没有下一篇了"}

    Article.objects.filter(pk=id).update(read_num=F('read_num') + 1)

    return render(request, "subject/article.html", context={
        "article": article, "pre_article": pre_article,  "next_article": next_article,
        "recomment_article": recomment_article})


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


class SearchView(IndexView):
    def get_queryset(self):
        query_text = self.request.GET.get("query_text")
        article_list = get_list_or_404(Article, Q(
            title__icontains=query_text) | Q(content__icontains=query_text))
        return article_list


class ContactView(ListView):
    def get(self, request):
        contacts = Contact.objects.filter(is_audit="True")
        md = Markdown(extensions=['markdown.extensions.extra'])
        for contact in contacts:
            contact.message = md.convert(contact.message)
        return render(request, 'subject/contact.html', {"contacts": contacts})

    @method_decorator(csrf_protect)
    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        try:
            Contact.objects.create(name=name, email=email, message=message)
            messages.info(request, "留言成功，待审核")
        except Exception:
            messages.error(request, "留言失败")
        return redirect(reverse("subject:contact"))
