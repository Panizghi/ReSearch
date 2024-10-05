# interface for all crawlers

class BaseCrawler:
    def __init__(self, crawler):
        self.crawler = crawler
        
    def crawl(self):
        self.crawler.crawl()
        
    def get_data(self):
        return self.crawler.get_data()
    