import configparser
import os
import subprocess


def parsing_data(data) -> dict:
    settings = {
        'SESSION_NAME': data.session_name,
        'API_ID': str(data.api_id),
        'API_HASH': data.api_hash,
        'RECIPIENT': data.recipient,
        'KEYWORDS': str(data.keywords_table.id),
        'EXCLUDED_WORDS': str(data.excluded_words_table.id),
    }
    return settings


def create_py(data: dict) -> None:

    bot_info = parsing_data(data)

    with open('bots/searcher/bot.example', 'r') as file:
        content = file.read()

    for key, value in bot_info.items():
        content = content.replace(key, value)

    name = bot_info.get('SESSION_NAME')
    with open(f'bots/bot_{name}.py', 'w') as file:
        file.write(content)


def create_conf(name):
    config = configparser.ConfigParser()
    config[f'program:bot_{name}'] = {
                        'command': f'.venv/bin/python bots/bot_{name}.py',
                        'directory': '/home/impuls_64/agency/',
                        'environment': 'PYTHONUNBUFFERED=1',
                        'autostart': 'false',
                        'stdout_logfile': f'logs/bot_{name}.log',
                        'stderr_logfile': f'logs/bot_{name}_error.log',
    }
    with open(f'conf.d/bot_{name}.conf', 'w') as configfile:
        config.write(configfile)


def create_bot_file(bot):
    create_py(bot)
    create_conf(bot.session_name)
    subprocess.run(['supervisorctl', 'reread'])
    subprocess.run(['supervisorctl', 'add', f'bot_{bot.session_name}'])



def del_bot_file(session: str, activated: bool):
    
    try:
        os.remove(f'bots/sessions/{session}.session')
    except FileNotFoundError:
        print('not file session')

    if activated:
        subprocess.run(['supervisorctl', 'stop', f'bot_{session}'])
        subprocess.run(['supervisorctl', 'remove', f'bot_{session}'])

        try:
            os.remove(f'conf.d/bot_{session}.conf')
        except FileNotFoundError:
            print('not file conf')

        try:
            os.remove(f'logs/bot_{session}.log')
            os.remove(f'logs/bot_{session}_error.log')
        except FileNotFoundError:
            print('not file conf')
        
        try:
            os.remove(f'bots/bot_{session}.py')
        except FileNotFoundError:
            print('not file py')



