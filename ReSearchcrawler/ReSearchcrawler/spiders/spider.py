# import scrapy
# from ReSearchcrawler.items import ACMProfileItem
# from bs4 import BeautifulSoup
# import logging
# import scrapy
# from ReSearchcrawler.items import ACMProfileItem
# from bs4 import BeautifulSoup
# import logging
# import json
# import os
# import requests
# import csv


# def get_random_user_agent():
#     """Returns a random user-agent string."""
#     return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# def retry_request(url, headers):
#     """Helper to send a request and handle retries."""
#     import requests
#     from requests.adapters import HTTPAdapter
#     from requests.packages.urllib3.util.retry import Retry

#     session = requests.Session()
#     retry = Retry(
#         total=3,
#         backoff_factor=1,
#         status_forcelist=[429, 500, 502, 503, 504]
#     )
#     adapter = HTTPAdapter(max_retries=retry)
#     session.mount('http://', adapter)
#     session.mount('https://', adapter)

#     try:
#         response = session.get(url, headers=headers, timeout=10)
#         response.raise_for_status()
#         return response
#     except requests.RequestException as e:
#         logging.error(f"Request failed for {url}: {e}", exc_info=True)
#         return None

# class ACMSpider(scrapy.Spider):
#     name = "acm_spider"
#     allowed_domains = ["awards.acm.org", "dl.acm.org"]
#     start_urls = ['https://awards.acm.org/award-recipients']

#     def parse(self, response):
#         """Parse the ACM award recipients page and extract profile URLs."""
#         table = response.xpath("//table[contains(@class, 'awards-tables--fullWidth')]")
#         rows = table.xpath(".//tr")
        
#         for idx, row in enumerate(rows[1:]):  # Skip the header row
#             recipient_name = row.xpath(".//td[1]//a/text()").get()
#             profile_url = row.xpath(".//td[1]//a/@href").get()
#             dl_link_element = row.xpath(".//td[last()]//a/@href").get()

#             # Extract additional data like year and type_of_award if available
#             year = row.xpath(".//td[2]/text()").get()  # Example XPath; adjust as needed
#             type_of_award = row.xpath(".//td[3]/text()").get()  # Example XPath; adjust as needed

#             if dl_link_element:
#                 dl_link = response.urljoin(dl_link_element)
#                 full_profile_url = response.urljoin(profile_url)

#                 # Log the recipient being processed
#                 self.logger.info(f"Processing recipient: {recipient_name}")

#                 # Send request to extract detailed profile from DL link
#                 yield scrapy.Request(
#                     dl_link,
#                     callback=self.parse_dl_profile,
#                     meta={
#                         'recipient_name': recipient_name,
#                         'profile_url': full_profile_url,
#                         'dl_link': dl_link,
#                         'index': idx,  # Track the index for checkpoint saving
#                         'year': year,
#                         'type_of_award': type_of_award
#                     },
#                     errback=self.errback_handler
#                 )

#     def parse_dl_profile(self, response):
#         """Parse the DL profile page for detailed data."""
#         recipient_name = response.meta['recipient_name']
#         profile_url = response.meta['profile_url']
#         dl_link = response.meta['dl_link']
#         index = response.meta['index']
#         year = response.meta['year']
#         type_of_award = response.meta['type_of_award']

#         # Parse the response with BeautifulSoup
#         soup = BeautifulSoup(response.text, 'html.parser')

#         try:
#             # Extract the detailed ACM profile
#             profile_data = self.extract_acm_profile(soup, dl_link)

#             # Create and populate the item
#             item = ACMProfileItem(
#                 full_name=recipient_name,
#                 profile_url=profile_url,
#                 dl_link=dl_link,
#                 bibliometrics=profile_data.get("Bibliometrics"),
#                 co_authors=profile_data.get("Co_Authors"),
#                 keywords=profile_data.get("Keywords"),
#                 publications=profile_data.get("Publications"),
#                 bar_chart_data=profile_data.get("Bar_Chart_Data"),
#                 image_url=profile_data.get("Image_URL"),
#                 year=year,
#                 type_of_award=type_of_award,
#                 index=index
#             )

