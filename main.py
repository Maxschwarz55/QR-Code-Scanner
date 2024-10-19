import sqlite3 as db
import qrcode
import random
import string

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choices(characters, k=length))
    return random_string


def create_qr_code():
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4
    )

    # Add data to the QR code
    id = generate_random_string(10)
    qr.add_data(id)

    # Compile the QR code data
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image
    img.save('custom_qr.png')

def init_database():
    conn = db.connect("test.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE contacts (lname text, fname text, num int, email text, id text)")
    cursor.execute("INSERT INTO contacts VALUES('Schwarz', 'Max' )")

def main():
    create_qr_code()

main()