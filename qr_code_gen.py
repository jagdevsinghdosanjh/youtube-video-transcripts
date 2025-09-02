import qrcode

upi_id = "8146553307@yescred"
upi_url = f"upi://pay?pa={upi_id}&pn=Jagdev%20Singh%20Dosanjh&am=50&cu=INR"

qr = qrcode.make(upi_url)
qr.save("upi_qr.png")
