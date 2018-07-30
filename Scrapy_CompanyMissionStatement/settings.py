BOT_NAME = 'Scrapy_CompanyMissionStatement'

SPIDER_MODULES = ['Scrapy_CompanyMissionStatement.spiders']
NEWSPIDER_MODULE = 'Scrapy_CompanyMissionStatement.spiders'

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 0.25

ITEM_PIPELINES = {'Scrapy_CompanyMissionStatement.pipelines.CSVPipeline': 300 }