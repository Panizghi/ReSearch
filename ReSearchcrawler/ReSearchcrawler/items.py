import scrapy

class ACMProfileItem(scrapy.Item):
    # Basic Info
    full_name = scrapy.Field()
    profile_url = scrapy.Field()  # ACM profile URL
    dl_link = scrapy.Field()  # Digital Library profile URL

    # Detailed ACM Profile Data
    bibliometrics = scrapy.Field()  # Citation, publication, and download metrics
    image_url = scrapy.Field()  # Profile image URL
    co_authors = scrapy.Field()  # List of co-authors and their paper counts
    keywords = scrapy.Field()  # List of research keywords with counts
    publications = scrapy.Field()  # List of publications with title, authors, etc.
    bar_chart_data = scrapy.Field()  # Annual publication counts

    # Publication Metadata for each publication
    publication_title = scrapy.Field()  # Title of the publication
    publication_title_url = scrapy.Field()  # URL for the publication
    publication_authors = scrapy.Field()  # List of authors for each publication
    journal_info = scrapy.Field()  # Information about the journal (if available)
    doi = scrapy.Field()  # DOI of the publication (if available)
    citations = scrapy.Field()  # Number of citations for the publication
    downloads = scrapy.Field()  # Number of downloads for the publication

    # New fields for Google Scholar data
    gsc_url = scrapy.Field()
    affiliation = scrapy.Field()
    interests = scrapy.Field()

    # Additional fields required by the pipeline
    year = scrapy.Field()
    type_of_award = scrapy.Field()
    index = scrapy.Field()
