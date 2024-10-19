import sqlite3 as db
import qrcode
import random
import string
import cv2
import numpy as np
from pyzbar.pyzbar import decode

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
    image_file = id + ".png"
    img.save(image_file)
    return id, img

def add_entry(lname, fname, num, email):


    qr_code_info = create_qr_code()  # Call the function properly
    id = qr_code_info[0]

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



def display_database(): 
    
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

def reset_database():
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")
        print(f"Table '{table[0]}' has been dropped.")

    conn.commit()

    print("Database has been reset (all tables dropped).")


def in_database(barcode_data):

    query = "SELECT COUNT(*) FROM contacts WHERE id = ?"
    cursor.execute(query, (barcode_data,))

    # Fetch the result
    count = cursor.fetchone()[0]

    if count > 0:
        print(f'Barcode data "{barcode_data}" exists in the database.')
    else:
        print(f'Barcode data "{barcode_data}" does not exist in the database.')

def decoder(image):
    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img)

    for obj in barcode:
        points = obj.polygon
        (x,y,w,h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)
        
        cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
        in_database(barcodeData)
        

def main():
    add_entry("Schwarz", "Max", 2066024579, "max.schwarz9@gmail.com")
    add_entry("Bob", "Jones", 1111111111, "bobjones@gmail.com")
    display_database()



main()
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    decoder(frame)
    cv2.imshow('Image', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break



