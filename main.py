from playwright.sync_api import sync_playwright, Locator  
import pytesseract  
from PIL import Image  
from typing import List, Dict  
from jinja2 import Template  
from utils.data import html_template  

class LocatorIterator:
    """  
    A class responsible for extracting text content from Playwright locators.
    """
    @staticmethod
    def extract_text(locator: Locator) -> List[str]:
        """
        Extracts text content from a given locator.

        Args:
            locator (Locator): Playwright locator object.

        Returns:
            List[str]: A list of cleaned text content from the locator.
        """
        texts = []
        for index in range(locator.count()):
            raw_text = locator.nth(index).text_content()
            cleaned_text = raw_text.replace("\n", "").replace("\t", "")
            texts.append(cleaned_text)
        return texts

class ImageProcessor:
    """
    A class responsible for processing images and extracting text.
    """
    def __init__(self, tesseract_cmd: str):
        """
        Initialize the ImageProcessor with the Tesseract command path.

        Args:
            tesseract_cmd (str): Path to the Tesseract executable.
        """
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def extract_text_from_image(self, image_path: str) -> int:
        """
        Extract and evaluate a mathematical equation from an image.

        Args:
            image_path (str): Path to the image file.

        Returns:
            int: The result of the evaluated equation extracted from the image.
        """
        img = Image.open(image_path)
        result = pytesseract.image_to_string(img)
        equation = result.translate({ord(c): None for c in "?="})
        return eval(equation)

class PNRStatusChecker:
    """
    A class for checking PNR status using Playwright.
    """
    def __init__(self, tesseract_cmd: str):
        """
        Initialize the PNRStatusChecker with the Tesseract command path.

        Args:
            tesseract_cmd (str): Path to the Tesseract executable.
        """
        self.image_processor = ImageProcessor(tesseract_cmd)

    def fetch_pnr_status(self, pnr: str) -> Dict[str, str]:
        """
        Fetch the PNR status from the Indian Railways website.

        Args:
            pnr (str): The PNR number to check.

        Returns:
            Dict[str, str]: A dictionary containing the PNR status details.
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://www.indianrail.gov.in/enquiry/PNR/PnrEnquiry.html?locale=en")

            page.fill("#inputPnrNo", pnr)
            page.locator("#modal1").click()
            page.locator("#CaptchaImgID").screenshot(path="captcha.png")

            captcha_result = self.image_processor.extract_text_from_image("captcha.png")
            print("===  result  ===",captcha_result)
            page.fill("#inputCaptcha", str(captcha_result))
            page.locator("#submitPnrNo").click()

            journey_titles_locator = page.locator("#journeyDetailsTable >> thead >> tr >> th")
            passenger_titles_locator = page.locator("#psgnDetailsTable >> thead >> tr >> th")
            journey_records_locator = page.locator("#journeyDetailsTable >> tbody >> tr >> td")
            passenger_records_locator = page.locator("#psgnDetailsTable >> tbody >> tr >> td")

            # Ensure locators are resolved properly
            try:
                # Wait for the locators to be visible
                page.wait_for_selector("#journeyDetailsTable >> thead >> tr >> th", timeout=5000)
                page.wait_for_selector("#psgnDetailsTable >> thead >> tr >> th", timeout=5000)
                page.wait_for_selector("#journeyDetailsTable >> tbody >> tr >> td", timeout=5000)
                page.wait_for_selector("#psgnDetailsTable >> tbody >> tr >> td", timeout=5000)

                # Extract text from the resolved locators
                journey_titles = LocatorIterator.extract_text(journey_titles_locator)
                passenger_titles = LocatorIterator.extract_text(passenger_titles_locator)
                journey_records = LocatorIterator.extract_text(journey_records_locator)
                passenger_records = LocatorIterator.extract_text(passenger_records_locator)

                # Debugging output
                print("Journey Titles:", journey_titles)
                print("Passenger Titles:", passenger_titles)
                print("Journey Records:", journey_records)
                print("Passenger Records:", passenger_records)

                # Combine the titles and records as per original logic
                titles = journey_titles + passenger_titles
                records = journey_records + passenger_records

                # Safely create a dictionary to store the results
                data = {titles[i]: records[i] for i in range(min(len(titles), len(records)))}

                print("Final Data:", data)
            except Exception as e:
                print(f"Error while processing locators: {e}")

            browser.close()
            return data



def generate_html_report(data):

    # Create a Jinja template object  
    template = Template(html_template)  

    # Render the template with the data  
    rendered_html = template.render(  
        train_number=data[' Train Number'],  
        train_name=data['Train Name'],  
        boarding_date=data['Boarding Date (DD-MM-YYYY)'],  
        from_=data['From'],  
        to=data['To'],  
        reserved_upto=data['Reserved Upto'],  
        boarding_point=data['Boarding Point'],  
        class_=data['Class'],  
        s_no=data['S. No.'],  
        booking_status=data['Booking Status (Coach No , Berth No., Quota)'],  
        current_status=data['*Current Status (Coach No , Berth No.)'],  
        coach_position=data['Coach Position']  
    )  

    # Save the rendered HTML to a file  
    with open('train_details.html', 'w') as f:  
        f.write(rendered_html)  

    print("HTML file generated: train_details.html")  


if __name__ == "__main__":  
    pnr = input("Enter PNR: ")





    checker = PNRStatusChecker("/opt/homebrew/bin/tesseract")  # Update path as per your OS  
    details = checker.fetch_pnr_status(pnr)  
    generate_html_report(details)
