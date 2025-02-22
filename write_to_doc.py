#python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def setup_driver():
    """Set up the Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Start browser maximized
    driver = webdriver.Chrome(options=options)
    return driver

def create_google_doc(email, password, doc_name):
    """Log into Google, create a new Google Doc, and name it."""
    driver = setup_driver()
    
    try:
        # Open Google Docs
        driver.get("https://docs.google.com/document/u/0/")
        time.sleep(2)  # Wait for the page to load
        
        # Click on "Go to Google Docs"
        driver.find_element(By.XPATH, "//a[contains(text(), 'Go to Google Docs')]").click()
        time.sleep(2)

        # Log in to Google Account
        email_input = driver.find_element(By.XPATH, "//input[@type='email']")
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)
        time.sleep(2)

        password_input = driver.find_element(By.XPATH, "//input[@type='password']")
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)  # Wait for login to complete

        # Click on the "+" button to create a new document
        new_doc_button = driver.find_element(By.XPATH, "//div[@class='docs-homescreen-templates-templateview-preview']")
        new_doc_button.click()
        time.sleep(2)

        # Name the new document
        title_input = driver.find_element(By.XPATH, "//input[@placeholder='Untitled document']")
        title_input.click()
        title_input.clear()
        title_input.send_keys(doc_name)
        
        # Optionally, press Enter to save the title
        title_input.send_keys(Keys.RETURN)
        
        print(f"New document '{doc_name}' created successfully.")

    finally:
        time.sleep(5)  # Wait before closing the driver
        driver.quit()

if __name__ == "__main__":
    your_email = "jebeboone@gmail.com"  # Replace with your Google email
    your_password = "4276010b"  # Replace with your Google password
    document_name = "My New Document"  # Name of the new Google Doc
    create_google_doc(your_email, your_password, document_name)