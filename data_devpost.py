import time
import re
import csv  # Import the CSV module
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def save_to_csv(hackathon_data, filename):
    """Saves the scraped hackathon data to a CSV file."""
    if not hackathon_data:
        print("No data to save to CSV.")
        return

    # Define the headers for the CSV file
    headers = ['title', 'link', 'location', 'participants', 'days_left', 'host']
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(hackathon_data)
        print(f"\n✅ Data successfully saved to '{filename}'")
    except IOError as e:
        print(f"❌ Error saving to CSV file: {e}")

def upsert_to_mysql(hackathon_data):
    """
    Connects to the devpost_data database and performs an "upsert" operation.
    - INSERTS a new hackathon if it doesn't exist.
    - UPDATES an existing hackathon if a duplicate is found (based on title and host).
    """
    if not hackathon_data:
        print("No data to insert into the database.")
        return

    try:
        with mysql.connector.connect(
            host='localhost',
            user='YOUR_USERNAME',
            password='YOUR_USER_PASSWORD',  # Replace with your password
            database='devpost_data'
        ) as conn:
            with conn.cursor() as cursor:
                upsert_query = """
                    INSERT INTO hackathons (title, link, location, participants, days_left, host)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        link = VALUES(link),
                        location = VALUES(location),
                        participants = VALUES(participants),
                        days_left = VALUES(days_left);
                """
                
                records_to_upsert = [
                    (
                        hackathon['title'], hackathon['link'], hackathon['location'],
                        hackathon['participants'], hackathon['days_left'], hackathon['host']
                    ) for hackathon in hackathon_data
                ]

                cursor.executemany(upsert_query, records_to_upsert)
                conn.commit()

                print(f"✅ Database synchronized. {cursor.rowcount} records were inserted or updated.")

    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")

def main():
    """Main function to scrape Devpost, save to CSV, and update the database."""
    # --- Setup Chrome options ---
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(options=options)
    all_hackathons = []

    try:
        url = 'https://devpost.com/hackathons?status[]=open'
        print(f"Navigating to {url}...")
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'hackathons-container'))
        )

        # --- Scroll to load all content ---
        print("Scrolling to load all hackathons...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        print("Finished scrolling. Parsing final page content...")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tiles = soup.find_all('div', class_='hackathon-tile')
        print(f"Found {len(tiles)} total hackathon listings.")

        # --- Parse final results ---
        for i, tile in enumerate(tiles, 1):
            title_elem = tile.find(['h2', 'h3'])
            title = title_elem.get_text(strip=True) if title_elem else 'N/A'

            link_elem = tile.find('a', href=True)
            link = 'N/A'
            if link_elem:
                href = link_elem['href']
                link = href if href.startswith('http') else f"https://devpost.com{href}"

            text_block = tile.get_text(separator=' ', strip=True)

            days_match = re.search(r'(\d+\s+days?\s+left|Submission period ends\s+in\s+\d+\s+hours)', text_block, re.IGNORECASE)
            days_left = days_match.group(1) if days_match else 'N/A'
            
            participants_match = re.search(r'(\d[\d,]*)\s+participants', text_block, re.IGNORECASE)
            participants = participants_match.group(1).replace(',', '') if participants_match else 'N/A'
            
            location = 'N/A'
            if "Online" in text_block: location = "Online"
            elif "Remote" in text_block: location = "Remote"

            host_elem = tile.find('p', class_='hosted-by')
            host = host_elem.get_text(strip=True).replace('Hosted by', '').strip() if host_elem else 'N/A'
            
            all_hackathons.append({
                'title': title, 'link': link, 'location': location,
                'participants': participants, 'days_left': days_left, 'host': host
            })
            print(f"  > Scraped: {title}")

    except Exception as e:
        print(f"❌ An error occurred during scraping: {e}")
    finally:
        driver.quit()

    if not all_hackathons:
        print("\nScraping finished, but no hackathons were found. Exiting.")
        return

    # --- Step 1: Save the content to hackathons.csv ---
    save_to_csv(all_hackathons, 'hackathons.csv')

    # --- Step 2: Connect to the database and update ---
    upsert_to_mysql(all_hackathons)

if __name__ == "__main__":
    main()
