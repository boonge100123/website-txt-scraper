#python

from chrome_driver import setup_driver
from selenium.webdriver.common.by import By
import time

def scrape_light_novel(url):
    driver = setup_driver()
    
    try:
        driver.get(url)
        time.sleep(2)  # Allow the page to load
        
        # Extract title
        title_element = driver.find_element(By.CLASS_NAME, "entry-title")
        title_text = title_element.text.replace("Kawaikereba Hentai demo Suki ni Natte Kuremasu ka?", "").strip()
        
        # Extract text paragraphs until stopping point
        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        text_content = []
        for para in paragraphs:
            if "unable to move from that spot" in para.text:
                text_content.append(para.text)
                break
            text_content.append(para.text)
        
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

def main():
    url = 'https://cclawtranslations.home.blog/2019/02/23/kawaikereba-hentai-demo-suki-ni-natte-kuremasu-ka-volume-1-chapter-1/'
    result = scrape_light_novel(url)
    print(result)

if __name__ == "__main__":
    main()
