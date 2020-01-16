from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Tag(models.Model):
    name = models.CharField("标签", max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name


class Category(models.Model):
    name = models.CharField("类别", max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "类别"
        verbose_name_plural = verbose_name


class Article(models.Model):
    title = models.CharField("标题", max_length=50)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="作者")
    excerpt = models.CharField("摘要", max_length=150, default="无摘要")
    content = models.TextField("正文")
    category = models.ForeignKey(
        Category, verbose_name="类别", on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name="标签", blank=True)
    read_num = models.IntegerField("阅读人数", default=0)
    publish_time = models.DateTimeField("发布时间", auto_now_add=True)
    modify_time = models.DateTimeField("修改时间", auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('subject:article', kwargs={'id': self.pk})

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ["-modify_time"]


class Contact(models.Model):
    name = models.CharField("姓名", max_length=10)
    email = models.EmailField("邮箱")
    # subject = models.CharField("主题", max_length=150)
    message = models.TextField("信息")
    is_audit = models.BooleanField("审核", default=False)
    publish_time = models.DateTimeField("留言时间", auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "留言"
        verbose_name_plural = verbose_name
        ordering = ["-publish_time"]