from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from chrome_driver import setup_driver

def scrape_light_novel(url):
    driver = setup_driver()
    
    try:
        driver.get(url)
        
        # Use WebDriverWait for loading the title element
        title_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "entry-title"))
        )
        title_text = title_element.text.replace("Kawaikereba Hentai demo Suki ni Natte Kuremasu ka?", "").strip()
        
        # Extract text paragraphs until stopping point
        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        text_content = []
        
        for para in paragraphs:
            para_text = para.text
            
            # Skip unwanted content related to Discord, Facebook, Patreon, and specific links
            if any(keyword in para_text for keyword in ["Discord", "Facebook", "Patreon", "CClaw Translations", "Editor:", "discord.gg", "patreon.com"]):
                continue
            
            # Stop if the specific phrase is found
            if ("<span id=\"wordads-inline-marker\" style=\"display: none;\"></span>" in para.get_attribute("outerHTML") or
                "View all posts by" in para_text or
                "Allgemein" in para_text):
                break
            
            # Collect the paragraph text
            text_content.append(para_text)
        
        # Extract images
        images = driver.find_elements(By.CSS_SELECTOR, "figure.wp-block-image img")
        image_urls = [img.get_attribute("src") for img in images]
        
        # Combine text and images in order
        content = []
        text_idx, img_idx = 0, 0
        elements = driver.find_elements(By.XPATH, "//p | //figure")
        
        for elem in elements:
            if elem.tag_name == "p":
                if text_idx < len(text_content):
                    content.append(text_content[text_idx])
                    text_idx += 1
            elif elem.tag_name == "figure" and img_idx < len(image_urls):
                content.append(f"[IMAGE: {image_urls[img_idx]}]")
                img_idx += 1
        
        full_text = f"{title_text}\n\n" + "\n\n".join(content)
        return full_text
    
    except Exception as e:
        return f"An error occurred: {e}"
    
    finally:
        driver.quit()

if __name__ == "__main__":
    url = 'https://cclawtranslations.home.blog/2019/05/24/kawaikereba-hentai-demo-suki-ni-natte-kuremasu-ka-volume-4-chapte-4/'
    text = scrape_light_novel(url)
    print(text)
