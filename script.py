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

def extract_company_info(cin_queue, lock, counter):
    # Initialize the Selenium webdriver with Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-minimized")  # Minimize the browser window
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://finanvo.in/")  # Replace the URL here

        while not cin_queue.empty():
            cin = cin_queue.get()

            # Check if the CIN number already has an email associated with it in the CSV file
            if check_email_exists_in_csv(cin):
                print(f"Skipping CIN {cin}: Email already exists")
                continue

            # Attempt to extract email, retrying if unsuccessful
            while True:
                try:
                    driver.get("https://finanvo.in/")
                    # Find the search input field and enter the CIN number
                    search_input = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search for a company"]'))
                    )
                    search_input.clear()
                    search_input.send_keys(cin)

                    # Introduce a 1-second delay (you may need to adjust this duration)
                    time.sleep(1)

                    # Click the search button using JavaScript to handle Angular behavior
                    driver.execute_script('document.querySelector("button[style*=\'background-color: rgb(112, 170, 56)\']").click()')

                    # Wait for the company name link to be clickable
                    company_name_link = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, '//a[@href="javascript:void(0)"]'))
                    )

                    # Execute JavaScript to click on the company name link
                    driver.execute_script("arguments[0].click();", company_name_link)

                    # Wait for the page to load (you may need to adjust the duration)
                    time.sleep(3)

                    # Find the email element using more robust locating strategy
                    email_element = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//li[@class="flex flex-space-between" and contains(.//span[@class="name"], "Email")]/span[@class="value"]//span[@class="number"]'))
                    )

                    # Extract the email value
                    updated_email = email_element.text.strip()

                    # Print email information and count
                    lock.acquire()
                    try:
                        counter.value += 1
                        print(f"Email for CIN {cin}: {updated_email} - Count: {counter.value}")
                    finally:
                        lock.release()

                    # Update the email part for the CIN number in the CSV file
                    update_email_in_csv(cin, updated_email, lock)

                    break  # Exit retry loop if successful
                except Exception as e:
                    print(f"Error processing CIN {cin}: {e}")
                    print("Retrying CIN entry...")

    except Exception as e:
        print(f"Error processing CIN {cin}: {e}")

    finally:
        # Close the browser window when done
        driver.quit()


def is_valid_email(email):
    # Regular expression pattern to validate email format
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def check_email_exists_in_csv(cin):
    with open(csvFile, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row[firstCol] == cin and is_valid_email(row[secondCol]):
                return True
    return False



def update_email_in_csv(cin, updated_email, lock):
    # Acquire the lock before accessing the CSV file
    lock.acquire()
    try:
        # Read the contents of the CSV file
        with open(csvFile, 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        # Update the email for the corresponding CIN number
        for row in rows:
            if row[firstCol] == cin:
                row[secondCol] = updated_email

        # Write the updated rows back to the CSV file
        with open(csvFile, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    except Exception as e:
        print(f"Error updating CSV for CIN {cin}: {e}")
    finally:
        # Release the lock after updating the CSV file
        lock.release()

# Read the CIN numbers from the CSV file
csvFile = '5k to 11k.csv'
firstCol = 'CIN'
secondCol = 'EMAIL'

# Create a lock to ensure exclusive access to the CSV file
lock = Lock()

# Define a counter variable for email entries
counter = multiprocessing.Value('i', 0)

# Define the maximum number of worker processes
max_processes = 8  # Adjust this number as needed

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
        process = Process(target=extract_company_info, args=(cin_queue, lock, counter))
        process.start()
        processes.append(process)

    # Wait for all processes to finish
    for process in processes:
        process.join()
