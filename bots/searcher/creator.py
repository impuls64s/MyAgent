import configparser
import os
import subprocess


def parsing_data(data) -> dict:
    settings = {
        'SESSION_NAME': data.get_file_name(),
        'API_ID': str(data.api_id),
        'API_HASH': data.api_hash,
        'RECIPIENT': data.recipient,
        'KEYWORDS': str(data.keywords_table.id),
        'EXCLUDED_WORDS': str(data.excluded_words_table.id),
    }
    return settings


def create_py(bot: dict) -> None:

    bot_info = parsing_data(bot)

    with open('bots/searcher/bot.example', 'r') as file:
        content = file.read()

    for key, value in bot_info.items():
        content = content.replace(key, value)

    name = bot_info.get('SESSION_NAME')
    with open(f'bots/{bot.get_file_name()}.py', 'w') as file:
        file.write(content)


def create_conf(name):
    config = configparser.ConfigParser()
    config[f'program:{name}'] = {
                        'command': f'python3 bots/{name}.py',
                        'environment': 'PYTHONUNBUFFERED=1',
                        'autostart': 'false',
                        'stdout_logfile': f'logs/{name}.log',
                        'stderr_logfile': f'logs/{name}_error.log',
    }
    with open(f'conf.d/{name}.conf', 'w') as configfile:
        config.write(configfile)


def create_bot_file(bot):
    create_py(bot)
    create_conf(bot.get_file_name())
    subprocess.run(['supervisorctl', 'reread'])
    subprocess.run(['supervisorctl', 'add', bot.get_file_name()])



def del_bot_file(file_name: str, activated: bool):
    
    try:
        os.remove(f'bots/sessions/{file_name}.session')
    except FileNotFoundError:
        print('not file session')

    if activated:
        subprocess.run(['supervisorctl', 'remove', file_name])

        try:
            os.remove(f'conf.d/{file_name}.conf')
        except FileNotFoundError:
            print('not file conf')

        try:
            os.remove(f'logs/{file_name}.log')
            os.remove(f'logs/{file_name}_error.log')
        except FileNotFoundError:
            print('not file logs')
        
        try:
            os.remove(f'bots/{file_name}.py')
        except FileNotFoundError:
            print('not file py')



