from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from mailer import Mailer

process = CrawlerProcess(get_project_settings())

# starting crawling process
process.crawl('readme')
process.start()

# starting sending emails
mailer = Mailer()
mailer.start()
