from searcher.basic import BasicSearchBot, Tables


def main():
    bot = BasicSearchBot(
        session_name='oleg_test8',
        api_id=23624680, 
        api_hash='0c5adec1271f738ef27ca9abf4553870',
        recipient='impuls_64',
        db_name='db.sqlite3',
        tables=Tables(
            messages='tgparser_chatmessage',
            keywords='1',
            excluded_words='2',
            blocked_users='tgparser_blockedusers'
        )
    )
    bot.start_bot()


if __name__ == '__main__':
    main()
