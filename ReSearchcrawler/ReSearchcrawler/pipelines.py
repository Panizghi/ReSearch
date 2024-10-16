# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from ReSearchcrawler.items import ACMProfileItem

import json

import csv
import os
import json
import logging
from scholarly import scholarly, ProxyGenerator

class ACMProfilePipeline:

    def open_spider(self, spider):
        """Open the file and the checkpoint when the spider is opened."""
        self.file = open('acm_profiles.json', 'a')  # Change to 'w' if you want to overwrite
        self.csv_file = open('acm_profiles.csv', 'a', newline='')

        # If CSV is empty, write the header
        if os.stat('acm_profiles.csv').st_size == 0:
            self.writer = csv.writer(self.csv_file)
            self.writer.writerow(['Full Name', 'Profile URL', 'DL Link', 'Bibliometrics', 'Co-Authors', 'Keywords', 'Publications', 'Bar Chart Data', 'Image URL', 'Google Scholar URL', 'Affiliation', 'Interests'])
        
        # Checkpoint to keep track of the last processed researcher
        self.checkpoint_file = 'last_iteration.txt'
        self.last_iteration = self._read_checkpoint()

    def _read_checkpoint(self):
        """Read the last checkpoint from file."""
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'r') as f:
                return int(f.read().strip())
        return 0

    def _save_checkpoint(self, idx):
        """Save the current index as a checkpoint."""
        with open(self.checkpoint_file, 'w') as f:
            f.write(str(idx))

    def process_item(self, item, spider):
        """Process each item scraped by the spider."""
        # Save to JSON file progressively
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)

        # Save to CSV file
        self.writer.writerow([item['full_name'], item['profile_url'], item['dl_link'],
                              json.dumps(item['bibliometrics']), json.dumps(item['co_authors']),
                              json.dumps(item['keywords']), json.dumps(item['publications']),
                              json.dumps(item['bar_chart_data']), item['image_url'],
                              item.get('gsc_url', 'N/A'), item.get('affiliation', 'N/A'),
                              item.get('interests', 'N/A')])

        # Save checkpoint
        self._save_checkpoint(item['index'])  # Use the 'index' you get from the spider for each researcher

        return item

    def close_spider(self, spider):
        """Close the file and resources when the spider is closed."""
        self.file.close()
        self.csv_file.close()

    # Integrating Google Scholar scraping using `scholarly`
    def _fetch_google_scholar_data(self, name):
        """Fetch Google Scholar data for the researcher."""
        pg = ProxyGenerator()
        pg.ScraperAPI('YOUR_SCRAPERAPI_KEY')  # Replace with your API key
        scholarly.use_proxy(pg)

        author = scholarly.search_author(name)
        try:
            author_data = next(author)
            return {
                'gsc_url': f"https://scholar.google.com/citations?user={author_data['scholar_id']}",
                'affiliation': author_data.get("affiliation", ""),
                'interests': ", ".join(author_data.get('interests', []))
            }
        except StopIteration:
            return None
