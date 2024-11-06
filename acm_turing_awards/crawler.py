import requests
from bs4 import BeautifulSoup
import csv
import os
import time
from gsc_crawler import get_google_scholar_url

# Function to crawl profile data from the award profile URL
def profile_crawler(name, profile_url):
    response = requests.get(profile_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    last_name, first_name = name.split(", ")
    full_name = soup.find('h1').text.strip()  # Ensure no trailing spaces

    awards_info = soup.find_all('section', {'class': 'awards-winners__citation'})
    acm_award = next((award for award in awards_info if award.find('h2').a.text == 'ACM A. M. Turing Award'), None)

    if acm_award:
        location, year = acm_award.find('h3', {'class': 'awards-winners__location'}).text.split(' - ')
        citation = ' '.join(acm_award.find('p', {'class': "awards-winners__citation-short"}).text.split('\n')).strip()
    else:
        location, year, citation = '', '', ''

    # extract Google Scholar data
    gsc_data = get_google_scholar_url(full_name)
    if not gsc_data and len(full_name.split()) >= 3:
        first_last_name = f'{full_name.split()[0]} {full_name.split()[-1]}'
        gsc_data = get_google_scholar_url(first_last_name)
    
    if gsc_data:
        gsc_url = f'https://scholar.google.com/citations?user={gsc_data["scholar_id"]}'
        affiliation = gsc_data.get("affiliation", "")
        interests = " ".join(gsc_data.get('interests', []))
    else:
        gsc_url, affiliation, interests = '', '', '[]'

    return [last_name, first_name, year, location, citation, profile_url, gsc_url, affiliation, interests]


# Scraping ACM Turing Award page
url = 'https://awards.acm.org/turing/award-recipients'
session = requests.Session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = session.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Locate the table and check if it exists
table = soup.find('table', class_='awards-tables')
if not table:
    print("Table not found!")
    exit(1)

# Extract table headers
headers = [th.text.strip() for th in table.find('thead').find_all('th')]

# Extract table rows
rows = []
for tr in table.find('tbody').find_all('tr'):
    row_data = [td.text.strip() for td in tr.find_all('td')]
    rows.append(row_data)

# Print the extracted data for verification
print("Headers:", headers)
for row in rows:
    print("Row:", row)

# Sorting the rows by year (column index 2)
rows.sort(key=lambda row: int(row[2]), reverse=True)

# Handling file and checkpoint for resuming
it = 0
checkpoint = 'last_iteration.txt'
fileName = 'acm_turings2.csv'
fileExist = os.path.isfile(fileName) and os.path.isfile(checkpoint)

with open(fileName, 'a' if fileExist else 'w', newline='') as file:
    writer = csv.writer(file)
    # Write the header row if the file is new
    if not fileExist:
        writer.writerow(['Index', 'Last Name', 'Given Name', 'Year', 'Location', 'Citation', 'ACM Fellow Profile', 'Google Scholar Profile', 'Affiliation', 'Interests'])
    else:
        with open(checkpoint, 'r') as f:
            index = int(f.readline().split(':')[-1])
            rows = rows[index:]
            it = index
    
    for row in rows:
        try:
            award_recipient = row[0]  # Assuming name is in the first column
            profile_url = f'https://awards.acm.org/{row[-1]}'  # Adjust if profile URL is in a different column

            # Clean the name to remove non-ASCII characters
            name = ''.join([i if ord(i) < 128 else ' ' for i in award_recipient])

            data = profile_crawler(name, profile_url)
            it += 1

            data.insert(0, it)  # Add index at the start
            writer.writerow(data)

            if it % 20 == 0:
                print(f"Finished {it} iterations...")
            time.sleep(1)

        except KeyboardInterrupt:
            print("Process interrupted manually.")
            with open(checkpoint, 'w') as f:
                f.write(f'Last completed iteration: {it}')
            break

        except Exception as e:
            print(f"Exception occurred: {e}")
            with open(checkpoint, 'w') as f:
                f.write(f'Failed at iteration: {it}')
            break
