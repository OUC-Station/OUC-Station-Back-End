from django.db import models


class Suggestion(models.Model):
    account = models.ForeignKey('Account', verbose_name='用户', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='内容', null=False, blank=False)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    reply = models.TextField(verbose_name='回复', null=False, blank=False)

    class Meta:
        verbose_name = '意见'
        verbose_name_plural = verbose_name
