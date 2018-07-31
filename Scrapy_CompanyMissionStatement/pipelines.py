from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter


class CSVPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        if spider.name != 'company_crawler':
            return
        file = open('result.csv', 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.fields_to_export = [
            'company', 'link', 'foundation', 'community_investment', 'community_focus', 'community_contribution',
            'community_engagement', 'community_education', 'local_investment', 'local_focus', 'local_contribution',
            'local_engagement', 'local_education', 'values_driven', 'mission_driven', 'funding_education_programs',
            'community_development', 'financial_knowledge', 'tools_and_training_programs', 'focusing_on_financial_needs',
            'financial_foundations', 'financial_programs', 'local_partnerships', 'promotion_of_volunteerism',
            'underserved_communities', 'education_progrmas', 'community_programs', 'community_financial_programs',
            'local_branch_programs', 'community_reinvestment', 'at_risk_populations', 'financial_literacy',
            'employee_education', 'at_risk_youth'
        ]
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        if spider.name != 'company_crawler':
            return
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        if spider.name != 'company_crawler':
            return item
        self.exporter.export_item(item)
        return item