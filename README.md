# Gitea Bot
A Python/Scrapy project, that runs spiders on gitea, finds repositories without README.md and sends the email to the owner.

## Requirements
- Python3
- Pip3
- Sqlite3

## Install requirements.txt
````shell
pip3 install -r requirements.txt
````

## Configuration
To make the bot working, you have to fill up settings in:
```./giteaBot/settings.py```

```
BOT_USER_NAME = ''
BOT_PASSWORD = ''

# gitea base url
BASE_URL = ''

MAIL_FROM = ''
MAIL_HOST = ''
MAIL_USER = ''
MAIL_PASS = ''

MAIL_TOPIC = ''
MAIL_CC = []
```

Example config:
```
BOT_USER_NAME = 'bot'
BOT_PASSWORD = 'secretPassword'

# gitea base url
BASE_URL = 'https://gitea.example.com'

MAIL_FROM = "\"Gitea Bot\" <bot@agiqon.email>"
MAIL_HOST = 'smtp.example.com'
MAIL_USER = 'userName'
MAIL_PASS = 'secretPassword'

MAIL_TOPIC = 'Missing README.md!'
MAIL_CC = ['cc1@email.com', 'cc2@email.com']
```

## Run (from project root)
````shell
python3 giteaBot/start.py
````

## Check database
````shell
sqlite3 database.db
````
