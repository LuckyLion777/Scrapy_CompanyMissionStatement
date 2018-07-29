import scrapy
import csv
import re
import requests
from urllib.parse import urljoin
import urllib.request
from Scrapy_CompanyMissionStatement.items import CompanymissionstatementItem


class CompanyCrawler(scrapy.Spider):
    name = 'company_crawler'
    phrase_list = []
    content_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.99 Safari/537.36',
    }

    def start_requests(self):
        company_list = []
        link_list = []

        reader = csv.reader(open('company_link_list.csv', newline=''), delimiter='\t', quotechar='|')
        is_first = True
        for row in reader:
            if not is_first:
                company_list.append(row[0].split(',')[0])
                link_list.append(row[0].split(',')[1])
            is_first = False

        for i in range(len(company_list)):
            item = CompanymissionstatementItem()
            self.phrase_list = [p for p in list(item.fields.keys()) if p not in {'company', 'link', 'foundation'}]
            for p in self.phrase_list:
                item[p] = 0
            item['company'] = company_list[i].strip()
            item['link'] = link_list[i].strip()
            if 'http' in item['link'] and 'www..com/' not in item['link']:
                yield scrapy.Request(
                    url=item['link'],
                    callback=self.parse_page,
                    meta={'item': item},
                    headers=self.headers,
                    dont_filter=True
                )

        # item = CompanymissionstatementItem()
        # self.phrase_list = [p for p in list(item.fields.keys()) if p not in {'company', 'link', 'foundation'}]
        # for p in self.phrase_list:
        #     item[p] = 0
        # # item['company'] = company_list[i]
        # # item['link'] = link_list[i]
        # yield scrapy.Request(
        #     url='https://www.unionbank.com/',
        #     callback=self.parse_page,
        #     meta={'item': item},
        #     headers=self.headers,
        # )

    def parse_page(self, response):
        item = response.meta.get('item')
        item['foundation'] = 'No'
        if 'foundation' in response.body_as_unicode():
            item['foundation'] = 'Yes'

        item = get_phrase_matches(self.phrase_list, response.body_as_unicode().lower(), self.content_list, item)
        self.content_list.append(response.body_as_unicode().lower())

        href_list = list(set(response.xpath('*//a/@href').extract()))
        about_link = response.xpath('//a[contains(text(), "About")]/@href').extract()
        if len(about_link) > 0:
            href_list.insert(0, about_link[0])
        if len(href_list) > 1:
            for href in href_list[:10]:
                if 'mailto:' in href:
                    continue
                link = urljoin(response.url, href)
                # with urllib.request.urlopen(link) as temp_response:
                #     if response.url in temp_response:
                if response.url in link:
                    try:
                        content = requests.get(link, timeout=5).text.lower()
                        item = get_phrase_matches(self.phrase_list, content, self.content_list, item)
                        self.content_list.append(content)
                        if 'foundation' in content:
                            item['foundation'] = 'Yes'
                    except requests.exceptions.RequestException as e:
                        print(e)

        yield item


def get_phrase_matches(phrase_list, content, content_list, item):
    if content in content_list:
        return item
    for phrase in phrase_list:
        keyword = phrase.replace('_', ' ')
        item[phrase] += len(re.findall(keyword, content))
        if len(re.findall(keyword, content)) > 0:
            print(5)
    return item
