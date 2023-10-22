import scrapy
from bookscraper.items import BookItem


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        
        books = response.css('article.product_pod')

        for book in books:

            relative_url = book.css('h3 a').attrib['href']
            
            if "catalogue/" in relative_url:
                book_url = "http://books.toscrape.com/" + relative_url
            else:
                book_url = "http://books.toscrape.com/catalogue/" + relative_url
            
                yield response.follow(book_url, callback = self.parse_book_page)    


        
        
        next_page = response.css('li.next a').attrib['href']

        if next_page is not None:
            if "catalogue/" in next_page:
                next_page_url = "http://books.toscrape.com/" + next_page
            else:
                next_page_url = "http://books.toscrape.com/catalogue/" + next_page


            yield response.follow(next_page_url , callback =  self.parse)

    def parse_book_page(self,response):
            
            table_rows = response.css('table tr')
            book_item = BookItem()
                
            book_item["url"] = response.url,
            book_item["title"] = response.css('div.product_main h1 ::text').get(),
            book_item["category"] = response.xpath("//ul[@class='breadcrumb']/li[3]/a/text()").get(),
            book_item["price"] =  response.css('div.product_main p.price_color ::text').get(),
            book_item["price_excl_tax"] = table_rows[2].css('td ::text').get(),
            book_item["price_incl_tax"] = table_rows[3].css('td ::text').get(),
            book_item["tax"] = table_rows[4].css('td ::text').get(),
            book_item["availability"] = table_rows[5].css('td ::text').get(),
            book_item["number_of_reviews"] = table_rows[6].css('td ::text').get(),
            book_item["rating"] = response.css('p.star-rating').attrib['class'],
            book_item["description"] = response.xpath("//*[@id='content_inner']/article/p/text()").get(),

            yield book_item