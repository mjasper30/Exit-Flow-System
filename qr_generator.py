import tkinter as tk
import qrcode
from PIL import ImageTk, Image
import time
import subprocess  # Required for opening another Python script
import mysql.connector

# Establish a connection to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="thesis",
    password="thesis",
    database="qr_codes"
)

data = ""

def generate_qr():
    global data
    
    # Get the current timestamp to make the data unique
    timestamp = int(time.time())
    
    data = f"{plastic_bag.get()}, {box.get()}, {paper_bag.get()}, {timestamp}"
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"qr_codes/qr_code_{timestamp}.png")  # Save the QR code with a unique filename
    img = img.resize((300, 300), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    qr_label.config(image=img)
    qr_label.image = img

    # Insert data into MySQL database
    cursor = mydb.cursor()
    sql = "INSERT INTO qr_codes (plastic_bag, box, paper_bag, timestamp, qr_code_path) VALUES (%s, %s, %s, %s, %s)"
    values = (plastic_bag.get(), box.get(), paper_bag.get(), timestamp, f"qr_codes/qr_code_{timestamp}.png")
    cursor.execute(sql, values)
    mydb.commit()

    cursor.close()

def open_qr_reader(data):
    subprocess.Popen(["python", "qr_reader.py", str(data)]) # Open the QR reader script in a new process

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

# Button to generate QR code
generate_button = tk.Button(root, text="Generate", command=generate_qr)
generate_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Button to open QR reader window
qr_reader_button = tk.Button(root, text="QR Reader", command=lambda: open_qr_reader(data))
qr_reader_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Label to display QR code
qr_label = tk.Label(root)
qr_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
