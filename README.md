# Company Mission Statement
This is a Scrapy project to scrape mission statements from any kinds company websites worldwide.


## Spiders

This project contains two spiders and you can list them using the `list` command:

    $ scrapy list
    company_crawler
    company_link_crawler

company_link_crawler spider reads company names from Excel file, then extracts/produces company website link
from google and write it to csv file, exam: company_link_list.csv

company_crawler spider reads company website links from csv file and extracts mission statements from those websites.


## Running the spiders
    $ scrapy crawl company_link_crawler -o company_link_list.csv
    $ scrapy crawl company_crawler -o result.csv
