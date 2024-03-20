import qrcode

qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=5
)

data = "plastic-bag=1, box=0, paper-bag=0"
qr.add_data(data)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("qr.png")