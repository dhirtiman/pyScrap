# Company Email Updater

This Python script is designed to update company emails in a CSV file by scraping information from the Finavo website.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python (3.x recommended)
- venv
- Selenium WebDriver
- Chrome WebDriver
- Required Python packages (install using `pip`):
  - `selenium`

## Installation

1. **Python Installation**: If you haven't already installed Python, download and install it from the [official Python website](https://www.python.org/).

2. **Venv and Selenium Installation**: Install venv and Selenium package:
   ```bash
   python -m venv venv
   pip install selenium
   ```

3. **Chrome WebDriver**: Download the Chrome WebDriver compatible with your Chrome browser version and place it in a directory accessible by your system. You can download the Chrome WebDriver from the [official Chrome WebDriver website](https://sites.google.com/a/chromium.org/chromedriver/downloads).


## Usage

1. **Prepare CSV File**: Prepare a CSV file with columns named `CIN` and `EMAIL` containing the company identification numbers (CIN) and no emails

2. **Specify CSV File**: Open the `script.py` file and specify the path to your CSV file on line 130:
   ```python
   csv_file = 'path/to/your/csv_file.csv'
   ```

3. **Specify Number of Instances**: If you wish to run multiple instances of the script concurrently, specify the desired number on line 141:
   ```python
   max_processes = 5  # Adjust the number of instances as needed
   ```

4. **Run the Script**: Run the script by executing the following command in your terminal:
   ```bash
   python script.py
   ```


5. **Email removal script**: Run the removeEmail.py script to remove emails against call CIN entries from  a csv file.
    ```bash
    python removeEmail.py
    ```
6. **Remove duplicate rows scrip**:  Run this script to remove duplicate rows from the csv file.
    ```bash
    python compare.py
    ```


## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This project is solely for EDUCATIONAL PURPOSES ONLY. Any abuse is strictly no recommended.
