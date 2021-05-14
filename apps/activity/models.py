from django.db import models

from DjangoUeditor.models import UEditorField

from apps.utils.random_string_generator import generate_random_string


def upload_file_path(_, filename):
    extension = filename.split('.')[-1]
    name = generate_random_string(10, add_time_prefix=True)
    return name + '.' + extension


class Activity(models.Model):
    title = models.CharField(verbose_name='名称', max_length=200, null=False, blank=False)
    cover = models.ImageField(verbose_name='背景图', upload_to=upload_file_path, null=False, blank=True)
    content = UEditorField(verbose_name='内容', width=900, height=600, toolbars='mini', imagePath='',
                           filePath='', upload_settings={'imageMaxSize': 5 * 1024 * 1024}, settings={},
                           command=None, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    start_time = models.DateTimeField(verbose_name='开始时间')
    display = models.BooleanField(verbose_name='是否展示', default=True)

    class Meta:
        verbose_name = '活动'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
