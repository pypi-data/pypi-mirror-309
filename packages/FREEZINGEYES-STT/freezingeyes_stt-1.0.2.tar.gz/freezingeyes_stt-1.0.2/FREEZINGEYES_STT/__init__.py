from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from os import getcwd


# Setting Up the Browser with options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--use-fake-ui-for-media-stream')
chrome_options.add_argument('--headless=new')  # Run in headless mode

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Telling chrome to open html
website = "https://allorizenproject1.netlify.app"
driver.get(website)

# File to save recognized text
rec_file = f"{getcwd()}\\input.txt"

def listen():
    try:
        # Wait for the start button to be clickable and click it
        start_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "startButton")))
        start_button.click()
        print("Listening...")

        output_text = ""
        is_second_click = False

        # Keep listening while button state indicates it's listening
        while True:
            # waiting for 'output' element
            output_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'output')))
            current_text = output_element.text.strip()  # Clean the text output

            # Checking conditions for button state and output
            if "Start Listening" in start_button.text and is_second_click:
                if output_text:
                    is_second_click = False  # Exit the loop if listening is complete
            elif "listening..." in start_button.text:
                is_second_click = True

            # Update only if there's new text
            if current_text and current_text != output_text:
                output_text = current_text
                with open(rec_file, "w") as file:
                    file.write(output_text.lower())
                    print("USER : " + output_text)

    except KeyboardInterrupt:
        print("Process interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()  # Close the browser when finished
