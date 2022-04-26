# to run 
# scrapy crawl imdb_spider -o movies.csv
import scrapy
from scrapy.linkextractors import LinkExtractor

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'

    start_urls = ['https://www.imdb.com/title/tt0898266/']

    def parse(self,response):
        next_page = response.css("a[href*='fullcredits']").attrib["href"]
        if next_page: # identical to if next_page is not None
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_full_credits)

    def parse_full_credits(self, response):
        paths=[a.attrib["href"] for a in response.css("td.primary_photo a")]

        if paths:# identical to if path is not None
            for path in paths:
                actor=response.urljoin(path)
                yield scrapy.Request(actor, callback=self.parse_actor_page)

    def parse_actor_page(self,response):
        name=response.css(".header").css("span.itemprop::text").get()
        for movie in response.css("div.filmo-category-section::not([style*='displsy::none;']) b"):
            yield{
                "name":name,
                "movie_name":movie.css("a::text").get()
            }


    

