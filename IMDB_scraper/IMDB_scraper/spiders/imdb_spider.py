# to run 
# scrapy crawl imdb_spider -o movies.csv
import scrapy
from scrapy.linkextractors import LinkExtractor

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'

    start_urls = ['https://www.imdb.com/title/tt0898266/']

    def parse(self, response):
        link = response.css("a[href*='fullcredits']").attrib["href"]
        if link: # identical to if next_page is not None
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_full_credits)

    def parse_full_credits(self, response):
        paths=[a.attrib["href"] for a in response.css("td.primary_photo a")]

        if paths:# identical to if path is not None
            for path in paths:
                actor=response.urljoin(path)
                yield scrapy.Request(actor, callback=self.parse_actor_page)

    def parse_actor_page(self, response) :
        name=response.css(".header").css("span.itemprop::text").get()
        movies=response.css("div.filmo-row b")
        for movie in movies:
            yield{
                "name":name,
                "movie_name":movie.css("a::text").get()
            }


    

