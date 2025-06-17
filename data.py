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

def scrape_category_page(driver, url, category_name):
    """
    Navigates to a specific category URL, handles the 'Load More' button until all
    content is loaded, and then uses BeautifulSoup to parse and extract event data.
    
    Args:
        driver: The active Selenium WebDriver instance.
        url (str): The URL of the category page to scrape.
        category_name (str): The name of the category (e.g., "Competitions").

    Returns:
        list: A list of dictionaries, where each dictionary represents an event.
    """
    print(f"\nNavigating to {category_name} page: {url}")
    driver.get(url)
    time.sleep(2) # Allow initial page elements to render

    # --- MORE ROBUST "LOAD MORE" LOGIC ---
    print("Starting to load all events by clicking 'Load More'...")
    click_count = 0
    while True:
        try:
            # Increase wait time for more patience on slow networks
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Load More')]"))
            )
            # A more reliable click method
            driver.execute_script("arguments[0].click();", load_more_button)
            click_count += 1
            print(f"  > Clicked 'Load More' ({click_count} time(s))...")
            time.sleep(4) # Give ample time for new content to load after click
        except TimeoutException:
            print("Finished loading. 'Load More' button is no longer available.")
            break
        except Exception as e:
            print(f"An unexpected error occurred while clicking 'Load More': {e}")
            break
            
    # --- Hand over to BeautifulSoup for reliable parsing ---
    print("Handing over the fully loaded page to BeautifulSoup...")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    page_data = []
    event_cards = soup.find_all("app-competition-listing")
    
    if not event_cards:
        print(f"Warning: No event listings found for the '{category_name}' category.")
        return []

    print(f"Found {len(event_cards)} listings in '{category_name}'. Extracting details...")
    for card in event_cards:
        data = {}
        # Add the category to each record
        data['category'] = category_name

        # Title
        title_element = card.find("h2", class_="double-wrap")
        data['title'] = title_element.get_text(strip=True) if title_element else "N/A"

        # Organization
        org_element = card.find("p")
        data['organization'] = org_element.get_text(strip=True) if org_element else "N/A"

        # Tags
        tags_list = []
        skills_container = card.find("div", class_="skills")
        if skills_container:
            tag_elements = skills_container.find_all("span", class_="chip_text")
            for tag in tag_elements:
                tags_list.append(tag.get_text(strip=True))
        data['tags'] = ", ".join(tags_list) if tags_list else "N/A"

        # Deadline
        data['deadline'] = "N/A"
        other_fields = card.find_all("div", class_="seperate_box")
        for field in other_fields:
            field_text = field.get_text(strip=True)
            if "days left" in field_text or "day left" in field_text or "Closes" in field_text or "Ends" in field_text:
                data['deadline'] = field_text
                break
        
        page_data.append(data)

    return page_data

def main():
    """
    Main function to orchestrate the scraping of multiple categories from Unstop.
    """
    PAGES_TO_SCRAPE = [
        {"category": "Competitions", "url": "https://unstop.com/competitions"},
        {"category": "Hackathons", "url": "https://unstop.com/hackathons"},
        {"category": "Hiring Challenges", "url": "https://unstop.com/hiring-challenges"},
    ]

    print("--- Starting Unstop Multi-Category Scraper ---")
    
    # --- Setup WebDriver ---
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--start-maximized")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"Fatal Error: Could not set up WebDriver. {e}")
        return

    # Handle cookie banner on the first visit
    driver.get("https://unstop.com")
    try:
        cookie_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "accept-all-cookies")))
        cookie_button.click()
        print("Initial cookie consent banner accepted.")
    except TimeoutException:
        print("Initial cookie consent banner not found or already accepted.")

    # --- Loop through all pages and collect data ---
    all_unstop_data = []
    for page in PAGES_TO_SCRAPE:
        category_data = scrape_category_page(driver, page['url'], page['category'])
        all_unstop_data.extend(category_data)
        print(f"--- Finished scraping '{page['category']}'. Total items collected so far: {len(all_unstop_data)} ---")

    # --- Cleanup and Save ---
    print("\nAll categories scraped. Closing WebDriver.")
    driver.quit()

    if not all_unstop_data:
        print("No data was scraped from any category. Exiting.")
        return

    df = pd.DataFrame(all_unstop_data)
    
    # Reorder columns to have 'category' first for better readability
    df = df[['category', 'title', 'organization', 'tags', 'deadline']]
    
    output_filename = "unstop_all_events.csv"
    df.to_csv(output_filename, index=False, encoding='utf-8')

    print("\n" + "="*50)
    print("                FINAL SCRAPING SUMMARY")
    print("="*50)
    print(f"Total events scraped across all categories: {len(df)}")
    print(f"Data successfully saved to '{output_filename}'")
    print("\n--- SAMPLE OF COMBINED DATA ---")
    print(df.head())
    print("...")
    print(df.tail())
    print("="*50)


if __name__ == "__main__":
    main()
