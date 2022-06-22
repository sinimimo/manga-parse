import scrapy

class mangaSpider(scrapy.Spider):
    name = 'manga'
    start_urls = ['https://www.bookvoed.ru/books?genre=1585&offset=0&pages=15&page=15&_part=books']
    
    def parse(self, response):
        for link in response.css('div.ls.ms a::attr(href)'):
            yield response.follow(link, callback=self.parse_manga)
        
        for i in range(1,50):
            next_page = f'https://www.bookvoed.ru/books?genre=1585&offset={60*i}&pages=15&page=15&_part=books'
            yield response.follow(next_page, callback=self.parse)
        
    def parse_manga(self, response):
        yield{
            'title': response.css('h1.MC span::text').get(),
            'review': response.css('div.Ur span::text').get(),
            'numberReviews': response.css('div.Ur span::text')[1].get().split()[0],
            'creator': response.css('div.a4::text').get(),
            'price': response.css('div.CC::text').get().replace('₽', '').replace(' ', '').strip(),
            'inStock': response.css('span.rC::text').get()
        }