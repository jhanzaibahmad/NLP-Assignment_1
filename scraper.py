#!/usr/bin/env python3
import os
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://pakistancode.gov.pk/english/LGu0xVD.php"
OUTPUT_FILE = "PakistanCode_21I0792.json"
DOWNLOAD_DIR = "PakistanLaw_pdfs"

# Ensure folders
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# JSON file init
if not os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"Laws": []}, f, indent=2)

def append_to_json(new_entry):
    """Incrementally append a new law entry to the JSON file."""
    with open(OUTPUT_FILE, "r+", encoding="utf-8") as f:
        data = json.load(f)
        data["Laws"].append(new_entry)
        f.seek(0)
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.truncate()

def scroll_page(driver):
    """Scroll to bottom to load dynamic content."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# Configure Selenium (normal mode, not headless)
options = Options()
options.add_argument("--start-maximized")  # open browser maximized

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

try:
    print("Opening site:", BASE_URL)
    driver.get(BASE_URL)
    scroll_page(driver)  # Ensure categories load

    # Wait for categories to load
    WebDriverWait(driver, 20).until(
        EC.visibility_of_all_elements_located((By.XPATH, '//section[contains(@class,"content-section")]//ul//a'))
    )

    # Step 1: get all categories
    categories = driver.find_elements(By.XPATH, '//section[contains(@class,"content-section")]//ul//a')
    print(f"Found {len(categories)} categories.")

    # Step 2: iterate over categories
    for category in categories:
        cat_name = category.text.strip()
        cat_url = category.get_attribute("href")
        print(f"\nOpening category: {cat_name} -> {cat_url}")

        driver.get(cat_url)
        scroll_page(driver)

        # Step 3: collect all laws in category (store plain text + url, not WebElements)
        laws_data = []
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"accordion-section-title")]//a'))
            )
            laws = driver.find_elements(By.XPATH, '//div[contains(@class,"accordion-section-title")]//a')
            for law in laws:
                law_name = law.text.strip().replace("/", "_").replace("\\", "_")
                law_url = law.get_attribute("href")
                laws_data.append({"name": law_name, "url": law_url})
        except:
            print(f"No laws found in {cat_name}")
            continue

        print(f"Found {len(laws_data)} laws in '{cat_name}'")

        # Step 4: loop through laws
        for law in laws_data:
            law_name = law["name"]
            law_url = law["url"]
            print(f"- Opening law: {law_name} -> {law_url}")

            driver.get(law_url)
            time.sleep(2)

            # Extract Act No
            try:
                act_no = driver.find_element(By.XPATH, '//div[@id="act-no"]').text.strip()
            except:
                act_no = "Not Available"

            # Extract Promulgation Date
            try:
                promulgation_date = driver.find_element(By.XPATH, '//div[@id="promulgation-date"]').text.strip()
            except:
                promulgation_date = "Not Available"

            # Extract PDF link
            pdf_file = "Not Available"
            try:
                pdf_link_elem = driver.find_element(By.XPATH, '//a[contains(@href,".pdf")]')
                pdf_url = pdf_link_elem.get_attribute("href")
                pdf_file = os.path.join(DOWNLOAD_DIR, f"{law_name}.pdf")

                # Download PDF immediately
                response = requests.get(pdf_url, stream=True)
                if response.status_code == 200:
                    with open(pdf_file, "wb") as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                else:
                    pdf_file = "Not Available"
            except:
                pass

            # Prepare JSON entry
            law_entry = {
                "Category": cat_name,
                "Total_Count": len(laws_data),
                "Laws_List": [
                    {
                        "Law_Name": law_name,
                        "Details": {
                            "Category": cat_name,
                            "Act_No": act_no,
                            "Promulgation_Date": promulgation_date,
                            "Pdf_File": pdf_file
                        }
                    }
                ]
            }

            # Save incrementally
            append_to_json(law_entry)

finally:
    driver.quit()
