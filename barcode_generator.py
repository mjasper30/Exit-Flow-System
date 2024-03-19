from barcode import EAN13

data = '5901234123457'  # Replace with your own 12-digit EAN-13 data
my_code = EAN13(data)

my_code.save('barcode')  # Save the barcode image as 'ean13_barcode.png'
