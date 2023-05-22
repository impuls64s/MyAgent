from telethon import TelegramClient
from telethon.errors.rpcerrorlist import SessionPasswordNeededError


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


async def complite_session(
        session, api_id, api_hash, phone,
        code, phone_code_hash, password):
    client = TelegramClient(f'bots/sessions/{session}', api_id, api_hash)
    await client.connect()
    try:
        sent = await client.sign_in(
            phone=phone, code=code, phone_code_hash=phone_code_hash)
    except SessionPasswordNeededError:
        sent = await client.sign_in(password=password)
    except Exception as ex:
        raise ex
    finally:
        await client.disconnect()
    return sent
