BOT_NAME = 'Scrapy_CompanyMissionStatement'

SPIDER_MODULES = ['Scrapy_CompanyMissionStatement.spiders']
NEWSPIDER_MODULE = 'Scrapy_CompanyMissionStatement.spiders'

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 0.25

DOWNLOADER_MIDDLEWARES = {'scrapy_crawlera.CrawleraMiddleware': 300}
CRAWLERA_ENABLED = True
CRAWLERA_APIKEY = 'dd175571a64b4f558db54c896d02f026'