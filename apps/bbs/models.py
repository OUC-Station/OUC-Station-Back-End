from django.db import models


class Topic(models.Model):
    account = models.ForeignKey('account.Account', verbose_name='用户', on_delete=models.CASCADE)
    anonymous = models.BooleanField(verbose_name='是否匿名', default=False)

    title = models.CharField(verbose_name='标题', max_length=100, null=False, blank=False)
    content = models.TextField(verbose_name='内容', null=False, blank=False)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '主题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class Comment(models.Model):
    account = models.ForeignKey('account.Account', verbose_name='用户', on_delete=models.CASCADE)
    anonymous = models.BooleanField(verbose_name='是否匿名', default=False)
 
    topic = models.ForeignKey('bbs.Topic', verbose_name='主题', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='内容', null=False, blank=False)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content
