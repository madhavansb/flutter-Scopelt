import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scrape_with_blueprint():
    """
    This script works because it is built from the exact HTML structure provided by the user.
    1. Selenium loads the full page by handling the "Load More" button.
    2. BeautifulSoup parses the final HTML using the correct, verified selectors.
    """
    # 1. --- Use Selenium to get the complete, fully-loaded page HTML ---
    print("Setting up WebDriver...")
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--start-maximized")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"Error setting up WebDriver: {e}")
        return

    target_url = "https://unstop.com/competitions"
    print(f"Navigating to {target_url}...")
    driver.get(target_url)

    # Handle cookie banner
    try:
        cookie_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "accept-all-cookies")))
        cookie_button.click()
        print("Cookie consent banner accepted.")
    except TimeoutException:
        print("Cookie consent banner not found or already accepted.")

    # Click "Load More" until all events are visible
    print("Loading all events by clicking the 'Load More' button...")
    while True:
        try:
            load_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Load More')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
            time.sleep(1)
            load_more_button.click()
            print("Clicked 'Load More'.")
            time.sleep(3)
        except TimeoutException:
            print("All events have been loaded.")
            break

    # 2. --- Pass the final HTML to BeautifulSoup ---
    print("\nHanding over the complete page source to BeautifulSoup...")
    page_source_html = driver.page_source
    driver.quit() # We're done with the browser
    
    soup = BeautifulSoup(page_source_html, "html.parser")

    # 3. --- Extract data using the CORRECT selectors from your blueprint ---
    print("Extracting data using the correct structure...")
    all_events_data = []
    
    # The main container for each event is the <app-competition-listing> tag
    event_cards = soup.find_all("app-competition-listing")
    
    if not event_cards:
        print("CRITICAL ERROR: Could not find any '<app-competition-listing>' tags. The core structure may have changed.")
        return

    print(f"Success! Found {len(event_cards)} event listings.")

    for i, card in enumerate(event_cards):
        data = {}

        # Title
        title_element = card.find("h2", class_="double-wrap")
        data['title'] = title_element.get_text(strip=True) if title_element else "N/A"

        # Organization
        org_element = card.find("p") # The <p> tag is unique at this level
        data['organization'] = org_element.get_text(strip=True) if org_element else "N/A"

        # Tags (inside the 'skills' div)
        tags_list = []
        skills_container = card.find("div", class_="skills")
        if skills_container:
            tag_elements = skills_container.find_all("span", class_="chip_text")
            for tag in tag_elements:
                tags_list.append(tag.get_text(strip=True))
        data['tags'] = ", ".join(tags_list) if tags_list else "N/A"

        # Other details like deadline and registrations
        data['deadline'] = "N/A"
        data['registrations'] = "N/A"
        other_fields = card.find_all("div", class_="seperate_box")
        for field in other_fields:
            field_text = field.get_text(strip=True)
            if "days left" in field_text or "day left" in field_text or "Closes" in field_text or "Ends" in field_text:
                data['deadline'] = field_text
            elif "Registered" in field_text:
                data['registrations'] = field_text

        all_events_data.append(data)
        print(f"  - Extracted: {data['title']}")

    # 4. --- Save the final, correct data to a CSV file ---
    df = pd.DataFrame(all_events_data)
    output_filename = "unstop_event_data_CORRECT.csv"
    df.to_csv(output_filename, index=False, encoding='utf-8')
    
    print("\n" + "="*50)
    print("                SCRAPING SUMMARY")
    print("="*50)
    print(f"Total events scraped: {len(df)}")
    print(f"Data successfully saved to '{output_filename}'")
    print("\n--- SAMPLE OF CORRECTLY EXTRACTED DATA ---")
    print(df.head())
    print("="*50)

if __name__ == "__main__":
    scrape_with_blueprint()
