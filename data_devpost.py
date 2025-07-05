from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
import time
import csv
import re

# Setup Chrome options
options = Options()
options.add_argument('--headless')  # Run without UI
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0')

# Launch WebDriver
driver = webdriver.Chrome(options=options)

try:
    url = 'https://devpost.com/hackathons?status[]=open'
    driver.get(url)

    # Wait for container to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'hackathons-container'))
    )

    # Scroll to load content
    scroll_pause = 4
    max_attempts = 30
    previous_count = 0

    for attempt in range(max_attempts):
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(scroll_pause)

        # Click Load More if exists
        try:
            load_more = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Load More') or contains(text(), 'Show More')]"))
            )
            load_more.click()
            time.sleep(scroll_pause)
        except:
            pass

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        container = soup.find('div', class_='hackathons-container')
        tiles = container.find_all('div', class_='hackathon-tile')
        current_count = len(tiles)

        print(f"Attempt {attempt + 1}: {current_count} hackathon tiles")

        if current_count == previous_count and attempt > 2:
            break
        previous_count = current_count

    # Parse final results
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tiles = soup.find_all('div', class_='hackathon-tile')

    hackathon_data = []
    for i, tile in enumerate(tiles, 1):
        data = {
            'title': 'N/A',
            'link': 'N/A',
            'location': 'N/A',
            'prize_money': 'N/A',
            'participants': 'N/A',
            'days_left': 'N/A',
            'host': 'N/A'
        }

        # Title
        title_elem = tile.find(['h2', 'h3'])
        if title_elem:
            data['title'] = title_elem.get_text(strip=True)

        # Link
        link_elem = tile.find('a', href=True)
        if link_elem:
            href = link_elem['href']
            data['link'] = href if href.startswith('http') else f"https://devpost.com{href}"

        # Full text block
        text_block = tile.get_text(separator=' ', strip=True)

        # Days left
        days_match = re.search(r'(\d+\s+days?\s+left)', text_block, re.IGNORECASE)
        if days_match:
            data['days_left'] = days_match.group(1)

        # Prize Money
        prize_match = re.search(r'(\$\d[\d,]*)', text_block)
        if prize_match:
            data['prize_money'] = prize_match.group(1)

        # Participants
        participants_match = re.search(r'(\d[\d,]*)\s+participants', text_block, re.IGNORECASE)
        if participants_match:
            count = participants_match.group(1).replace(',', '')
            data['participants'] = f"{count} participants"

        # Location (Online or Remote or N/A fallback)
        if "Online" in text_block:
            data['location'] = "Online"
        elif "Remote" in text_block:
            data['location'] = "Remote"

        # Host or Description
        host_elem = tile.find('p') or tile.find('span')
        if host_elem:
            data['host'] = host_elem.get_text(strip=True)

        hackathon_data.append(data)
        print(f"[{i}] {data['title']} - {data['participants']} - {data['prize_money']}")

    # Save to CSV
    headers = ['title', 'link', 'location', 'prize_money', 'participants', 'days_left', 'host']
    with open('hackathons.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(hackathon_data)

    print("\n✅ Data saved to 'hackathons.csv'")
    print(f"✅ Total hackathons scraped: {len(hackathon_data)}")

except Exception as e:
    print(f"❌ Error occurred: {e}")

finally:
    driver.quit()
