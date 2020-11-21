from django.db import models

# Create your models here.
class Paste(models.Model):
    name = models.CharField("用户", max_length=15)
    message = models.TextField("信息")
    code_class = models.CharField("语言", default="nohighlight",  max_length=15)
    valid_day = models.IntegerField("有效时间", default=3)
    is_audit = models.BooleanField("审核", default=True)
    publish_time = models.DateTimeField("提交时间", auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "文本展示"
        verbose_name_plural = verbose_name
        ordering = ["-publish_time"]
