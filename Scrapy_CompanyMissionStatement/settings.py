BOT_NAME = 'Scrapy_CompanyMissionStatement'

SPIDER_MODULES = ['Scrapy_CompanyMissionStatement.spiders']
NEWSPIDER_MODULE = 'Scrapy_CompanyMissionStatement.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 10
DOWNLOAD_DELAY = 4
DOWNLOAD_TIMEOUT = 4

MEDIA_ALLOW_REDIRECTS = True
HTTPERROR_ALLOW_ALL = True

ITEM_PIPELINES = {'Scrapy_CompanyMissionStatement.pipelines.CSVPipeline': 301}

DOWNLOADER_MIDDLEWARES = {'scrapy_crawlera.CrawleraMiddleware': 300}
CRAWLERA_ENABLED = True
CRAWLERA_APIKEY = '*** API_KEY HERE ***'
