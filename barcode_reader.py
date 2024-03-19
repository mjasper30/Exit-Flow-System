import cv2
from pyzbar import pyzbar

# Function to decode barcodes
def decode_barcodes(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Use ZBar to detect and decode barcodes
    barcodes = pyzbar.decode(gray)
    
    # Loop over detected barcodes
    for barcode in barcodes:
        # Extract barcode data and type
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type
        
        # Draw a bounding box around the barcode
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Display barcode data and type
        text = "{} ({})".format(barcode_data, barcode_type)
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
        
        # Print barcode data and type to console
        print("Found {} barcode: {}".format(barcode_type, barcode_data))

    return frame

# Initialize camera or webcam
cap = cv2.VideoCapture(0)

while True:
    # Read frame from camera
    ret, frame = cap.read()
    
    # Check if frame is successfully captured
    if not ret:
        break
    
    # Decode barcodes in the frame
    frame = decode_barcodes(frame)
    
    # Display the frame
    cv2.imshow('Barcode Scanner', frame)
    
    # Check for 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
