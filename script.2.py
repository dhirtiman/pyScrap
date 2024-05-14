import csv
import re
import time
import multiprocessing
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from multiprocessing import Lock, Process, Queue
import os


def extract_company_info(cin_queue, lock, counter):
    download_dir = "C:\\Users\\dhirt\\Desktop\\pyScrap\\downloadFromSite"
    # Update this path
   # Verify the download directory
    if not os.path.exists(download_dir):
        print(f"Creating download directory: {download_dir}")
        os.makedirs(download_dir)
    else:
        print(f"Using existing download directory: {download_dir}")

    # Initialize the Selenium webdriver with Chrome options
    chrome_options = Options()
    # Minimize the browser window

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    print("Chrome WebDriver initialized with download directory:", download_dir)

    try:
        driver.get("https://finanvo.in/")  # Replace the URL here

        while not cin_queue.empty():
            cin = cin_queue.get()

            # Attempt to extract email, retrying if unsuccessful
            while True:
                try:
                    driver.get("https://finanvo.in/")
                    # Find the search input field and enter the CIN number
                    search_input = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//input[@placeholder="Search for a company"]'))
                    )
                    search_input.clear()
                    search_input.send_keys(cin)

                    # Introduce a 1-second delay (you may need to adjust this duration)
                    time.sleep(3)

                    # Click the search button using JavaScript to handle Angular behavior
                    driver.execute_script(
                        'document.querySelector("button[style*=\'background-color: rgb(112, 170, 56)\']").click()')

                    # Wait for the company name link to be clickable
                    company_name_link = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//a[@href="javascript:void(0)"]'))
                    )

                    # Execute JavaScript to click on the company name link
                    driver.execute_script(
                        "arguments[0].click();", company_name_link)

                    # Wait for the page to load (you may need to adjust the duration)
                    time.sleep(3)

                    drop_down_button = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable(
                            (By.XPATH,
                             '//*[@id="section-about"]/app-about/div[1]/div[2]/div[1]/div/div[1]'))
                    )
                    driver.execute_script(
                        "arguments[0].click();", drop_down_button)

                    time.sleep(1)

                    csv_downloadLink = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//*[@id="section-about"]/app-about/div[1]/div[2]/div[1]/div/div[1]/ul/li[2]/a'))
                    )

                    driver.execute_script(
                        "arguments[0].click();", csv_downloadLink)

                    # Wait for the download to complete
                    time.sleep(5)

                    files = os.listdir(download_dir)
                    print("Downloaded files: ", files)

                    lock.acquire()
                    try:
                        print("Processing CIN:", cin)
                        # counter.value += 1
                        # print(f"Email for CIN {cin}: {updated_email} - Count: {counter.value}")
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


# Read the CIN numbers from the CSV file
csvFile = 'input/cin name 6k to 12k (1).csv'
firstCol = 'Company names'
secondCol = 'emails'

max_processes = 1  # Adjust this number as needed

# Set download directory

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
            cin_queue, lock, counter, ))
        process.start()
        processes.append(process)

    # Wait for all processes to finish
    for process in processes:
        process.join()
