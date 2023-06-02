from django.db import models
from django.contrib.auth.models import User


class Table(models.Model):
    name = models.CharField(
        max_length=40,
        verbose_name='Название')
    description = models.TextField(
        max_length=75,
        verbose_name='Описание',
        blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Таблица'
        verbose_name_plural = 'Таблицы'

    def __str__(self):
        return self.name


class Phrase(models.Model):
    phrase = models.CharField(
        max_length=100,
        verbose_name='Фраза')
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name='tab_phrases')

    class Meta:
        unique_together = ('phrase', 'table')
        verbose_name = 'Фраза'
        verbose_name_plural = 'Фразы'

    def __str__(self):
        return self.phrase


class BlockedUsers(models.Model):
    tg_user_id = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
        verbose_name='Telegram User ID')
    tg_username = models.CharField(
        max_length=100,
        blank=True,
        null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Заблокированный пользователь'
        verbose_name_plural = 'Заблокированные пользователи'

    def __str__(self):
        return f'{self.tg_username} | {self.tg_user_id}'


class ChatMessage(models.Model):
    phrase = models.CharField(max_length=200)
    message = models.TextField()
    url_message = models.CharField(max_length=200)
    first_name = models.CharField(max_length=120, null=True)
    last_name = models.CharField(max_length=120, null=True)
    tg_user_id = models.IntegerField()
    username = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    session = models.CharField(max_length=40)
    created_at = models.DateTimeField()

    class Meta:
        verbose_name = 'Сообщение из чата'
        verbose_name_plural = 'Сообщения из чатов'

    def __str__(self):
        return self.message


class Bot(models.Model):
    activated = models.BooleanField(default=False)
    api_id = models.IntegerField()
    api_hash = models.CharField(max_length=50)
    session_name = models.CharField(
        max_length=40,
        verbose_name='Сессия',
        unique=True,
        help_text='Только английские буквы, цифры и _')
    phone = models.CharField(
        max_length=30,
        verbose_name='Номер телефона',
        help_text='От Telegram аккаунта')
    phone_code_hash = models.CharField(max_length=30, blank=True)
    password = models.CharField(
        max_length=10,
        verbose_name='Пароль',
        help_text='Облачный пароль, если его нет то 1234')
    recipient = models.CharField(
        max_length=30,
        verbose_name='Получатель',
        help_text='Telegram для получения уведомлений без @')
    keywords_table = models.ForeignKey(
        Table,
        related_name='tab_keywords',
        on_delete=models.PROTECT,
        verbose_name='Ключевые фразы')
    excluded_words_table = models.ForeignKey(
        Table,
        related_name='tab_excluded',
        on_delete=models.PROTECT,
        verbose_name='Фразы исключения')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Конфигурация бота'
        verbose_name_plural = 'Конфигурации ботов'

    def __str__(self):
        return f'Сессия: {self.session_name} | Номер: {self.phone}'
    
    def get_file_name(self):
        return f'{self.owner}_{self.session_name}'
