import scrapy
import csv
import re
from urllib.parse import urljoin
from Scrapy_CompanyMissionStatement.items import CompanymissionstatementItem


class CompanyCrawler(scrapy.Spider):
    name = 'company_crawler'
    phrase_list = ['community investment', 'community focus', 'community contribution', 'community engagement',
                   'community education', 'local investment', 'local focus', 'local contribution',
                   'local engagement', 'local education']

    def start_requests(self):
        company_list = []
        link_list = []

        # reader = csv.reader(open('company_link_list.csv', newline=''), delimiter='\t', quotechar='|')
        # is_first = True
        # for row in reader:
        #     if not is_first:
        #         company_list.append(row[0].split(',')[0])
        #         link_list.append(row[0].split(',')[1])
        #     is_first = False
        #
        # for i in range(len(company_list)):
        #     item = CompanymissionstatementItem()
        #     item['company'] = company_list[i].strip()
        #     item['link'] = link_list[i].strip()
        #     if 'http' in item['link'] and 'www..com/' not in item['link']:
        #         yield scrapy.Request(
        #             url=item['link'],
        #             callback=self.parse_page,
        #             meta={'item': item},
        #             dont_filter=True
        #         )

        item = CompanymissionstatementItem()
        # item['company'] = company_list[i]
        # item['link'] = link_list[i]
        yield scrapy.Request(
            url='https://www.efirstbank.com/',
            callback=self.parse_page,
            meta={'item': item},
        )

    def parse_page(self, response):
        item = response.meta.get('item')
        item['Foundation'] = 'No'
        item['number_of_matches'] = 0

        for phrase in self.phrase_list:
            if 'Foundation' in response.body_as_unicode():
                item['Foundation'] = 'Yes'
            if phrase in response.body_as_unicode():
                item['number_of_matches'] = len(re.findall(phrase, response.body_as_unicode()))
            phrase_text = response.xpath('//*[contains(text(), "'+phrase+'")]')
            if len(phrase_text) > 0:
                for p in phrase_text:
                    item['phrase'] = phrase
                    item['mission'] = p.xpath('./text()').extract_first()
                    yield item
            phrase_content = response.xpath('//*[contains(@content, "'+phrase+'")]')
            if len(phrase_content) > 0:
                for p in phrase_content:
                    item['phrase'] = phrase
                    item['mission'] = p.xpath('./@content').extract_first()
                    yield item

        about_link = response.xpath('//a[contains(text(), "About")]/@href').extract_first()

        if '.com/about' in response.url.lower() and item['number_of_matches'] == 0:
            yield item

        elif item['number_of_matches'] == 0 and about_link:
            yield scrapy.Request(
                url=urljoin(response.url, about_link),
                callback=self.parse_page,
                meta={'item': item},
            )

        elif item['number_of_matches'] == 0:
            yield item
