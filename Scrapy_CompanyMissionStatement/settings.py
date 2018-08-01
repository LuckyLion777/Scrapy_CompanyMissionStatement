BOT_NAME = 'Scrapy_CompanyMissionStatement'

SPIDER_MODULES = ['Scrapy_CompanyMissionStatement.spiders']
NEWSPIDER_MODULE = 'Scrapy_CompanyMissionStatement.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 10
DOWNLOAD_DELAY = 4
DOWNLOAD_TIMEOUT = 4

ITEM_PIPELINES = {'Scrapy_CompanyMissionStatement.pipelines.CSVPipeline': 300 }