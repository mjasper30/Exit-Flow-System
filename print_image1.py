from fpdf import FPDF
from datetime import datetime
import calendar
import subprocess

# Sample data (replace with actual fetched data)
no_data = {
    "plastic-bag": "1",
    "box": "2",
    "eco-bag": "3",
    "paper-bag": "4",
}

# Get the current date and time
now = datetime.now()
date_generated = now.strftime("%B %d, %Y")  # Format date in word format
time_generated = now.strftime("%I:%M %p")   # Format time

# Create instance of FPDF class
pdf = FPDF(orientation='P', unit='mm', format=(80, 40))  # Specify custom paper format here

# Add a page
pdf.add_page()

# Example with local image
pdf.image("qr_codes/qr_code.png", x=20, y=0, w=40, h=40) # Add image (x, y, width, height

# Save the pdf with name .pdf
pdf_file_name = "receipt.pdf"
pdf.output(pdf_file_name)

# Open the PDF file
subprocess.Popen([pdf_file_name], shell=True)

# Print the PDF file
subprocess.Popen(['cmd', '/c', 'print', pdf_file_name], shell=True)