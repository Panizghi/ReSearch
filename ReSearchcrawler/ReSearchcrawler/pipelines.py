import json
import os
import logging
from scholarly import scholarly, ProxyGenerator
import sys

class ACMProfilePipeline:

    def open_spider(self, spider):
        """Open files and read checkpoint when the spider starts."""
        self.base_filepath = 'acm_profiles'
        self.jsonl_filepath = f'{self.base_filepath}.jsonl'
        self.checkpoint_file = 'last_iteration.txt'

        # Set a limit for file size (optional)
        self.file_size_limit = 100 * 1024 * 1024  # 100 MB for each JSONL file

        

        # Open the JSONL file in append mode
        self._open_jsonl_file()

        # Read checkpoint to continue from the last processed item
        self.last_iteration = self._read_checkpoint()
        logging.info(f"Starting from checkpoint: {self.last_iteration}")

    def _open_jsonl_file(self):
        """Open a new JSONL file in append mode."""
        if not os.path.exists(self.jsonl_filepath):
            logging.info(f"Creating new JSONL file: {self.jsonl_filepath}")
            with open(self.jsonl_filepath, 'w'):  # Create empty file if it doesn't exist
                pass
        self.jsonl_file = open(self.jsonl_filepath, 'a', encoding='utf-8')

    def _read_checkpoint(self):
        """Read the last checkpoint index from file."""
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, 'r') as f:
                    return int(f.read().strip())
            except (ValueError, IOError):
                logging.warning("Invalid checkpoint file. Starting from the beginning.")
                return 0
        return 0

    def _save_checkpoint(self, idx):
        """Save the current index as a checkpoint."""
        with open(self.checkpoint_file, 'w') as f:
            f.write(str(idx))
        logging.info(f"Checkpoint saved: {idx}")

    def process_item(self, item, spider):
        """Process each item and append to the JSONL file."""
        unique_key = (item['full_name'], item['year'], item['type_of_award'])

        # Check if this (full_name, year, type_of_award) tuple is already processed
        logging.info(f"Processing: {unique_key}")

        # Fetch Google Scholar data for the researcher (if applicable)
        scholar_data = self._fetch_google_scholar_data(item['full_name'])
        if scholar_data:
            item['gsc_url'] = scholar_data['gsc_url']
            item['affiliation'] = scholar_data['affiliation']
            item['interests'] = scholar_data['interests']
        else:
            item['gsc_url'] = 'N/A'
            item['affiliation'] = 'N/A'
            item['interests'] = 'N/A'

        # Write profile data as JSONL entry
        profile_data = {
            'full_name': item['full_name'],
            'year': item['year'],
            'type_of_award': item['type_of_award'],
            'profile_url': item['profile_url'],
            'dl_link': item['dl_link'],
            'bibliometrics': item['bibliometrics'],
            'co_authors': item['co_authors'],
            'keywords': item['keywords'],
            'publications': item['publications'],
            'bar_chart_data': item['bar_chart_data'],
            'image_url': item['image_url'],
            'gsc_url': item.get('gsc_url', 'N/A'),
            'affiliation': item.get('affiliation', 'N/A'),
            'interests': item.get('interests', 'N/A')
        }

        # Append the profile data to the JSONL file and flush
        self._write_jsonl(profile_data)

        # Save checkpoint
        self._save_checkpoint(item['index'])

        return item

    def _write_jsonl(self, data):
        """Write a single line of JSON to the JSONL file and flush the buffer."""
        json.dump(data, self.jsonl_file, ensure_ascii=False)
        self.jsonl_file.write('\n')
        self.jsonl_file.flush()  # Flush the buffer to ensure data is saved immediately

    def close_spider(self, spider):
        """Close all resources when the spider closes."""
        logging.info("Closing spider")
        self.jsonl_file.close()

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
