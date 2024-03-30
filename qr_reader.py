import cv2
import time
from pyzbar.pyzbar import decode
import subprocess
import RPi.GPIO as GPIO
import sys

# GPIO pins for the ultrasonic sensor
TRIG = 23
ECHO = 24

# Set GPIO mode and pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Access the passed argument
data = sys.argv[1]

def distance():
    # Send a pulse to trigger the ultrasonic sensor
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    # Measure the time it takes for the echo to return
    pulse_start = time.time()
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    
    pulse_end = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    
    # Calculate distance in centimeters
    distance = pulse_duration * 17150
    return distance

def read_qr_code_from_camera():
    global data
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
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
                
                #print("Camera is now ready to scan objects")
                
                qr_decoded = True  # Set the flag to True to break out of the loop
                
                break
        
        if qr_decoded:
            break
            
        # Display the frame
        cv2.imshow("QR Code Scanner", frame)
        
        # Break the loop if 'q' is pressed again
        if cv2.waitKey(1) & 0xFF == ord('q'):
            qr_decoded = False
            break
        
    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()
    
    # Ultrasonic sensor
    while True:
        dist = distance()
        print("Distance:", dist, "cm")
            
        # If someone passes by (distance less than a threshold), break the loop
        if dist < 30:  # You can adjust this threshold according to your requirements
            print("Someone passed by!")
            break
            
        time.sleep(0.1)  # Small delay to reduce CPU usage
    
    # Call yolo_process function
    capture_camera()
    
    # Call yolo_process function
    yolo_process(data)

def capture_camera():
    subprocess.Popen(["python", "capture_camera.py"])

def yolo_process(data):
    subprocess.Popen(["python", "yolo_process.py", str(data)])

# Now you can use the data variable in your qr_reader.py script
print(data)  # Just an example usage

# Call the function to start reading QR codes from camera
read_qr_code_from_camera()
