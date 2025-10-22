# Python Utilities: Image Converter & Email Sender

This repository contains two useful Python scripts:

1.  **Image Converter:** A graphical tool built with Tkinter for converting images between formats (JPG, PNG, SVG, WebP).
2.  **Email Sender:** A script to send personalized emails in bulk using a Gmail account, reading recipient data from a CSV file.

---

## 1. Image Converter

### Features
* Simple graphical user interface (GUI) built with Tkinter.
* Supports input formats: `.jpg`, `.jpeg`, `.png`, `.svg`, `.webp`.
* Supports output formats: `.jpg`, `.png`, `.webp`.
* Allows selecting multiple files for batch conversion.
* Option to set the output quality for JPEG and WebP formats.
* Includes basic support for converting SVG files (requires `cairosvg`).
* Displays conversion progress.
* Allows choosing a custom output directory.

### Requirements
* Python 3.x
* Pillow library (`pip install Pillow`)
* (Optional) CairoSVG for SVG support (`pip install CairoSVG`)

### Usage
1.  Ensure Python 3 and Pillow are installed. Install CairoSVG if you need SVG support.
2.  Run the script (e.g., `python image_converter_script_name.py`).
3.  Use the "Select Files" button to choose the images you want to convert.
4.  Choose the desired output format (JPEG, PNG, WebP).
5.  (Optional) Adjust the quality slider if converting to JPEG or WebP.
6.  (Optional) Change the output directory using the "Browse" button.
7.  Click "CONVERT" to start the process.

---

## 2. Bulk Email Sender

### Features
* Sends personalized emails using a Gmail account.
* Reads recipient data (name, email address) from a CSV file.
* Supports sending emails in HTML format.
* Allows embedding images within the email body.
* Includes options to control the sending rate (batch size, delay) to avoid spam filters.
* Basic error handling and logging for failed sends.

### Setup
1.  **Enable Less Secure App Access / App Passwords:** For Gmail, you'll need to enable 2-Step Verification for your account and then generate an "App Password". Google has increased security measures, so using your regular password directly might not work and is less secure.
    * Go to your Google Account settings.
    * Navigate to "Security".
    * Under "Signing in to Google", enable 2-Step Verification if not already enabled.
    * Then, find the "App passwords" option (you might need to search within your account settings).
    * Generate a new app password for "Mail" on "Other (Custom name)" (e.g., "PythonMailer").
    * Copy the generated 16-character password. This will be used in the script.
2.  **Edit the Script:** Open the `send_emails.py` (or your script name) file and update the following variables:
    * `EMAIL`: Set this to your Gmail address (e.g., `your_email@gmail.com`).
    * `PASSWORD`: Set this to the 16-character App Password you generated.
    * `SUBJECT`: Customize the subject line of your email.
    * `MESSAGE_HTML`: Modify the HTML content of your email. Use `{name}` as a placeholder for the recipient's name.
    * `MESSAGE_TEXT`: Provide a plain text version of your email content (optional but recommended).
    * `CSV_FILE`: Ensure this matches the name of your CSV file (e.g., `recipients.csv`).
    * `image_path` (optional): If you want to embed an image, set this to the path of the image file (e.g., `'logo.png'`). Make sure the `<img>` tag in your `MESSAGE_HTML` uses `src="cid:image1"`.

### CSV File Format
Your CSV file (e.g., `recipients.csv`) should have at least two columns with headers: `name` and `email`.

```csv
name,email
Alice,alice@example.com
Bob,bob@example.com
Charlie,charlie@example.com
