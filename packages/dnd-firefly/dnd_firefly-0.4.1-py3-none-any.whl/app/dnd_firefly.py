import os
import argparse
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Default file path
DEFAULT_FILE_PATH = "./file.fits"


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Upload a file or a URL in the Firefly Viewer."
    )
    parser.add_argument(
        "file_value",
        nargs="?",
        default=DEFAULT_FILE_PATH,
        help="Path to the local file or URL to load into Firefly Viewer. (default: ./file.fits)",
    )
    args = parser.parse_args()

    input_value = args.file_value

    # Determine if input is a file path or a URL
    if os.path.isfile(input_value):
        # Call your main functionality here, using file_path
        run_dnd_firefly(input_value)
    elif input_value.startswith('http://') or input_value.startswith('https://'):
        run_dnd_firefly_url(input_value)
    else:
        print("Error: The input must be a valid file path or a URL.")
        sys.exit(1)
    

# # Parse command-line arguments
# parser = argparse.ArgumentParser(description="Drag and drop file upload using Selenium")
# parser.add_argument("file_path", help="The path to the file to be uploaded")
# args = parser.parse_args()
# Main function to handle drag-and-drop
def run_dnd_firefly(file_path):
    # Convert to absolute path
    absolute_file_path = os.path.abspath(file_path)
    options = ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # Initialize the WebDriver
    driver = webdriver.Chrome(options)

    try:
        # Open the target web page
        driver.get(
            "https://irsa.ipac.caltech.edu/irsaviewer/?__action=layout.showDropDown&view=FileUploadDropDownCmd"
        )

        # Allow the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "drop-down"))
        )

        # Locate the file input element if available
        file_input = driver.find_element(By.ID, "upload-file")

        # # Path to the local file to be uploaded
        # file_path = '/Users/ejoliet/Downloads/file.fits'

        # Set the file path to the input element
        file_input.send_keys(absolute_file_path)

        # Simulate drag-and-drop if necessary (e.g., if there are additional steps required after selecting the file)
        drop_area = driver.find_element(By.ID, "drop-down")
        driver.execute_script(
            """
            var dropArea = arguments[0];
            var fileInput = arguments[1];
            var file = fileInput.files[0];

            var dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);

            var dragStartEvent = new DragEvent('dragstart', {
                dataTransfer: dataTransfer
            });
            var dropEvent = new DragEvent('drop', {
                dataTransfer: dataTransfer
            });
            var dragEndEvent = new DragEvent('dragend', {
                dataTransfer: dataTransfer
            });

            dropArea.dispatchEvent(dragStartEvent);
            dropArea.dispatchEvent(dropEvent);
            dropArea.dispatchEvent(dragEndEvent);
        """,
            drop_area,
            file_input,
        )

        # Keep the browser open
        print("Data loaded successfully.")
        print("The browser will remain open. Close it manually to end the session.")

        main_window_handle = driver.current_window_handle

        while True:
            if main_window_handle not in driver.window_handles:
                print("The tab was closed.")
                break
            time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Optionally handle any cleanup if needed
        driver.quit()  # Ensure the browser closes
def run_dnd_firefly_url(url):
    # Existing code to handle file drag-and-drop
    # Initialize the Selenium WebDriver
    options = ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # Initialize the WebDriver
    driver = webdriver.Chrome(options)

    try:
        # Open the target web page
        driver.get(
            "https://irsa.ipac.caltech.edu/irsaviewer/?__action=layout.showDropDown&view=FileUploadDropDownCmd"
        )

        # Allow the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "drop-down"))
        )

        # Select the 'Upload from URL' radio button
        url_radio_button = driver.find_element(By.CSS_SELECTOR, 'input[value="urlUpload"]')
        url_radio_button.click()
        
        # Wait for the URL input field to be present
        url_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"]')))

        # Enter the URL into the input field
        url_input.clear()
        url_input.send_keys(url)

        # Find the 'Upload' button
        upload_button = driver.find_element(By.XPATH, '//*[@id="drop-down"]/div/div/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[1]/div/div/div/div/div/button')
        # Click the 'Upload' button
        upload_button.click()

        print("Data loaded successfully.")
        print("The browser will remain open. Close it manually to end the session.")
        main_window_handle = driver.current_window_handle

        while True:
            if main_window_handle not in driver.window_handles:
                print("The tab was closed.")
                break
            time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Optionally handle any cleanup if needed
        driver.quit()  # Ensure the browser closes

if __name__ == "__main__":
    main()
