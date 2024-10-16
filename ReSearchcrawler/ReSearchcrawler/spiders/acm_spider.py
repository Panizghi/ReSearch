import scrapy
from ReSearchcrawler.items import ACMProfileItem

from bs4 import BeautifulSoup
import logging
import json

logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)

class ACMSpider(scrapy.Spider):
    name = "acm_spider"
    allowed_domains = ["awards.acm.org", "dl.acm.org"]
    start_urls = ['https://awards.acm.org/award-recipients']

    def parse(self, response):
        """Parse the ACM award recipients page and extract profile URLs."""
        table = response.xpath("//table[contains(@class, 'awards-tables--fullWidth')]")
        rows = table.xpath(".//tr")

        for idx, row in enumerate(rows[1:]):
            recipient_name = row.xpath(".//td[1]//a/text()").get()
            profile_url = row.xpath(".//td[1]//a/@href").get()
            dl_link_element = row.xpath(".//td[last()]//a/@href").get()

            if dl_link_element:
                dl_link = response.urljoin(dl_link_element)
                full_profile_url = response.urljoin(profile_url)

                # Log the recipient being processed
                self.logger.info(f"Processing recipient: {recipient_name}")

                # Send request to extract detailed profile from DL link
                yield scrapy.Request(
                    dl_link,
                    callback=self.parse_dl_profile,
                    meta={
                        'recipient_name': recipient_name,
                        'profile_url': full_profile_url,
                        'dl_link': dl_link,
                        'index': idx  # Track the index for checkpoint saving
                    }
                )

    def parse_dl_profile(self, response):
        """Parse the DL profile page for detailed data."""
        recipient_name = response.meta['recipient_name']
        profile_url = response.meta['profile_url']
        dl_link = response.meta['dl_link']

        # Parse the response with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            # Extract the detailed ACM profile
            profile_data = self.extract_acm_profile(soup)
            
            # Create and populate the item
            item = ACMProfileItem(
                full_name=recipient_name,
                profile_url=profile_url,
                dl_link=dl_link,
                bibliometrics=profile_data.get("Bibliometrics"),
                co_authors=profile_data.get("Co_Authors"),
                keywords=profile_data.get("Keywords"),
                publications=profile_data.get("Publications"),
                bar_chart_data=profile_data.get("Bar_Chart_Data"),
                image_url=profile_data.get("Image_URL")
            )

            # Yield the item to the pipeline
            self.logger.info(f"Scraped profile for {recipient_name}")
            yield item
        except Exception as e:
            self.logger.error(f"Error parsing profile for {recipient_name}: {e}")

    def extract_acm_profile(self, soup):
        """Extract detailed profile data from the DL page."""
        profile_data = {}

        # Extract bibliometrics
        profile_data['Bibliometrics'] = self.extract_bibliometrics(soup)

        # Extract co-authors
        profile_data['Co_Authors'] = self.extract_co_authors(soup)

        # Extract keywords
        profile_data['Keywords'] = self.extract_keywords(soup)

        # Extract publications
        profile_data['Publications'] = self.extract_publications(soup)

        # Extract image URL if present
        profile_data['Image_URL'] = soup.find('img', class_='profile-image')['src'] if soup.find('img', class_='profile-image') else None

        # Extract bar chart data
        profile_data['Bar_Chart_Data'] = self.extract_bar_chart_data(soup)

        return profile_data

    def extract_bibliometrics(self, soup):
        """Extract bibliometrics from the profile."""
        bibliometrics_section = soup.find('div', class_='bibliometrics equal-height-slides')
        if not bibliometrics_section:
            return {}

        metrics = bibliometrics_section.find_all('div', class_='slide-item')
        bibliometrics = {}
        for metric in metrics:
            title = metric.find('div', class_='bibliometrics__title').text.strip()
            value = metric.find('div', class_='bibliometrics__count').text.strip()
            bibliometrics[title] = value
        return bibliometrics

    def extract_co_authors(self, soup):
        """Extract co-authors from the profile."""
        co_authors = []
        contrib_section = soup.find('div', {'data-widget-def': 'UX3ACMContributorsMetrics'})
        if contrib_section:
            author_items = contrib_section.find_all('div', class_='box-item__item')
            for item in author_items:
                co_author_data = {}
                author_tag = item.find('a')
                if author_tag:
                    co_author_data['Author'] = author_tag.text.strip()
                    co_author_data['Paper_Count'] = item.find('div', class_='box-item__count').text.strip()
                    co_authors.append(co_author_data)
        return co_authors

    def extract_keywords(self, soup):
        """Extract keywords from the profile."""
        keywords_section = soup.find_all('div', class_='keyword-item')
        keywords = []
        for keyword in keywords_section:
            term = keyword.find('span', class_='keyword-term').text.strip()
            count = keyword.find('span', class_='keyword-count').text.strip()
            keywords.append({'term': term, 'count': count})
        return keywords

    def extract_publications(self, soup):
        """Extract publications from the DL profile."""
        publications = []
        pub_list_section = soup.find_all('li', class_='search__item issue-item-container')
        for pub in pub_list_section:
            pub_data = {}

            title_tag = pub.find('h5', class_='issue-item__title').find('a')
            pub_data['Title'] = title_tag.text.strip() if title_tag else "No title"
            pub_data['Title_URL'] = title_tag['href'].strip() if title_tag else "No URL"

            authors = []
            author_list_section = pub.find('ul', class_='loa')
            if author_list_section:
                for author_item in author_list_section.find_all('li'):
                    author_link_tag = author_item.find('a')
                    if author_link_tag and author_link_tag.text.strip():
                        authors.append({
                            'Name': author_link_tag.text.strip(),
                            'Profile_URL': f"https://dl.acm.org{author_link_tag['href']}"
                        })
            pub_data['Authors'] = authors if authors else "No authors listed"

            # Other publication metadata
            pub_data['Journal_Info'] = pub.find('span', class_='epub-section__title').text if pub.find('span', class_='epub-section__title') else "No journal info"
            pub_data['DOI'] = pub.find('span', class_='doi').text if pub.find('span', class_='doi') else "No DOI"
            pub_data['Citations'] = pub.find('span', class_='citation-count').text if pub.find('span', class_='citation-count') else "0"
            pub_data['Downloads'] = pub.find('span', class_='downloads-count').text if pub.find('span', class_='downloads-count') else "0"

            publications.append(pub_data)
        return publications

    def extract_bar_chart_data(self, soup):
        """Extract bar chart data showing publication counts per year."""
        bar_chart_section = soup.find_all('div', class_='bar-chart-item')
        bar_chart_data = []
        for chart_item in bar_chart_section:
            year = chart_item.find('span', class_='bar-chart-item__label').text.strip()
            count = chart_item.find('span', class_='bar-chart-item__count').text.strip()
            bar_chart_data.append({'year': year, 'count': count})
        return bar_chart_data
