from django.db import models

from apps.utils.random_string_generator import generate_random_string


def upload_file_path(_, filename):
    extension = filename.split('.')[-1]
    name = generate_random_string(10, add_time_prefix=True)
    return name + '.' + extension


class Location(models.Model):
    name = models.CharField(verbose_name='名称', max_length=200, null=False, blank=False)
    introduction = models.TextField(verbose_name='介绍', null=False, blank=True, default='')
    remark = models.TextField(verbose_name='备注', null=False, blank=True, default='')

    icon = models.ImageField(verbose_name='图标', upload_to=upload_file_path, null=False, blank=True)
    image = models.ImageField(verbose_name='背景图', upload_to=upload_file_path, null=False, blank=True)

    address = models.CharField(verbose_name='地址', max_length=200, null=False, blank=True, default='')
    longitude = models.FloatField(verbose_name='经度', null=True, blank=True)
    latitude = models.FloatField(verbose_name='纬度', null=True, blank=True)

    class Meta:
        verbose_name = '位置'
        verbose_name_plural = verbose_name
