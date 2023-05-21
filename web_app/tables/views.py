from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Bot, Phrase, Table, ChatMessage, BlockedUsers
from bots.searcher.tg import create_session, complite_session
from bots.searcher.creator import create_bot_file, del_bot_file
import asyncio
from telethon.errors.rpcerrorlist import ApiIdInvalidError, PhoneNumberInvalidError, PhonePasswordFloodError
import subprocess
from .forms import BotForm, TableForm, PhraseForm, BlockedUsersForm
from django.urls import reverse
from django.contrib import messages
from django.db.models.deletion import ProtectedError


# Tables
def tables_view(request):
    tables = Table.objects.all()
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tables_view')
    else:
        form = TableForm()
    context = {'tables': tables, 'form': form, 'title': 'Таблицы'}
    return render(request, 'tab/tables.html', context)


def del_table(request):
    try:
        if request.method == 'POST':
            table_id = request.POST.get('table_id')
            table = Table.objects.get(pk=table_id)
            table.delete()
    except ProtectedError:
        messages.warning(request, 'Нельзя удалить таблицу, так как к ней привязан бот.')
    return redirect('tables_view')


# Phrases
def phrases_view(request, table_id):
    phrases = Phrase.objects.filter(table=table_id)
    if request.method == 'POST':
        form = PhraseForm(request.POST)
        if form.is_valid():
            phrase = form.save(commit=False)
            phrase.table_id = table_id
            phrase.save()
            return redirect(reverse('phrases_view', args=[table_id]))
    else:
        form = PhraseForm()
    context = {'phrases': phrases, 'form': form, 'title': 'Фразы'}
    return render(request, 'tab/phrases.html', context)


def del_phrase(request, phrase_id):
    if request.method == 'GET':
        phrase = Phrase.objects.get(pk=phrase_id)
        tab_id = phrase.table.pk
        phrase.delete()
    return redirect(reverse('phrases_view', args=[tab_id]))


def upd_phrase(request, phrase_id):
    phrase = Phrase.objects.get(pk=phrase_id)
    tab_id = phrase.table.pk
    if request.method == 'POST':
        form = PhraseForm(request.POST, instance=phrase)
        if form.is_valid():
            form.save()
            return redirect(reverse('phrases_view', args=[tab_id]))
    else:
        form = PhraseForm(instance=phrase)

    context = {'form': form}
    return render(request, 'tab/upd_phrase.html', context)


# Messages
def view_messages(request):
    msgs = ChatMessage.objects.all().order_by('-id')
    count_block_usr = BlockedUsers.objects.count()
    context = {'msgs': msgs, 'title': 'Сообщения', 'count_block_usr': count_block_usr}
    return render(request, 'msg/messages.html', context)


def msg_detail(request, msg_id):
    message = ChatMessage.objects.get(pk=msg_id)
    context = {'message': message, 'title': 'Детали сообщения'}
    return render(request, 'msg/msg_detail.html', context)


def view_blocked_users(request):
    blocked_users = BlockedUsers.objects.all().order_by('-id')
    
    if request.method == 'POST':
        form = BlockedUsersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_blocked_users')
    else:
        form = BlockedUsersForm()
    context = {'blocked_users': blocked_users, 'form': form, 'title': 'Заблокированные души'}
    return render(request, 'msg/blocked_users.html', context)


def del_blocked_user(request, usr_id):
    if request.method == 'GET':
        user = BlockedUsers.objects.get(pk=usr_id)
        user.delete()
        messages.info(request, 'Пользователь успешно освобожден.')
    return redirect('view_blocked_users')

# Bots
def view_bots(request):
    bots = Bot.objects.all().order_by('-id')
    context = {'bots': bots, 'title': 'Список ботов'}
    return render(request, 'bots/bots.html', context)


def create_bot(request):
    if request.method == 'POST':
        form = BotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_bots')
    else:
        form = BotForm()
    context = {'form': form, 'title': 'Создание бота', 'button': 'Создать'}
    return render(request, 'bots/create_bot.html', context)


def edit_bot(request, bot_id):
    bot = Bot.objects.get(pk=bot_id)
    if request.method == 'POST':
        form = BotForm(request.POST, instance=bot)
        if form.is_valid():
            form.save()
            return redirect('view_bots')
    else:
        form = BotForm(instance=bot)
    context = {'form': form, 'title': 'Изменение бота', 'button': 'Изменить'}
    return render(request, 'bots/create_bot.html', context)


def del_bot(request, bot_id):
    if request.method == 'GET':
        bot = Bot.objects.get(pk=bot_id)
        del_bot_file(bot.session_name, bot.activated)
        bot.delete()
        messages.info(request, 'Бот успешно удален.')
    return redirect('view_bots')


def send_code(request, bot_id):
    bot = Bot.objects.get(pk=bot_id)
    if request.method == 'GET':
        try:
            resp_tg = asyncio.run(
                create_session(
                    bot.session_name,
                    bot.api_id,
                    bot.api_hash,
                    bot.phone
                )
            )
        except PhoneNumberInvalidError:
            messages.error(request, 'Номер телефона недействителен.')
            return redirect('view_bots')
            
        except ApiIdInvalidError:
            messages.error(request, 'Не правильно указан Api ID или Api Hash.')
            return redirect('view_bots')
        
        except PhonePasswordFloodError:
            messages.error(request, 'Вы пытались войти слишком много раз.')
            return redirect('view_bots')

        else:
            bot.phone_code_hash = resp_tg.phone_code_hash
            bot.save()
    
    context = {'phone': bot.phone, 'bot_id': bot_id, 'title': 'Активация бота'}
    return render(request, 'bots/activate.html', context)


def activate_bot(request, bot_id):
    bot = Bot.objects.get(pk=bot_id)
    if request.method == 'POST':
        try:
            code = request.POST.get('code')
            resp_tg = asyncio.run(
                complite_session(
                    bot.session_name, 
                    bot.api_id, 
                    bot.api_hash, 
                    bot.phone,
                    code,
                    bot.phone_code_hash,
                    bot.password
                )
            )
            bot.activated = True
            bot.save()
 
        except Exception as ex:
            messages.error(request, 'Недействительный  пароль от Telegram или Код.')

        else:
            create_bot_file(bot)
            messages.success(request, 'Бот успешно создан, перейдите в "Диспетчер" для управления.')

    return redirect('view_bots')