from searcher.basic import BasicSearchBot, Tables


def main():
    bot = BasicSearchBot(
        session_name='bset69',
        api_id=23624680, 
        api_hash='0c5adec1271f738ef27ca9abf4553870',
        recipient='impuls_64',
        db_name='db.sqlite3',
        tables=Tables(
            messages='tables_chatmessage',
            keywords='29',
            excluded_words='30',
            blocked_users='tables_blockedusers'
        )
    )
    bot.start_bot()


if __name__ == '__main__':
    main()
