import scrapy

class ACMSpider(scrapy.Spider):
    name = 'acm_spider'
    start_urls = ['https://dl.acm.org/profile/81100093619/publications?Role=author']

    def parse(self, response):
        # Extract publications from the current page
        publications = response.css('li.search__item.issue-item-container')
        for pub in publications:
            title_tag = pub.css('h5.issue-item__title a')
            title = title_tag.css('::text').get()
            relative_url = title_tag.css('::attr(href)').get()

            if relative_url:
                full_url = response.urljoin(relative_url)
                # Follow the URL to fetch the full abstract
                yield scrapy.Request(
                    full_url,
                    callback=self.parse_abstract,
                    meta={'title': title, 'url': full_url}
                )

        # Handle pagination
        next_page = response.css('a.pagination__btn--next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_abstract(self, response):
        # Extract the abstract text
        abstract_section = response.css('div[role="paragraph"]::text').get()
        yield {
            'Title': response.meta['title'],
            'URL': response.meta['url'],
            'Full Abstract': abstract_section.strip() if abstract_section else "Abstract not found or failed to load."
        }
