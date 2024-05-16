import csv
import re
import time
import multiprocessing
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from multiprocessing import Lock, Process, Queue
import os
import shutil

def extract_company_info(cin_queue, lock, counter):
    download_dir = "C:\\Users\\dhirt\\Desktop\\pyScrap\\downloadFromSite"
    # Verify the download directory
    if not os.path.exists(download_dir):
        print(f"Creating download directory: {download_dir}")
        os.makedirs(download_dir)
    else:
        print(f"Using existing download directory: {download_dir}")

    # Initialize the Selenium webdriver with Chrome options
    chrome_options = Options()
    main_download_dir = download_dir+"\\download"
    prefs = {
        "download.default_directory": main_download_dir,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    print("Chrome WebDriver initialized with download directory:", download_dir)

    try:
        driver.get("https://finanvo.in/company/profile/ACG-4904/INIYA-AESTHETICS-&-WELLNESS-CLINIC-LLP")  # Replace the URL here

        while not cin_queue.empty():
            cin = cin_queue.get()

            if alreadyDownloaded(download_dir, cin):
                print(f"Skipping for {cin}: It is already downloaded.")
                continue

            # Attempt to extract email, retrying if unsuccessful
            while True:
                try:
                    
                    # Find the search input field and enter the CIN number
                    search_input = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//input[@placeholder="Search for a company"]'))
                    )
                    search_input.clear()
                    search_input.send_keys(cin)
                    search_input.send_keys(Keys.ENTER)
                    
                    time.sleep(3)
                    
                    driver.execute_script(
                        'document.querySelector("#ngb-typeahead-0-0 > ngb-highlight > span").click()')


                    # Wait for the page to load (you may need to adjust the duration)
                    time.sleep(3)
                    
                    # Download the CSV file
                    driver.execute_script(
                        'document.querySelector("#section-about > app-about > div.flex-row.flex-space-between.flex-gap-8 > div.col-lg-4.col-xl-4.col-12.p-0.print-hide > div:nth-child(1) > div > div:nth-child(1) > ul > li:nth-child(3) > a").click()')

                    # Wait for the download to complete
                    time.sleep(3)

                    

                    lock.acquire()
                    try:
                        print("Processing CIN:", cin)
                        filename = max([os.path.join(main_download_dir, f) for f in os.listdir(main_download_dir)], key=os.path.getctime)
                        shutil.move(filename, os.path.join(download_dir, cin + ".csv"))
                    finally:
                        lock.release()

                    break  # Exit retry loop if successful
                except Exception as e:
                    print(f"Error processing CIN {cin}: {e}")
                    print("Retrying CIN entry...")

    except Exception as e:
        print(f"Error in main processing loop: {e}")

    finally:
        # Close the browser window when done
        driver.quit()

def alreadyDownloaded(download_dir, cin):
    file_path = os.path.join(download_dir, cin + ".csv")
    return os.path.exists(file_path)

# Read the CIN numbers from the CSV file
csvFile = 'input/cin name 6k to 12k (1).csv'
firstCol = 'Company names'
secondCol = 'emails'

max_processes = 1  # Adjust this number as needed

# Create a lock to ensure exclusive access to the CSV file
lock = Lock()

# Define a counter variable for email entries
counter = multiprocessing.Value('i', 0)

if __name__ == '__main__':
    # Read the CIN numbers from the CSV file
    cin_queue = Queue()
    with open(csvFile, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cin_queue.put(row[firstCol])

    # Create and start worker processes
    processes = []
    for _ in range(max_processes):
        process = Process(target=extract_company_info, args=(
            cin_queue, lock, counter))
        process.start()
        processes.append(process)

    # Wait for all processes to finish
    for process in processes:
        process.join()
