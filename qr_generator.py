import tkinter as tk
import qrcode
from PIL import Image, ImageTk
import time
import subprocess  # Required for opening another Python script
import mysql.connector
from fpdf import FPDF  # Import FPDF library for PDF creation
import win32print
import win32ui
import win32con
from fpdf import FPDF
from datetime import datetime
import calendar
# Establish a connection to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="qr_codes"
)

data = ""
last_generated_qr_path = ""  # Track the path of the last generated QR code
timestamp = ""

# Get the current date and time
now = datetime.now()
date_generated = now.strftime("%B %d, %Y")  # Format date in word format
time_generated = now.strftime("%I:%M %p")   # Format ti

def generate_qr():
    global data, last_generated_qr_path, timestamp
    
    # Get the current timestamp to make the data unique
    timestamp = int(time.time())
    
    data = f"{plastic_bag.get()}, {box.get()}, {paper_bag.get()}, {eco_bag.get()}, {timestamp}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,  # This size may need adjustment
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Rescale the image to the desired size
    desired_size = (58 * 48, 3276)
    img = img.resize(desired_size, Image.LANCZOS)
    
    qr_path = f"qr_codes/qr_code_{timestamp}.png"
    img.save(qr_path)  # Save the QR code with a unique filename
    last_generated_qr_path = qr_path  # Update the last generated QR path
    img = img.resize((300, 300), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    qr_label.config(image=img)
    qr_label.image = img

    # Insert data into MySQL database
    cursor = mydb.cursor()
    sql = "INSERT INTO qr_codes (plastic_bag, box, paper_bag, eco_bag, timestamp, qr_code_path) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (plastic_bag.get(), box.get(), paper_bag.get(), eco_bag.get(), timestamp, qr_path)
    cursor.execute(sql, values)
    mydb.commit()

    cursor.close()

def print_receipt():
    global timestamp

    # Create instance of FPDF class
    pdf = FPDF(orientation='P', unit='mm', format=(80, 130))  # Specify custom paper format here

    # Add a page
    pdf.add_page()

    # Header
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, 'EXIT FLOW SYSTEM', ln=True, align='C')
    pdf.set_font("Arial", size=8)
    pdf.cell(0, 5, '524 P. Ramos St. Caloocan City', ln=True, align='C')
    pdf.cell(0, 5, '347-4567-2314', ln=True, align='C')
    pdf.cell(0, 5, 'exitflow@gmail.com', ln=True, align='C')
    pdf.ln(2)  # Add some space

    # Date and time generated
    pdf.set_font("Arial", size=6)
    pdf.cell(0, 5, 'Date: ' + date_generated, ln=True, align='L')
    pdf.cell(0, 5, 'Time: ' + time_generated, ln=True, align='L')

    # Exit Details
    pdf.set_font("Arial", size=10, style='B')
    pdf.cell(0, 10, 'Exit Details', ln=True, align='C')
    pdf.set_font("Arial", size=8)
    pdf.cell(0, 5, 'Number of Plastic Bag: ' + plastic_bag.get(), ln=True)
    pdf.cell(0, 5, 'Number of Box: ' + box.get(), ln=True)
    pdf.cell(0, 5, 'Number of Paper Bag: ' + paper_bag.get(), ln=True) 
    pdf.cell(0, 5, 'Number of Eco Bag: ' + eco_bag.get(), ln=True)

    # Example with local image
    pdf.image(f"qr_codes/qr_code_{timestamp}.png", x=20, y=78, w=40, h=40) # Add image (x, y, width, height

    # Save the pdf with name .pdf
    pdf_file_name = "receipt.pdf"
    pdf.output(pdf_file_name)

    # Open the PDF file
    subprocess.Popen([pdf_file_name], shell=True)

    # Print the PDF file
    subprocess.Popen(['cmd', '/c', 'print', pdf_file_name], shell=True)

# Create main window
root = tk.Tk()
root.title("QR Code Generator")

# Create entry widgets for input
plastic_bag_label = tk.Label(root, text="Number of plastic bags:")
plastic_bag_label.grid(row=0, column=0, padx=5, pady=5)
plastic_bag = tk.Entry(root)
plastic_bag.grid(row=0, column=1, padx=5, pady=5)

box_label = tk.Label(root, text="Number of boxes:")
box_label.grid(row=1, column=0, padx=5, pady=5)
box = tk.Entry(root)
box.grid(row=1, column=1, padx=5, pady=5)

paper_bag_label = tk.Label(root, text="Number of paper bags:")
paper_bag_label.grid(row=2, column=0, padx=5, pady=5)
paper_bag = tk.Entry(root)
paper_bag.grid(row=2, column=1, padx=5, pady=5)

eco_bag_label = tk.Label(root, text="Number of eco bags:")
eco_bag_label.grid(row=3, column=0, padx=5, pady=5)
eco_bag = tk.Entry(root)
eco_bag.grid(row=3, column=1, padx=5, pady=5)

# Button to generate QR code
generate_button = tk.Button(root, text="Generate", command=generate_qr)
generate_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Button to print last generated text
print_text_button = tk.Button(root, text="Print", command=print_receipt)
print_text_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Label to display QR code
qr_label = tk.Label(root)
qr_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
