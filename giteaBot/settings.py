BOT_NAME = 'giteaBot'

# gitea bot (user) credentials - it needs admin rights
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

SPIDER_MODULES = ['giteaBot.spiders']
NEWSPIDER_MODULE = 'giteaBot.spiders'

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 8
DOWNLOAD_DELAY = 0.35

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

ITEM_PIPELINES = {
    'giteaBot.pipelines.UserWriterPipeline': 300,
    'giteaBot.pipelines.RepoWriterPipeline': 600
}