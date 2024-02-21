import os
from ultralytics import YOLO
import cv2

IMAGES_DIR = os.path.join('.', 'images')
OUTPUT_IMAGES_DIR = os.path.join('.', 'output_images')

# Create the output_images directory if it doesn't exist
os.makedirs(OUTPUT_IMAGES_DIR, exist_ok=True)

image_path = os.path.join(IMAGES_DIR, 'first_frame.jpg')  # Replace 'your_image.jpg' with the actual image file
output_image_path = os.path.join(OUTPUT_IMAGES_DIR, 'output_image.jpg')

# Load a model
model_path = os.path.join('.', 'models', 'yolov8x.pt')
model = YOLO(model_path)  # load a custom model

# Read the input image
image = cv2.imread(image_path)

# Perform object detection on the image
results = model(image)[0]

# Set a threshold for detections
threshold = 0.5

# Define a dictionary mapping class IDs to background colors
background_colors = {
    2: (0, 0, 255),    
    3: (0, 255, 255),
    5: (0, 0, 255),
    7: (0, 255, 255),
}

car_count = 0  # Initialize car count

# Process the detected objects
for result in results.boxes.data.tolist():
    x1, y1, x2, y2, score, class_id = result

    if score > threshold:
        # Check if the detected object is a car (assuming class ID 0 represents cars)
        if int(class_id) == 0:
            car_count += 1  # Increment car count

        class_label = results.names[int(class_id)].upper()
        text = f'{class_label} {score:.2f}'

        # Get the size of the text
        (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 2, 5)

        # Get the background color based on the class ID
        background_color = background_colors.get(int(class_id), (0, 0, 0))

        # Draw bounding box and label on the image
        color = (0, 0, 0)  # Black text color for bounding box
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), background_color, 10)

        # Draw a colored background for the text
        cv2.rectangle(image, (int(x1), int(y1) - text_height - 20),
                      (int(x1) + text_width, int(y1)), background_color, cv2.FILLED)

        # Draw text on the colored background
        cv2.putText(image, text, (int(x1), int(y1) - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, color, 5, cv2.LINE_AA)

# Draw the car count on the side
car_count_text = f"Number of plastic bag: {car_count}"
cv2.putText(image, car_count_text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5, cv2.LINE_AA)

# Draw the car count on the side
cartonbox_count_text = f"Number of carton box: {car_count}"
cv2.putText(image, cartonbox_count_text, (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5, cv2.LINE_AA)

# Draw a horizontal line indicating the number of cars passing by
line_y_coordinate = 1000  # Adjust the y-coordinate as needed
cv2.line(image, (0, line_y_coordinate), (image.shape[1], line_y_coordinate), (255, 0, 255), 10)

# Save the output image
cv2.imwrite(output_image_path, image)

print(f"Number of cars passing by: {car_count}")
print(f"Output image saved at: {output_image_path}")
