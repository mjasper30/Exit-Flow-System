import tkinter as tk
import win32print
import win32ui
import win32con  # Add this import

def print_text():
    text_to_print = "Hello, world!"  # Text you want to print
    printer_name = win32print.GetDefaultPrinter()  # Get the default printer

    # Create a printer device context (DC)
    printer_handle = win32print.OpenPrinter(printer_name)
    printer_dc = win32ui.CreateDC()
    printer_dc.CreatePrinterDC(printer_name)

    # Start a document
    printer_dc.StartDoc("Test Document")
    printer_dc.StartPage()

    # Set the text properties (font, size, etc.)
    printer_dc.SetMapMode(win32con.MM_TWIPS)
    printer_dc.SetTextAlign(win32con.TA_LEFT | win32con.TA_TOP)
    printer_dc.TextOut(20, 20, text_to_print)

    # End the document
    printer_dc.EndPage()
    printer_dc.EndDoc()

    # Close the printer
    printer_dc.DeleteDC()
    win32print.ClosePrinter(printer_handle)

# Create the main Tkinter window
root = tk.Tk()
root.title("Print Text")

# Create a button to print text
print_button = tk.Button(root, text="Print", command=print_text)
print_button.pack()

# Run the Tkinter event loop
root.mainloop()
