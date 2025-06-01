from django.db import models

# Create your models here.

class Task(models.Model):
    GENRE_CHOICES = [
        ('work', '仕事'),
        ('private', 'プライベート'),
        ('other', 'その他'),
    ]

    PRIORITY_CHOICES = [
        (1, '低'),
        (2, 'やや低'),
        (3, '中'),
        (4, 'やや高'),
        (5, '高'),
    ]

    title = models.CharField('タスク名', max_length=200)
    memo = models.TextField('メモ', blank=True)
    genre = models.CharField('ジャンル', max_length=20, choices=GENRE_CHOICES)
    priority = models.IntegerField('重要度', choices=PRIORITY_CHOICES)
    is_completed = models.BooleanField('完了', default=False)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = 'タスク'
        verbose_name_plural = 'タスク'

    def __str__(self):
        return self.title
