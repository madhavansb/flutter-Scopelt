# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# from selenium.common.exceptions import TimeoutException, WebDriverException
# import time

# # Setup Chrome options for headless (optional)
# options = Options()
# options.add_argument('--headless')  # Comment this line to see the browser
# options.add_argument('--disable-gpu')
# options.add_argument('--window-size=1920,1080')  # Full viewport
# options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0')

# # Start Selenium WebDriver
# try:
#     driver = webdriver.Chrome(options=options)

#     # Correct URL
#     url = 'https://devpost.com/hackathons?status[]=open'
#     driver.get(url)

#     # Wait for initial container to load (max 10 seconds)
#     try:
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CLASS_NAME, 'hackathons-container'))
#         )
#     except TimeoutException:
#         print("Error: Timeout waiting for hackathons-container to load")
#         exit(1)

#     # Scroll to load all content
#     scroll_timeout = 120  # Max time to spend scrolling (seconds)
#     scroll_pause = 4  # Wait time after each scroll (seconds)
#     max_attempts = 30  # Max scroll attempts
#     start_time = time.time()
#     previous_tile_count = 0
#     attempt = 0

#     while attempt < max_attempts:
#         # Incremental scroll (smaller steps to trigger lazy loading)
#         driver.execute_script("window.scrollBy(0, 1000);")
#         attempt += 1
#         time.sleep(scroll_pause)  # Wait for content to load

#         # Parse current page to check tile count
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         container = soup.find('div', class_='hackathons-container')
#         if not container:
#             print("Error: 'hackathons-container' not found")
#             break

#         tiles = container.find_all('div', class_='hackathon-tile')
#         current_tile_count = len(tiles)
#         print(f"Attempt {attempt}: Found {current_tile_count} hackathon tiles")

#         # Check for "Load More" button and click if present
#         try:
#             load_more_button = WebDriverWait(driver, 2).until(
#                 EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Load More') or contains(text(), 'Show More')]"))
#             )
#             load_more_button.click()
#             print(f"Clicked 'Load More' button on attempt {attempt}")
#             time.sleep(scroll_pause)  # Wait after clicking
#         except:
#             pass  # No button or not clickable

#         # Scroll to bottom to ensure all content is triggered
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(scroll_pause)

#         # Check if new tiles loaded
#         if current_tile_count == previous_tile_count and attempt > 2:
#             print("No new tiles loaded, stopping scroll")
#             break
#         previous_tile_count = current_tile_count

#         # Stop if timeout reached
#         if (time.time() - start_time) > scroll_timeout:
#             print("Scroll timeout reached")
#             break

#     # Final scroll to bottom to ensure all content is loaded
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(scroll_pause)

#     # Final parse after scrolling
#     soup = BeautifulSoup(driver.page_source, 'html.parser')

#     # Find the hackathons container
#     container = soup.find('div', class_='hackathons-container')
#     if not container:
#         print("Error: 'hackathons-container' not found")
#         exit(1)

#     # Find all hackathon tiles
#     tiles = container.find_all('div', class_='hackathon-tile')
#     if not tiles:
#         print("Error: No 'hackathon-tile' elements found")
#         exit(1)

#     # Count elements with class 'main-content'
#     main_content_elements = soup.find_all(lambda tag: 'main-content' in tag.get('class', []))
#     main_content_count = len(main_content_elements)

#     # Print final results
#     print(f"\nFinal Results:")
#     print(f"Total hackathon tiles found: {len(tiles)}")
#     print(f"Elements with class 'main-content': {main_content_count}")

#     # Debug: Print details of main-content elements
#     if main_content_count > 0:
#         print("\nDetails of main-content elements:")
#         for i, element in enumerate(main_content_elements, 1):
#             print(f"Element {i}: Tag={element.name}, Classes={element.get('class', [])}")
#     else:
#         # Debug: List all classes on page to find similar classes
#         all_classes = set()
#         for tag in soup.find_all(True):
#             all_classes.update(tag.get('class', []))
#         print("\nNo 'main-content' elements found. All classes on page:", sorted(all_classes))

# except Exception as e:
#     print(f"An error occurred: {e}")
# finally:
#     driver.quit()



from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, WebDriverException
import csv
import time

# Setup Chrome options for headless (optional)
options = Options()
options.add_argument('--headless')  # Comment this line to see the browser
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')  # Full viewport
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0')

