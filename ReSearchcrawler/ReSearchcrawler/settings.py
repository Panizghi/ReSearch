# Scrapy settings for ReSearchcrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "ReSearchcrawler"

SPIDER_MODULES = ["ReSearchcrawler.spiders"]
NEWSPIDER_MODULE = "ReSearchcrawler.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "ReSearchcrawler (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Enable AutoThrottle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0


# Limit concurrent requests
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8

# Disable cookies
COOKIES_ENABLED = False

# Enable rotating user agents
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

# Enable HTTP caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Configure a delay for requests to avoid being blocked
DOWNLOAD_DELAY = 10

# Enable item pipelines
ITEM_PIPELINES = {
    "ReSearchcrawler.pipelines.ACMProfilePipeline": 300,
}

# settings.py

ITEM_PIPELINES = {
    'ReSearchcrawler.pipelines.ACMProfilePipeline': 300,  # Adjust the path as necessary
}

# Optional: Configure logging level to DEBUG for more verbose output
LOG_LEVEL = 'INFO'


# settings.py

# Enable retry middleware
RETRY_ENABLED = True
RETRY_TIMES = 3  # Number of retries
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408]

# Configure download delays to prevent getting blocked
DOWNLOAD_DELAY = 2  # 2 seconds delay between requests

# Enable AutoThrottle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