#             # Yield the item to the pipeline
#             self.logger.info(f"Scraped profile for {recipient_name}")
#             yield item
#         except Exception as e:
#             self.logger.error(f"Error parsing profile for {recipient_name}: {e}", exc_info=True)

#     def extract_acm_profile(self, soup, dl_link):
#         """Extract detailed profile data from the DL page."""
#         profile_data = {}

#         # Extract bibliometrics
#         profile_data['Bibliometrics'] = self.extract_bibliometrics(soup)

#         # Extract co-authors
#         profile_data['Co_Authors'] = self.extract_co_authors(soup)

#         # Extract keywords
#         profile_data['Keywords'] = self.extract_keywords(soup)

#         # Extract publications
#         profile_data['Publications'] = self.extract_publications(dl_link)

#         # Extract image URL if present
#         profile_data['Image_URL'] = soup.find('img', class_='profile-image')['src'] if soup.find('img', class_='profile-image') else None

#         # Extract bar chart data
#         profile_data['Bar_Chart_Data'] = self.extract_bar_chart_data(soup)

#         return profile_data

#     def extract_bibliometrics(self, soup):
#         """Extract bibliometrics from the profile."""
#         bibliometrics_section = soup.find('div', class_='bibliometrics equal-height-slides')
#         if not bibliometrics_section:
#             return {}

#         metrics = bibliometrics_section.find_all('div', class_='slide-item')
#         bibliometrics = {}
#         for metric in metrics:
#             title = metric.find('div', class_='bibliometrics__title').text.strip()
#             value = metric.find('div', class_='bibliometrics__count').text.strip()
#             bibliometrics[title] = value
#         return bibliometrics

#     def extract_co_authors(self, soup):
#         """Extract co-authors from the profile."""
#         co_authors = []
#         contrib_section = soup.find('div', {'data-widget-def': 'UX3ACMContributorsMetrics'})
#         if contrib_section:
#             author_items = contrib_section.find_all('div', class_='box-item__item')
#             for item in author_items:
#                 co_author_data = {}
#                 author_tag = item.find('a')
#                 if author_tag:
#                     co_author_data['Author'] = author_tag.text.strip()
#                     co_author_data['Paper_Count'] = item.find('div', class_='box-item__count').text.strip()
#                     co_authors.append(co_author_data)
#         return co_authors

#     def extract_keywords(self, soup):
#         """Extract keywords from the profile."""
#         keywords = []
#         tag_cloud_div = soup.find('div', class_='tag-cloud')
#         if tag_cloud_div and tag_cloud_div.has_attr('data-tags'):
#             data_tags = tag_cloud_div['data-tags'].replace('&quot;', '"')
#             try:
#                 tags_data = json.loads(data_tags)
#                 for tag in tags_data:
#                     keyword_info = {
#                         'term': tag.get('term'),
#                         'label': tag.get('label'),
#                         'count': tag.get('count'),
#                         'link': tag.get('link')
#                     }
#                     keywords.append(keyword_info)
#             except json.JSONDecodeError as e:
#                 logging.error(f"Failed to parse JSON: {e}", exc_info=True)
#         return keywords

#     def extract_publications(self, dl_link):
#         """Extract publications for the author using the DL link."""
#         publications_url = f"{dl_link}?Role=author"
#         headers = {'User-Agent': get_random_user_agent()}
        
#         try:
#             page_number = 1
#             publications = []
#             while True:
#                 paginated_url = f"{publications_url}&startPage={page_number}"
#                 response = retry_request(paginated_url, headers)
                
#                 if not response or response.status_code != 200:
#                     self.logger.error(f"Failed to retrieve page {page_number} for {paginated_url}")
#                     break

#                 soup = BeautifulSoup(response.content, 'html.parser')

#                 # Extract publication data
#                 pub_list_section = soup.find_all('li', class_='search__item issue-item-container')
#                 if not pub_list_section:
#                     self.logger.info(f"No publication list found on page {page_number}")
#                     break  # Exit if there are no more publications

