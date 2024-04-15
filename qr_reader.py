import cv2
import time
from pyzbar.pyzbar import decode
import subprocess
import RPi.GPIO as GPIO
import os
from ultralytics import YOLO
import sys
from gpiozero import Buzzer
from time import sleep

# GPIO pins for the ultrasonic sensor
TRIG = 23
ECHO = 24
buzzer_pin = 25

# Set GPIO mode and pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(buzzer_pin, GPIO.OUT)

# Pin numbers for the LEDs
green_pin = 17
red_pin = 18
yellow_pin = 27

# Set up GPIO
GPIO.setwarnings(False)  # Disable warnings
GPIO.setmode(GPIO.BCM)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(yellow_pin, GPIO.OUT)

IMAGES_DIR = os.path.join('.', 'images')
OUTPUT_DIR = os.path.join('.', 'output')

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

model_path = os.path.join('.', 'models', 'best3.pt')

# Load a model
model = YOLO(model_path)  # load a custom model

threshold = 0.5
distance_threshold = 80 # ADJUST HERE DISTANCE THRESHOLD

# Define a dictionary mapping class IDs to background colors
background_colors = {
    0: (0, 0, 255),    
    1: (0, 255, 255),
}

def accept_sound():
    # Play accept sound with higher pitch
    buzzer = GPIO.PWM(buzzer_pin, 1000)  # 1000 Hz frequency
    buzzer.start(50)  # 50% duty cycle
    sleep(0.5)
    buzzer.stop()
    
def reject_sound():
    # Play reject sound with higher pitch
    buzzer = GPIO.PWM(buzzer_pin, 1500)  # 1500 Hz frequency
    buzzer.start(50)  # 50% duty cycle
    sleep(0.2)
    buzzer.stop()

def turn_on_led(pin):
    # Turn on LED
    for _ in range(3):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.5)

# Function to turn on green LED
def turn_on_green():
    turn_on_led(green_pin)

# Function to turn on red LED
def turn_on_red():
    turn_on_led(red_pin)
    
# Function to turn on red LED
def turn_on_yellow():
    turn_on_led(yellow_pin)
    
def process_image(image_path, output_path, qr_data):
    # Read the image
    frame = cv2.imread(image_path)
    H, W, _ = frame.shape

    results = model(frame)[0]

    plastic_bag_count = 0  # Initialize count of plastic bags
    box_count = 0
    paper_bag_count = 0
    eco_bag_count = 0

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            # Draw bounding box and label on the image
            background_color = background_colors.get(int(class_id), (255, 0, 0))
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), background_color, 2)
            class_label = results.names[int(class_id)].upper()
            text = f'{class_label} {score:.2f}'
            cv2.putText(frame, text, (int(x1), int(y1) - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            # Increment count based on class
            print(class_label)
            if class_label == 'PLASTIC-BAG':
                plastic_bag_count += 1
            elif class_label == 'BOX':
                box_count += 1
            elif class_label == 'PAPER-BAG':
                paper_bag_count += 1
            elif class_label == 'ECO-BAG':
                eco_bag_count += 1

    # Overlay counts on the top left side of the image
    cv2.putText(frame, f'Plastic Bags: {plastic_bag_count}', (20, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, f'Boxes: {box_count}', (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, f'Paper Bags: {paper_bag_count}', (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, f'Eco Bags: {eco_bag_count}', (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    
    print("-------------------YOLO PROCESS INFORMATION-------------------")
    print("Number of Plastic Bag Detected:", plastic_bag_count)
    print("Number of Box Detected:", box_count)
    print("Number of Paper Bag Detected:", paper_bag_count)
    print("Number of Eco Bag Detected:", eco_bag_count)
    print("---------------------------------------------------------------")

    # Save the processed image to the output folder
    cv2.imwrite(output_path, frame)

    if plastic_bag_count == int(qr_data_array[0]) and box_count == int(qr_data_array[1]) and paper_bag_count == int(qr_data_array[2]) and eco_bag_count == int(qr_data_array[3]):
        print("Accepted")
        accept_sound()
        turn_on_green()
    else:
        print("Rejected")
        #Turn on red led
        GPIO.output(red_pin, GPIO.HIGH)
        
        # Play reject sound 5 times
        for _ in range(5):
            GPIO.output(red_pin, GPIO.HIGH)
            reject_sound()
            GPIO.output(red_pin, GPIO.LOW)
            time.sleep(1)
        
        #Turn off red led

    data = ""
    
    #Turn on yellow led
    GPIO.output(yellow_pin, GPIO.LOW)

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
    # Initialize camera
    cap = cv2.VideoCapture(2)
    
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
                qr_decoded = True  # Set the flag to True to break out of the loop
                qr_data = obj.data.decode("utf-8")  # Store the decoded data
                
                # Split the data into an array based on a delimiter (assuming comma in this case)
                qr_data_array = qr_data.split(',')
                
                print("-------------------QR Receipt Data-------------------")
                print("Number of Plastic Bag:", qr_data_array[0])
                print("Number of Box:", qr_data_array[1])
                print("Number of Paper Bag:", qr_data_array[2])
                print("Number of Eco Bag:", qr_data_array[3])
                print("Timestamp:", qr_data_array[4])
                print("-----------------------------------------------------")
                accept_sound()
                
                # Return the decoded data array
                return qr_data_array

        # Close the camera window if QR code is decoded
        if qr_decoded:
            cv2.destroyAllWindows()
            break
            
        # Display the frame
        cv2.imshow("QR Code Scanner", frame)
        
        # Break the loop if 'q' is pressed again
        if cv2.waitKey(1) & 0xFF == ord('q'):
            qr_decoded = False
            break

    # Release the video capture object and close the camera
    cap.release()

def pass_in(qr_data):
    #Turn on yellow led
    GPIO.output(yellow_pin, GPIO.HIGH)
    
    # Ultrasonic sensor
    while True:
        dist = distance()
        print("Distance:", int(dist), "cm")
                
        # If someone passes by (distance less than a threshold), break the loop
        if dist < distance_threshold:  # You can adjust this threshold according to your requirements
            print("Someone passed by!")
            accept_sound()
            break # Comment this to adjust the distance threshold
                
        time.sleep(0.1)  # Small delay to reduce CPU usage

def capture_camera():
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)

    # reading the input using the camera
    result, image = cam.read()

    # If an image is detected without any error, show the result
    if result:

        # showing result, it takes frame name and image output
        cv2.imshow("Capture Image", image)
        print("Captured!")

        # saving the image in local storage
        cv2.imwrite("images/capture.png", image)
        print("Image is now save on folder!")

        # If a keyboard interrupt occurs, destroy the image window
        #waitKey(0)
        cv2.destroyWindow("Capture Image")
        # Release the video capture object and close the camera
        cam.release()

    # If the captured image is corrupted, move to the else part
    else:
        print("No image detected. Please try again")

def yolo_process(qr_data):
    # Iterate over images in the input directory
    for filename in os.listdir(IMAGES_DIR):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(IMAGES_DIR, filename)
            output_path = os.path.join(OUTPUT_DIR, filename)
            process_image(image_path, output_path, qr_data)
            print(f"Processed {filename} and saved to {output_path}")

while True:
    qr_data_array = read_qr_code_from_camera()
    pass_in(qr_data_array)
    capture_camera()
    yolo_process(qr_data_array)
    
    # Break the loop if 'q' is pressed again
    if cv2.waitKey(1) & 0xFF == ord('q'):
        GPIO.cleanup()
        break
