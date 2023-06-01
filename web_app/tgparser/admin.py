from django.contrib import admin
from .models import BlockedUsers, ChatMessage, Bot,Phrase, Table


@admin.register(Phrase)
class PhrasesAdmin(admin.ModelAdmin):
    list_display = ('id', 'phrase', 'table_id')
    list_display_links = ('id', 'phrase', 'table_id')
    list_filter = ('table_id',)


@admin.register(Table)
class TablesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(BlockedUsers)
class BlockedUsersAdmin(admin.ModelAdmin):
    list_display = ('tg_user_id', 'tg_username')
    list_display_links = ('tg_user_id', 'tg_username')


@admin.register(ChatMessage)
class MersinChatMessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'phrase', 'message', 'first_name', 'last_name', 'username', 'created_at')
    list_display_links = ('id', 'phrase', 'message')


@admin.register(Bot)
class BotsAdmin(admin.ModelAdmin):
    list_display = ('id', 'activated', 'session_name', 'phone', 'recipient')
    list_display_links = ('id', 'session_name', 'phone', 'recipient')