# Start Selenium WebDriver
try:
    driver = webdriver.Chrome(options=options)

    # Correct URL
    url = 'https://devpost.com/hackathons?status[]=open'
    driver.get(url)

    # Wait for initial container to load (max 10 seconds)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'hackathons-container'))
        )
    except TimeoutException:
        print("Error: Timeout waiting for hackathons-container to load")
        exit(1)

    # Scroll to load all content
    scroll_timeout = 120  # Max time to spend scrolling (seconds)
    scroll_pause = 4  # Wait time after each scroll (seconds)
    max_attempts = 30  # Max scroll attempts
    start_time = time.time()
    previous_tile_count = 0
    attempt = 0

    while attempt < max_attempts:
        # Incremental scroll
        driver.execute_script("window.scrollBy(0, 1000);")
        attempt += 1
        time.sleep(scroll_pause)

        # Parse current page to check tile count
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        container = soup.find('div', class_='hackathons-container')
        if not container:
            print("Error: 'hackathons-container' not found")
            break

        tiles = container.find_all('div', class_='hackathon-tile')
        current_tile_count = len(tiles)
        print(f"Attempt {attempt}: Found {current_tile_count} hackathon tiles")

        # Check for "Load More" button
        try:
            load_more_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Load More') or contains(text(), 'Show More')]"))
            )
            load_more_button.click()
            print(f"Clicked 'Load More' button on attempt {attempt}")
            time.sleep(scroll_pause)
        except:
            pass

        # Full scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)

        # Check if new tiles loaded
        if current_tile_count == previous_tile_count and attempt > 2:
            print("No new tiles loaded, stopping scroll")
            break
        previous_tile_count = current_tile_count

        if (time.time() - start_time) > scroll_timeout:
            print("Scroll timeout reached")
            break

    # Final scroll to ensure all content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause)

    # Final parse
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the hackathons container
    container = soup.find('div', class_='hackathons-container')
    if not container:
        print("Error: 'hackathons-container' not found")
        exit(1)

    # Find all hackathon tiles
    tiles = container.find_all('div', class_='hackathon-tile')
    if not tiles:
        print("Error: No 'hackathon-tile' elements found")
        exit(1)

    # Extract data from main-content elements within tiles
    hackathon_data = []
    main_content_elements = container.find_all('div', class_='main-content')
    print(f"Found {len(main_content_elements)} main-content elements")

    for i, element in enumerate(main_content_elements, 1):
        # Initialize data dictionary
        data = {
            'title': 'N/A',
            'link': 'N/A',
            'status': 'N/A',
            'location': 'N/A',
            'prize_money': 'N/A',
            'participants': 'N/A',
            'host': 'N/A',
            'submission_dates': 'N/A',
            'themes': 'N/A'
        }

        # Title: Look for <h3> or <h2> with class like 'hackathon-title'
        title_elem = element.find(['h3', 'h2'], class_=lambda x: x and 'title' in x.lower())
        data['title'] = title_elem.get_text(strip=True) if title_elem else 'N/A'

        # Link: Look for <a> wrapping the tile or title
        link_elem = element.find('a', href=True)
        data['link'] = link_elem['href'] if link_elem and link_elem['href'].startswith('http') else 'N/A'

        # Status: Look for text indicating status (e.g., 'Open', 'Closed')
        status_elem = element.find(['span', 'div'], class_=lambda x: x and 'status' in x.lower())
        data['status'] = status_elem.get_text(strip=True) if status_elem else 'N/A'

        # Location: Look for text like 'Online' or city name
        location_elem = element.find(['span', 'p'], class_=lambda x: x and ('location' or 'online' in x.lower()))
        data['location'] = location_elem.get_text(strip=True) if location_elem else 'N/A'

        # Prize Money: Look for dollar amount
        prize_elem = element.find(['span', 'div'], class_=lambda x: x and 'prize' in x.lower())
        data['prize_money'] = prize_elem.get_text(strip=True) if prize_elem else 'N/A'

        # Participants: Look for number of participants
        participants_elem = element.find(['span', 'div'], class_=lambda x: x and 'participant' in x.lower())
        data['participants'] = participants_elem.get_text(strip=True) if participants_elem else 'N/A'

        # Host: Look for organizer name
        host_elem = element.find(['span', 'p'], class_=lambda x: x and 'host' in x.lower())
        data['host'] = host_elem.get_text(strip=True) if host_elem else 'N/A'

        # Submission Dates: Look for date range
        dates_elem = element.find(['time', 'span', 'div'], class_=lambda x: x and ('date' or 'submission' in x.lower()))
        data['submission_dates'] = dates_elem.get_text(strip=True) if dates_elem else 'N/A'

        # Themes: Look for tags or keywords
        themes_elem = element.find(['div', 'ul'], class_=lambda x: x and 'theme' in x.lower())
        if themes_elem:
            themes = [t.get_text(strip=True) for t in themes_elem.find_all(['span', 'li'])]
            data['themes'] = ', '.join(themes) if themes else 'N/A'
        else:
            data['themes'] = 'N/A'

        hackathon_data.append(data)
        print(f"Processed hackathon {i}: {data['title']}")

    # Write to CSV
    csv_file = 'hackathons.csv'
    headers = ['title', 'link', 'status', 'location', 'prize_money', 'participants', 'host', 'submission_dates', 'themes']
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(hackathon_data)
    print(f"\nData saved to {csv_file}")

    # Print final counts
    print(f"\nFinal Results:")
    print(f"Total hackathon tiles found: {len(tiles)}")
    print(f"Elements with class 'main-content': {len(main_content_elements)}")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
