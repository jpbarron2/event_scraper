# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest




class FCrawlerSpider(scrapy.Spider):
    name = 'f_crawler'
    allowed_domains = ['google.com']
    start_urls = ['https://google.com/']
    city_list = []
    f = "/Users/jasonbarron/Documents/Code_Work/crawler/support_files/gistfile1.txt"
    with open(f, 'r') as file:
        for i in range(55):
            data = file.readline()
            if i >= 5:
                line = data.split(",")
                city = line[1] + ", " + line[2]
                city_list.append(city)
                file.closed
    print(city_list)
    a = 0
    def parse(self, response):
        for city in self.city_list:    
            search = city
            yield FormRequest.from_response(response, formdata = {
                'q': search +" fireworks show 2019"
            }, callback= self.start_scraping)
    
    def start_scraping(self, response):
        event_title = response.css('.BjJfJf::text').extract()
        event_time = response.css('.k8RiQ:nth-child(1)').css('::text').extract()
        event_add = response.css('.nsol9b:nth-child(2)').css('::text').extract()
        event_city = response.css('.nsol9b+ .nsol9b').css('::text').extract()
        yield{'city': event_city, 'title': event_title, 'time': event_time, 'address': event_add}