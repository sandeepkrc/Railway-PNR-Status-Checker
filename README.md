# PNR Status Checker

A Python-based project to fetch and analyze PNR status from the Indian Railways website. This project leverages Playwright for browser automation, Tesseract-OCR for captcha recognition, and Jinja2 for generating HTML reports.

## Features

- Fetch PNR details from the Indian Railways PNR Enquiry page.
- Automate captcha solving using Tesseract-OCR.
- Generate an HTML report with PNR details using a Jinja2 template.
- Modular and extensible codebase.

---

## Prerequisites

- Python 3.8 or later
- [Node.js](https://nodejs.org/) (required for Playwright)
- Tesseract-OCR installed (update the path in `main.py` accordingly)
- Install required Python packages with `pip install -r requirements.txt`.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/PNRStatusChecker.git
   cd PNRStatusChecker
2. Install dependencies:

   pip install -r requirements.txt

3. Install Playwright dependencies:

   playwright install


## Usage
Run the script:

   python main.py

   Enter the PNR number when prompted.

   Check the generated HTML report (train_details.html) for the PNR status.

#  example output

   Journey Titles: ['Train Number', 'Train Name', ...]
   Passenger Titles: ['S. No.', 'Booking Status', ...]
   Journey Records: [...]
   Passenger Records: [...]
   Final Data: {...}
