"""
BookScraper.py
Scrapes books.toscrape.com with Selenium and saves results to JSON.
"""

import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Custom settings, change as needed
URL = "https://books.toscrape.com/"
MAX_PAGES = 3 # max pages is up to 50 (sets to 3 for demo purposes, to avoid long scraping time and GROQ API Rate Limit)
SAVE_FILE = "results/books.json"


class BookScraper:
    ROBOT_LIBRARY_SCOPE = "SUITE"   # keep one shared instance for the whole test suite

    def __init__(self):
        self.driver = None
        self.all_books = []

    def start_browser(self):
        options = webdriver.EdgeOptions()
        options.add_argument("--headless=new")
        self.driver = webdriver.Edge(options=options)
        self.driver.get(URL)

    def scrape_books(self):
        self.start_browser()
        wait = WebDriverWait(self.driver, 5)
        page_number = 1

        while page_number <= MAX_PAGES:
            print("scraping page " + str(page_number))
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product_pod")))

            books = self.driver.find_elements(By.CLASS_NAME, "product_pod")

            # gather data of each book and list them in all_books array
            for book in books:
                try:
                    title = book.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("title")
                    price = book.find_element(By.CLASS_NAME, "price_color").text
                    stock = book.find_element(By.CLASS_NAME, "instock").text

                    self.all_books.append({
                        "title": title,
                        "price": price,
                        "stock": stock
                    })
                except:
                    print("something went wrong with one book, skipping it")

            # click next page button
            try:
                next_button = self.driver.find_element(By.CSS_SELECTOR, "li.next a")
                next_button.click()
                page_number = page_number + 1
            except:
                print("no more pages, stopping")
                break

        self.driver.quit()

    def get_scraped_books(self):
        return self.all_books

    def save_to_json(self):
        os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
        with open(SAVE_FILE, "w") as f:
            json.dump(self.all_books, f, indent=4)
        print("saved " + str(len(self.all_books)) + " books to " + SAVE_FILE)

# start the scraper if this file is run directly
if __name__ == "__main__":
    scraper = BookScraper()
    scraper.scrape_books()
    scraper.save_to_json()