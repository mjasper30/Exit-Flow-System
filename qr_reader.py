import cv2
from pyzbar.pyzbar import decode

def read_qr_code_from_camera():
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Decode QR code
        decoded_objects = decode(gray_frame)
        
        # Print results
        for obj in decoded_objects:
            print("Data:", obj.data.decode("utf-8"))
            print("Type:", obj.type)
            print()
        
        # Display the frame
        cv2.imshow("QR Code Scanner", frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

# Call the function to start reading QR codes from camera
read_qr_code_from_camera()