#                 for pub in pub_list_section:
#                     pub_data = {}

#                     # Extract title and link
#                     title_tag = pub.find('h5', class_='issue-item__title').find('a')
#                     if title_tag:
#                         pub_data['Title'] = title_tag.text.strip()
#                         pub_data['Title_URL'] = title_tag['href'].strip()

#                     # Extract contributors/authors
#                     author_list_section = pub.find('ul', class_='loa')
#                     authors = []
#                     if author_list_section:
#                         for author_item in author_list_section.find_all('li'):
#                             author_link_tag = author_item.find('a')
#                             if author_link_tag and author_link_tag.text.strip():
#                                 author_name = author_link_tag.text.strip()
#                                 author_profile_url = author_link_tag['href'].strip()
#                                 authors.append({
#                                     'Name': author_name,
#                                     'Profile_URL': f"https://dl.acm.org{author_profile_url}"  # Ensure full URL
#                                 })

#                     # Check if there is a button for more authors (collapsed)
#                     collapsed_authors_button = pub.find('button', class_='removed-items-count')
#                     if collapsed_authors_button:
#                         self.logger.warning(f"Additional authors may be hidden behind a collapsed view for publication: {pub_data.get('Title')}")

#                     # If no authors are found, fallback to 'No authors listed'
#                     pub_data['Authors'] = authors if authors else "No authors listed"

#                     # Extract journal, article number, and pages
#                     details_tag = pub.find('div', class_='issue-item__detail')
#                     if details_tag:
#                         journal_info = details_tag.find('span', class_='epub-section__title')
#                         article_info = details_tag.find_all('span', class_='dot-separator') if details_tag else []
#                         pub_data['Journal_Info'] = journal_info.text.strip() if journal_info else "No journal info available"
#                         if len(article_info) > 0:
#                             pub_data['Article_No'] = article_info[0].text.strip()
#                         if len(article_info) > 1:
#                             pub_data['Pages'] = article_info[1].text.strip()

#                     # Extract DOI link
#                     doi_tag = details_tag.find('a', class_='issue-item__doi') if details_tag else None
#                     if doi_tag:
#                         doi_link = doi_tag['href'].strip()
#                         if not doi_link.startswith('https://'):
#                             doi_link = f"https://{doi_link}"
#                         pub_data['DOI'] = doi_link
#                     else:
#                         pub_data['DOI'] = "No DOI available"

#                     # Extract abstract
#                     abstract_tag = pub.find('div', class_='issue-item__abstract')
#                     if abstract_tag:
#                         pub_data['Abstract'] = abstract_tag.find('p').text.strip()

#                     # Extract citation and download metrics
#                     metrics_tag = pub.find('div', class_='issue-item__footer')
#                     if metrics_tag:
#                         citations = metrics_tag.find('span', class_='citation')
#                         downloads = metrics_tag.find('span', class_='metric')
#                         pub_data['Citations'] = citations.find('span').text.strip() if citations else "0"
#                         pub_data['Downloads'] = downloads.find('span').text.strip() if downloads else "0"

#                     publications.append(pub_data)

#                 page_number += 1  # Move to the next page

#             return publications

#         except Exception as e:
#             self.logger.error(f"Error fetching publications for {dl_link}: {e}", exc_info=True)
#             return []

#     def extract_bar_chart_data(self, soup):
#         """Extract bar chart data showing publication counts per year."""
#         bar_count = soup.find_all('svg', class_='d3-bar-chart')
#         data_chart_data = []
#         for bar_chart in bar_count:
#             if bar_chart.has_attr("data-chart-data"):
#                 chart_data = bar_chart['data-chart-data'].replace('&quot;', '"')
#                 try:
#                     chart_data = json.loads(chart_data)
#                     data_chart_data.extend(chart_data)
#                 except json.JSONDecodeError as e:
#                     self.logger.error(f"Failed to parse bar chart data: {e}", exc_info=True)
#         return data_chart_data

#     def errback_handler(self, failure):
#         """Handle request failures."""
#         self.logger.error(repr(failure))
