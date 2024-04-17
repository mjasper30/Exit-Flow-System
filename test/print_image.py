import os
import win32print
import win32ui
import win32api
import win32con
from PIL import Image, ImageWin
from fpdf import FPDF  # Import FPDF

# Specify the paper size in pixels (80mm width, 160mm height)
PAPER_WIDTH_MM = 80
PAPER_HEIGHT_MM = 160
PAPER_WIDTH_PIXELS = int(PAPER_WIDTH_MM / 25.4 * 300)  # Assuming 300 DPI
PAPER_HEIGHT_PIXELS = int(PAPER_HEIGHT_MM / 25.4 * 300)  # Assuming 300 DPI

printer_name = win32print.GetDefaultPrinter()
hDC = win32ui.CreateDC()
hDC.CreatePrinterDC(printer_name)
HORZRES = hDC.GetDeviceCaps(win32con.HORZRES)
VERTRES = hDC.GetDeviceCaps(win32con.VERTRES)
hDC.DeleteDC()

image_path = "qr_codes/qr_code.png"  # Specify the path to the image

if os.path.exists(image_path):  # Check if the image exists
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)
    
    # Adjust printable area to fit the custom paper size
    printable_area = PAPER_WIDTH_PIXELS, PAPER_HEIGHT_PIXELS
    
    bmp = Image.open(image_path)
    
    # Resize image to fit the paper size
    width_ratio = PAPER_WIDTH_PIXELS / bmp.width
    height_ratio = PAPER_HEIGHT_PIXELS / bmp.height
    resize_ratio = min(width_ratio, height_ratio)
    new_width = int(bmp.width * resize_ratio)
    new_height = int(bmp.height * resize_ratio)
    resized_image = bmp.resize((new_width, new_height))
    
    hDC.StartDoc(os.path.basename(image_path))
    hDC.StartPage()
    dib = ImageWin.Dib(resized_image)
    dib.draw(hDC.GetHandleOutput(), (0, 0, new_width, new_height))
    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()
else:
    print("Image file not found: qr_codes/qr_code.png")

# Creating PDF with custom paper size
pdf = FPDF(orientation='P', unit='mm', format=(PAPER_WIDTH_MM, PAPER_HEIGHT_MM))
pdf.add_page()
pdf.output("output.pdf")
