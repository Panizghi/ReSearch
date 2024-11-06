import requests
from bs4 import BeautifulSoup
import re
import csv
# Function to scrape a single researcher's additional details
def scrape_dl_profile(dl_url):
    profile_info = {}
    try:
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' }
        dl_response = requests.get(dl_url, headers=headers)
        if dl_response.status_code == 200:
            dl_soup = BeautifulSoup(dl_response.content, 'html.parser')
            
            # Find all elements with classes containing double underscores
            double_underscore_elements = dl_soup.find_all(class_=re.compile(r'\w+__\w+'))
            
            # Collecting text from these elements
            double_underscore_text = [element.get_text(strip=True) for element in double_underscore_elements]
            
            # Example fields to store:
            profile_info['double_underscore_content'] = " | ".join(double_underscore_text) if double_underscore_text else 'N/A'
            
        else:
            print(f"Failed to fetch DL profile: {dl_url}")
    except Exception as e:
        print(f"Error scraping DL profile {dl_url}: {e}")
    
    return profile_info

# Function to scrape the ACM award recipients page
def scrape_acm_award_recipients():
    url = "https://awards.acm.org/award-recipients"
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' }
    response = requests.get(url,headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve the page.")
        return
    
    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Try to find the table using a more generic approach
    table = soup.find('table')  # Try to locate the first table
    
    if table is None:
        print("No table found on the page. Check the structure or class name.")
        return
    
    # Now try to find all rows in the table
    rows = table.find_all('tr')[1:]  # Skip the header row
    
    if not rows:
        print("No rows found in the table. Verify the page content.")
        return
    
    # List to store scraped data
    recipients_data = []
    
    for row in rows:
        cols = row.find_all('td')
        name = cols[0].text.strip()
        award = cols[1].text.strip()
        year = cols[2].text.strip()
        region = cols[3].text.strip()
        dl_link = cols[4].find('a')['href'] if cols[4].find('a') else 'N/A'
        
        # Scrape additional details from the DL profile
        dl_url = f"https://dl.acm.org{dl_link}"
        profile_details = scrape_dl_profile(dl_url)
        
        # Append all the data together
        recipient = {
            'name': name,
            'award': award,
            'year': year,
            'region': region,
            'dl_profile': dl_url,
            **profile_details  # Include any additional info from the profile page
        }
        recipients_data.append(recipient)
    
    # Write data to CSV
    with open('acm_award_recipients.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'award', 'year', 'region', 'dl_profile', 'double_underscore_content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for data in recipients_data:
            writer.writerow(data)
    
    print("Data saved to acm_award_recipients.csv")

if __name__ == "__main__":
    scrape_acm_award_recipients()
