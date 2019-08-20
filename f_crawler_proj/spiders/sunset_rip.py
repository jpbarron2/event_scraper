# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class SunsetRipSpider(scrapy.Spider):
    name = 'sunset_rip'
    allowed_domains = ['sunrise-sunset.org']
    start_urls = ['https://sunrise-sunset.org/']
    city_list = ['New York, New York', 'Los Angeles, California', 'Chicago, Illinois', 'Houston, Texas', 'Philadelphia, Pennsylvania', 'Phoenix, Arizona', 'San Antonio, Texas', 'San Diego, California', 'Dallas, Texas', 'San Jose, California', 'Austin, Texas', 'Indianapolis, Indiana', 'Jacksonville, Florida', 'San Francisco, California', 'Columbus, Ohio', 'Charlotte, North Carolina', 'Fort Worth, Texas', 'Detroit, Michigan', 'El Paso, Texas', 'Memphis, Tennessee', 'Seattle, Washington', 'Denver, Colorado', 'Washington, District of Columbia', 'Boston, Massachusetts', 'Nashville-Davidson, Tennessee', 'Baltimore, Maryland', 'Oklahoma City, Oklahoma', 'Louisville/Jefferson County, Kentucky', 'Portland, Oregon', 'Las Vegas, Nevada', 'Milwaukee, Wisconsin', 'Albuquerque, New Mexico', 'Tucson, Arizona', 'Fresno, California', 'Sacramento, California', 'Long Beach, California', 'Kansas City, Missouri', 'Mesa, Arizona', 'Virginia Beach, Virginia', 'Atlanta, Georgia', 'Colorado Springs, Colorado', 'Omaha, Nebraska', 'Raleigh, North Carolina', 'Miami, Florida', 'Oakland, California', 'Minneapolis, Minnesota', 'Tulsa, Oklahoma', 'Cleveland, Ohio', 'Wichita, Kansas', 'Arlington, Texas']

    def parse(self, response):
        for city in self.city_list:
            yield FormRequest.from_response(response, formdata = {
                'location': city}, callback= self.nav_to_jul)

    def nav_to_jul(self, response):
        nextpage = response.css('.nextmonth a').css('::attr("href")').extract_first()
        if nextpage:
            yield scrapy.Request(response.urljoin(nextpage), callback=self.scrape_sunset)

    def scrape_sunset(self, response):
        open_in_browser(response)
        # city_sunset = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "day", " " )) and (((count(preceding-sibling::*) + 1) = 6) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "sunset", " " ))]/@innerText').extract()
        
        h1 = response.css('h1::text').extract()
        half_h1 = h1[0].split("in")
        list_city = half_h1[1]
        list_city = list_city.split(',')
        city = list_city[0]
        city = city.lstrip()
        yield{'city': city, 'sunset': ""}
