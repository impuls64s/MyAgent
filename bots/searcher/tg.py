from telethon import TelegramClient
from telethon.errors.rpcerrorlist import SessionPasswordNeededError


api_id = 23624680  # Replace with your Telegram API ID
api_hash = '0c5adec1271f738ef27ca9abf4553870'  # Replace with your Telegram API hash
phone = '+90 534 458 4252'
session_name = 'pop3'


async def create_session(session, api_id, api_hash, phone):
    client = TelegramClient(f'bots/sessions/{session}', api_id, api_hash)
    await client.connect()
    try:
        sent = await client.send_code_request(phone)
    except Exception as ex:
        raise ex
    finally:    
        await client.disconnect()
    return sent


async def complite_session(session, api_id, api_hash, phone, code, phone_code_hash, password):
    client = TelegramClient(f'bots/sessions/{session}', api_id, api_hash)
    await client.connect()
    try:
        sent = await client.sign_in(phone=phone, code=code, phone_code_hash=phone_code_hash)
    except SessionPasswordNeededError as e:
        sent = await client.sign_in(password=password)
    except Exception as ex:
        raise ex
    finally:
        await client.disconnect()
    return sent
