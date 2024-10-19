import sqlite3 as db
import qrcode
import random
import string

conn = db.connect("test.db")
cursor = conn.cursor()

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
    return id

def add_entry(lname, fname, num, email):

    id = create_qr_code()  # Call the function properly

    # Create the table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            lname TEXT, 
            fname TEXT, 
            num INTEGER, 
            email TEXT, 
            id TEXT
        )
    """)

    cursor.execute("INSERT INTO contacts (lname, fname, num, email, id) VALUES (?, ?, ?, ?, ?)",
                   (lname, fname, num, email, id))
    conn.commit()

    cursor.execute("SELECT * FROM contacts")

def display_database(): 
    
    rows = cursor.fetchall()

    for row in rows:
        print(row)

def main():
    add_entry()

main()