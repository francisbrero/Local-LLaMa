import scrapy
from scrapy.linkextractors import LinkExtractor

class Spider(scrapy.Spider):
    name = 'website'
    allowed_domains = ['support.madkudu.com/']
    start_urls = [
        'https://support.madkudu.com/'
        # ,'https://www.madkudu.com'
        # ,'https://www.madkudu.com/blog'
    ]

    def parse(self, response):
        # Extract all links using the LinkExtractor
        extractor = LinkExtractor(restrict_xpaths='//*[contains(@href,"/")]')
        links = extractor.extract_links(response)

        # Yield the URLs of all extracted links
        for link in links:
            print(link.url)
            yield {
                'url': link.url
            }
