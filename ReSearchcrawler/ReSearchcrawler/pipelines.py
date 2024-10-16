import json
import csv
import os
import logging
from scholarly import scholarly, ProxyGenerator

class ACMProfilePipeline:

    def open_spider(self, spider):
        """Open files and read checkpoint when the spider starts."""
        self.file = open('acm_profiles.json', 'a')  # Append mode to avoid overwriting
        self.csv_file = open('acm_profiles.csv', 'a', newline='')

        # Initialize the CSV writer
        self.writer = csv.writer(self.csv_file)

        # If CSV is empty, write the header
        if os.stat('acm_profiles.csv').st_size == 0:
            self.writer.writerow(['Full Name', 'Profile URL', 'DL Link', 'Bibliometrics', 'Co-Authors', 'Keywords', 'Publications', 'Bar Chart Data', 'Image URL', 'Google Scholar URL', 'Affiliation', 'Interests'])
        
        # Checkpoint to track the last processed researcher
        self.checkpoint_file = 'last_iteration.txt'
        self.last_iteration = self._read_checkpoint()
        logging.info(f"Starting from checkpoint: {self.last_iteration}")

    def _read_checkpoint(self):
        """Read the last checkpoint index from file."""
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'r') as f:
                return int(f.read().strip())
        return 0

    def _save_checkpoint(self, idx):
        """Save the current index as a checkpoint."""
        with open(self.checkpoint_file, 'w') as f:
            f.write(str(idx))
        logging.info(f"Checkpoint saved: {idx}")

    def process_item(self, item, spider):
        """Process each item scraped by the spider."""
        if 'index' not in item:
            logging.error("Index missing in item, cannot save checkpoint.")
            return item

        # Fetch Google Scholar data for the researcher
        scholar_data = self._fetch_google_scholar_data(item['full_name'])
        if scholar_data:
            item['gsc_url'] = scholar_data['gsc_url']
            item['affiliation'] = scholar_data['affiliation']
            item['interests'] = scholar_data['interests']
        else:
            # Fallback if Google Scholar data is not found
            item['gsc_url'] = 'N/A'
            item['affiliation'] = 'N/A'
            item['interests'] = 'N/A'

        # Save to JSON file
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
        self._save_checkpoint(item['index'])

        return item

    def close_spider(self, spider):
        """Close all resources when the spider closes."""
        self.file.close()
        self.csv_file.close()

    def _fetch_google_scholar_data(self, name):
        """Fetch Google Scholar data using the `scholarly` package."""
        pg = ProxyGenerator()
        pg.ScraperAPI('2c0689f76068fc9463b07cac6970050e')  # Replace with your ScraperAPI key
        scholarly.use_proxy(pg)

        try:
            author = scholarly.search_author(name)
            author_data = next(author)
            return {
                'gsc_url': f"https://scholar.google.com/citations?user={author_data['scholar_id']}",
                'affiliation': author_data.get("affiliation", ""),
                'interests': ", ".join(author_data.get('interests', []))
            }
        except StopIteration:
            logging.error(f"No Google Scholar data found for {name}")
            return None
        except Exception as e:
            logging.error(f"Error fetching Google Scholar data for {name}: {e}")
            return None
