from dataclasses import dataclass
from typing import List

from telethon.sync import TelegramClient, events

from .db import SQLiteDB


@dataclass
class Tables:
    messages: str
    keywords: str = 'tables_keywords'
    excluded_words: str = 'tables_excludedwords'
    blocked_users: str = 'tables_blockedusers'


class BasicSearchBot:
    def __init__(
            self,
            session_name: str,
            api_id: int,
            api_hash: str,
            recipient: int,
            tables: Tables, 
            db_name: str = 'db.sqlite3'
        ) -> None:

        self.client = TelegramClient(f'bots/sessions/{session_name}', api_id, api_hash)
        self.db = SQLiteDB(db_name)
        self.recipient = recipient
        self.tables = tables
        self.session = session_name

    @staticmethod
    def phrase_search(text: str, words: List[str]) -> list:
        result = [word for word in words if word.lower() in text.lower()]
        return result

    @staticmethod
    async def message_parser(
            event: events.NewMessage.Event,
            keywords: list, session) -> dict:
        
        chat = await event.get_chat()
        sender = await event.get_sender()
        chat_name = chat.username
        link_to_msg = f'https://t.me/{chat_name}/{event.message.id}'
        new_data = {
            'first_name': sender.first_name,
            'last_name': sender.last_name,
            'username': sender.username,
            'tg_user_id': int(sender.id),
            'phone': sender.phone,
            'phrase': ', '.join(keywords),
            'message': event.message.message,
            'url_message': link_to_msg,
            'session': session,
            'created_at': event.message.date.strftime('%Y-%m-%d %H:%M:%S')
        }
        return new_data

    def validator(self, text: str, sender_id: int) -> bool:
        lst_keywords = self.db.get_phrases(self.tables.keywords)
        keywords = self.phrase_search(text, lst_keywords)
        if not keywords:
            return False
        
        lst_excluded_words = self.db.get_phrases(self.tables.excluded_words)
        excluded_words = self.phrase_search(text, lst_excluded_words)
        if excluded_words:
            return False
        
        lst_blocked_users = self.db.get_blocked_users(self.tables.blocked_users)
        if sender_id in lst_blocked_users:
            return False

        return keywords

    async def chat_reader(self, event: events.NewMessage.Event):
            text = event.message.message
            print(event.message.date.strftime('%Y-%m-%d %H:%M:%S'), event.message.message)

            valid_data = self.validator(text, event.message.sender_id)
            if valid_data:
                print(f'[+] Получил данные')
                
                # Парсим данные
                new_data = await self.message_parser(event, valid_data, self.session)
                
                # Заносим данные в БД
                self.db.insert_data(new_data, self.tables.messages, self.session)
                
                # Отправляем ссылку получателю
                await self.client.send_message(self.recipient, new_data.get('url_message'))

    def start_bot(self):
        # Проверка наличия таблиц в БД
        # name_tables = list(vars(self.tables).values())
        # self.db.check_tables(name_tables)

        self.client.on(events.NewMessage)(self.chat_reader)
        
        self.client.start()
        self.client.run_until_disconnected()
