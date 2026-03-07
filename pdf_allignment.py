import os
from PIL import Image

image_folder = "dashboard_screenshots"
output_pdf = "aligned_images.pdf"

images = []

# Fixed width for mobile friendly PDF
PDF_WIDTH = 1080
MARGIN = 40

image_files = sorted([
    f for f in os.listdir(image_folder)
    if f.lower().endswith((".png", ".jpg", ".jpeg"))
])

for file in image_files:
    path = os.path.join(image_folder, file)
    img = Image.open(path).convert("RGB")

    # Resize image to fixed width
    new_width = PDF_WIDTH - (2 * MARGIN)
    ratio = new_width / img.width
    new_height = int(img.height * ratio)

    img = img.resize((new_width, new_height), Image.LANCZOS)

    # Create page slightly larger than image
    page_height = new_height + (2 * MARGIN)
    page = Image.new("RGB", (PDF_WIDTH, page_height), "white")

    # Center image
    x = (PDF_WIDTH - new_width) // 2
    y = MARGIN

    page.paste(img, (x, y))
    images.append(page)

# Save as PDF
if images:
    images[0].save(output_pdf, save_all=True, append_images=images[1:])

print("PDF created:", output_pdf)

import requests
import os

def send_email():

    url = "http://127.0.0.1:8000/send-email"

    payload = {
        "email": "neerajwings1@gmail.com",
        "subject": "Graphs PDF",
        "message": "sales descriptive pdf",
        "cc": "premkumaravula77@gmail.com"
    }

    pdf_path = "dashboard_report.pdf"

    # Check if file exists
    if not os.path.exists(pdf_path):
        print("Error: PDF file not found.")
        return

    try:
        with open(pdf_path, "rb") as f:
            files = {
                "attachment": ("aligned_images.pdf", f, "application/pdf")
            }

            response = requests.post(url, data=payload, files=files)

        print("Status:", response.status_code)
        print("Response:", response.text)

    except Exception as e:
        print("Error sending email:", str(e))


send_email()