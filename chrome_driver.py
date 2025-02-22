import sys
import os
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def setup_driver():
    """Sets up and returns a Chrome WebDriver instance with user profile support."""
    options = webdriver.ChromeOptions()
    
    chrome_user_data_path = get_chrome_user_data_dir()
    options.add_argument(f"--user-data-dir={chrome_user_data_path}")
    options.add_argument("--profile-directory=Default")  # Change if using a different profile
    # options.add_argument("--headless")  # Run in headless mode for no GUI
    # options.add_argument("--disable-gpu")  # Disable GPU acceleration
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver

def get_chrome_user_data_dir():
    """Returns the default Chrome user data directory based on the OS."""
    if sys.platform == "win32":
        return os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
    elif sys.platform == "darwin":
        return os.path.expanduser("~/Library/Application Support/Google/Chrome")
    elif sys.platform.startswith("linux"):
        return os.path.expanduser("~/.config/google-chrome")
    else:
        raise RuntimeError("Unsupported operating system")

def main():
    """Main function to set up the environment and test WebDriver."""
    driver = setup_driver()  # Set up the WebDriver
    
    try:
        driver.get("https://www.youtube.com/watch?v=xvFZjo5PgG0")
        play_button = driver.find_element(By.CSS_SELECTOR, "button.ytp-large-play-button.ytp-button")
        play_button.click()
        
        # Print the title of the page
        print(driver.title)
        
        # Keep YouTube open for 30 seconds
        time.sleep(30)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
