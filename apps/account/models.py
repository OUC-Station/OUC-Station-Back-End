from django.db import models


class Account(models.Model):
    openid = models.CharField(verbose_name='openid', max_length=255, null=False, blank=False)
    unionid = models.CharField(verbose_name='unionid', max_length=255, null=True)

    nick_name = models.CharField(verbose_name='昵称', max_length=255, null=True)
    avatar = models.CharField(verbose_name='头像', max_length=1000, null=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nick_name if self.nick_name else '用户'
