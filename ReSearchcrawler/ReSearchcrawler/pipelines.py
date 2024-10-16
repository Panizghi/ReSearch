import json
import csv
import os
import logging
from scholarly import scholarly, ProxyGenerator

import csv
import os
import json
import logging
import csv
import os
import json
import logging
import sys

class ACMProfilePipeline:

    def open_spider(self, spider):
        """Open files and read checkpoint when the spider starts."""
        self.base_filepath = 'acm_profiles'
        self.file_index = 1
        self.filepath = f'{self.base_filepath}_{self.file_index}.csv'
        self.checkpoint_file = 'last_iteration.txt'
        self.file_size_limit = 100 * 1024 * 1024  # 100 MB limit for each CSV file

        # Increase CSV field size limit
        csv.field_size_limit(sys.maxsize)

        # Open or create the CSV file
        self._open_csv_file()

        # Fallback for checkpoint
        self.last_iteration = self._read_checkpoint()
        logging.info(f"Starting from checkpoint: {self.last_iteration}")

    def _open_csv_file(self):
        """Open a new CSV file, create headers if needed."""
        if self._is_file_valid(self.filepath):
            self.csv_file = open(self.filepath, 'a', newline='')  # Append mode
            self.existing_data = self._load_existing_data()
        else:
            # Fallback: Create a new file and start from scratch
            logging.warning(f"{self.filepath} is missing or corrupted. Starting a new file.")
            self.csv_file = open(self.filepath, 'w', newline='')  # Create a new file
            self.writer = csv.writer(self.csv_file)
            self.writer.writerow([
                'Full Name', 'Year', 'Type of Award', 'Profile URL', 'DL Link', 'Bibliometrics', 'Co-Authors', 
                'Keywords', 'Publications', 'Bar Chart Data', 'Image URL', 'Google Scholar URL', 'Affiliation', 'Interests'
            ])
            self.existing_data = set()

        # Initialize the CSV writer
        self.writer = csv.writer(self.csv_file)

    def _is_file_valid(self, filepath):
        """Check if the file exists and is not empty or corrupted."""
        return os.path.exists(filepath) and os.stat(filepath).st_size > 0

    def _load_existing_data(self):
        """Load existing data from CSV to avoid duplicates based on (Full Name, Year, Type of Award)."""
        existing_data = set()
        with open(self.filepath, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            for row in reader:
                # Assuming 'Full Name', 'Year', 'Type of Award' are in the first three columns
                existing_data.add((row[0], row[1], row[2]))  # (Full Name, Year, Type of Award) tuple
        return existing_data

    def _read_checkpoint(self):
        """Read the last checkpoint from file with a fallback to 0 if missing or corrupted."""
        if self._is_file_valid(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, 'r') as f:
                    return int(f.read().strip())
            except (ValueError, IOError):
                logging.warning(f"Invalid checkpoint file. Starting from the beginning.")
                return 0
        return 0

    def _save_checkpoint(self, idx):
        """Save the current index as a checkpoint."""
        with open(self.checkpoint_file, 'w') as f:
            f.write(str(idx))
        logging.info(f"Checkpoint saved: {idx}")

    def _check_file_size(self):
        """Check if the current CSV file exceeds the size limit."""
        current_size = os.path.getsize(self.filepath)
        if current_size >= self.file_size_limit:
            logging.info(f"File size limit reached: {current_size} bytes. Creating a new CSV file.")
            self.csv_file.close()  # Close the current file
            self.file_index += 1  # Increment the file index
            self.filepath = f'{self.base_filepath}_{self.file_index}.csv'
            self._open_csv_file()  # Open a new CSV file

    def process_item(self, item, spider):
        """Process each item and append to the CSV file."""
        # Check if the file size exceeds the limit before writing
        self._check_file_size()

        # Construct the unique key (tuple) for the item
        unique_key = (item['full_name'], item['year'], item['type_of_award'])

        # Check if this (full_name, year, type_of_award) tuple is already processed
        if unique_key in self.existing_data:
            logging.info(f"Skipping already processed item: {unique_key}")
            return item

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

        # Append new data to CSV
        self.writer.writerow([
            item['full_name'], item['year'], item['type_of_award'], item['profile_url'], item['dl_link'],
            json.dumps(item['bibliometrics']), json.dumps(item['co_authors']),
            json.dumps(item['keywords']), json.dumps(item['publications']),
            json.dumps(item['bar_chart_data']), item['image_url'],
            item.get('gsc_url', 'N/A'), item.get('affiliation', 'N/A'),
            item.get('interests', 'N/A')
        ])

        # Save checkpoint
        self._save_checkpoint(item['index'])

        # Add the unique key to the existing data set
        self.existing_data.add(unique_key)

        return item

    def close_spider(self, spider):
        """Close all resources when the spider closes."""
        logging.info("Closing spider")
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
