import scrapy
import logging


class ACMSpider(scrapy.Spider):
    name = 'acm_spider'

    # Deduplicated start URLs
    start_urls = [
        'https://dl.acm.org/profile/81100344510/publications?Role=author',
        'https://dl.acm.org/profile/81100211852/publications?Role=author',
        'https://dl.acm.org/profile/81452592989/publications?Role=author',
        'https://dl.acm.org/profile/81100531409/publications?Role=author',
        'https://dl.acm.org/profile/81100545139/publications?Role=author',
        'https://dl.acm.org/profile/81100539349/publications?Role=author',
        'https://dl.acm.org/profile/81100089034/publications?Role=author',
        'https://dl.acm.org/profile/81451593001/publications?Role=author',
        'https://dl.acm.org/profile/81100267677/publications?Role=author',
        'https://dl.acm.org/profile/81100091376/publications?Role=author',
        'https://dl.acm.org/profile/81332515695/publications?Role=author',
        'https://dl.acm.org/profile/81100515854/publications?Role=author',
        'https://dl.acm.org/profile/81100107568/publications?Role=author',
        'https://dl.acm.org/profile/81100124997/publications?Role=author',
        'https://dl.acm.org/profile/81452610079/publications?Role=author',
        'https://dl.acm.org/profile/81330496505/publications?Role=author',
        'https://dl.acm.org/profile/81100156196/publications?Role=author',
        'https://dl.acm.org/profile/81100036481/publications?Role=author',
        'https://dl.acm.org/profile/81100648459/publications?Role=author',
        'https://dl.acm.org/profile/81557900356/publications?Role=author',
        'https://dl.acm.org/profile/81371594524/publications?Role=author',
        'https://dl.acm.org/profile/81100631947/publications?Role=author',
        'https://dl.acm.org/profile/81496648762/publications?Role=author',
        'https://dl.acm.org/profile/81100606986/publications?Role=author',
        'https://dl.acm.org/profile/81100301488/publications?Role=author',
        'https://dl.acm.org/profile/81100094018/publications?Role=author',
        'https://dl.acm.org/profile/81100215093/publications?Role=author',
        'https://dl.acm.org/profile/81100287057/publications?Role=author',
        'https://dl.acm.org/profile/81492650095/publications?Role=author',
        'https://dl.acm.org/profile/81100437589/publications?Role=author',
        'https://dl.acm.org/profile/81100165187/publications?Role=author',
        'https://dl.acm.org/profile/81321488138/publications?Role=author'
    ]

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
        abstract_text = None

        # Pattern 1: Abstract inside <div> with role="paragraph"
        if not abstract_text:
            abstract_text = response.css('div[role="paragraph"]::text').get()

        # Pattern 2: Abstract inside <div> with class "abstractSection"
        if not abstract_text:
            abstract_text = response.css('div.abstractSection p::text').get()

        # Pattern 3: Abstract inside <section> with role="doc-abstract"
        if not abstract_text:
            abstract_text = response.css('section[role="doc-abstract"] div[role="paragraph"]::text').get()

        # Pattern 4: Clean "before/after" content from <div class="abstractSection">
        if not abstract_text:
            abstract_text_raw = response.css('div.abstractSection p').get()
            if abstract_text_raw:
                abstract_text = scrapy.selector.Selector(text=abstract_text_raw).xpath('string()').get()

        # Log a warning if no abstract is found
        if not abstract_text:
            logging.warning(f"No abstract found for URL: {response.url}")

        # Normalize the abstract text
        if abstract_text:
            abstract_text = (
                abstract_text.replace("$underline{", "")
                            .replace("}", "")
                            .replace("''", "'")
                            .strip()
            )

        yield {
            'Title': response.meta['title'],
            'URL': response.meta['url'],
            'Full Abstract': abstract_text or "Abstract not found or failed to load."
        }
