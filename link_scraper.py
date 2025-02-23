from chrome_driver import setup_driver  # Import the setup_driver function
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def extract_volume_data(driver):
    """Extracts volume numbers and related links from the page."""
    volume_data = {}

    # Wait for elements containing the keyword "Volume" to load
    volume_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//*[contains(text(), 'Volume')]"))
    )

    for element in volume_elements:
        text = element.text
        match = re.search(r'Volume\s*(\d+)', text)
        if match:
            volume_number = int(match.group(1))
            volume_name = text.strip()
            volume_data[volume_number] = {
                'volume_name': volume_name,
                'chapters': {}
            }
    
    return volume_data

def extract_specific_links(driver, volume_data):
    """Extracts specific links from the page and adds them to volume data."""
    specific_link_texts = [
        "Illustrations", "Prologue", "Chapter 1", "Chapter 2",
        "Chapter 3", "Chapter 4", "Chapter 5", "Epilogue", "Afterword"
    ]
    
    for volume_number in volume_data.keys():
        for text in specific_link_texts:
            try:
                link_element = driver.find_element(By.LINK_TEXT, text)
                # Add chapter name and link to the corresponding volume
                volume_data[volume_number]['chapters'][text] = link_element.get_attribute('href')
            except Exception as e:
                print(f"Could not find link for: {text}")

def extract_links(url):
    """Extracts book links and volume numbers from the provided URL."""
    driver = setup_driver()
    
    try:
        driver.get(url)

        # Extract volume data
        volume_data = extract_volume_data(driver)
        print("Volume data found:")
        
        # Extract specific links and update volume data
        extract_specific_links(driver, volume_data)

        # # Print the volume data dictionary
        # for volume, data in volume_data.items():
        #     print('--------------------------------------------------------------')
        #     print(f"{data['volume_name']} (Volume {volume}):")
        #     for chapter, link in data['chapters'].items():
        #         print(f"  {chapter}: {link}")
        #     print('--------------------------------------------------------------')

        return volume_data  # Return the volume data

    finally:
        driver.quit()

if __name__ == "__main__":
    url = "https://cclawtranslations.home.blog/kawaikereba-hentai-demo-suki-ni-natte-kuremasu-ka-toc/"
    volume_data = extract_links(url)
    print(volume_data)
