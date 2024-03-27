import cv2
import time
from pyzbar.pyzbar import decode
import mysql.connector

def read_qr_code_from_camera():
    # Initialize camera
    cap = cv2.VideoCapture(1)
    
    # Connect to MySQL database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="qr_codes"
    )
    
    # Create a cursor object to execute queries
    cursor = db_connection.cursor()
    
    # Flag to track if a QR code has been decoded in the current frame
    qr_decoded = False
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if not qr_decoded:
            # Decode QR code
            decoded_objects = decode(gray_frame)
            
            # Print results
            for obj in decoded_objects:
                print("Data:", obj.data.decode("utf-8"))
                print("Type:", obj.type)
                print()
                
                # Insert data into MySQL database
                query = "UPDATE status SET camera_status = 'on' WHERE id = 1"
                cursor.execute(query)
                db_connection.commit()
                print("Camera is now ready to scan objects")
                
                time.sleep(1)
        
        # Display the frame
        cv2.imshow("QR Code Scanner", frame)
        
        # Break the loop if 'q' is pressed again
        if cv2.waitKey(1) & 0xFF == ord('q'):
            qr_decoded = False
            break
    
    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()
    
    # Close database connection
    cursor.close()
    db_connection.close()

# Call the function to start reading QR codes from camera
read_qr_code_from_camera()
