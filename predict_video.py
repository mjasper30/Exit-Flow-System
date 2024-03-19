import os
from ultralytics import YOLO
import cv2

VIDEOS_DIR = os.path.join('.', 'videos')

video_path = os.path.join(VIDEOS_DIR, 'test.mp4')
video_path_out = 'videos/test-output.mp4'

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
H, W, _ = frame.shape
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(
    *'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

model_path = os.path.join('.', 'models', 'best.pt')

# Load a model
model = YOLO(model_path)  # load a custom model

threshold = 0.5

# Set the y-coordinate for the horizontal line
line_y = int(H * 0.7)
plastic_bag_count = 0
objects_crossed_line = set()

# Define a dictionary mapping class IDs to background colors
background_colors = {
    0: (0, 0, 255),    
    1: (0, 255, 255),
}

while ret:
    results = model(frame)[0]
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            # Check if the center of the bounding box crosses the line
            center_y = (y1 + y2) / 2
            if center_y > line_y and int(class_id) not in objects_crossed_line:
                objects_crossed_line.add(int(class_id))
                plastic_bag_count += 1

            class_label = results.names[int(class_id)].upper()
            text = f'{class_label} {score:.2f}'

            # Get the size of the text
            (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 2, 5)

            # Get the background color based on the class ID
            background_color = background_colors.get(int(class_id), (0, 0, 0))

            # Draw bounding box and label on the image
            color = (0, 0, 0)  # Black text color for bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), background_color, 10)

            # Draw a colored background for the text
            cv2.rectangle(frame, (int(x1), int(y1) - text_height - 20),
                        (int(x1) + text_width, int(y1)), background_color, cv2.FILLED)

            # Draw text on the colored background
            cv2.putText(frame, text, (int(x1), int(y1) - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, color, 5, cv2.LINE_AA)

    # Draw the car count on the side
    plastic_bag_count_text = f"Number of plastic bag: {plastic_bag_count}"
    cv2.putText(frame, plastic_bag_count_text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5, cv2.LINE_AA)

    # Draw the car count on the side
    cartonbox_count_text = f"Number of carton box: 0"
    cv2.putText(frame, cartonbox_count_text, (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5, cv2.LINE_AA)

    # Draw a horizontal line indicating the number of cars passing by
    line_y_coordinate = 1000  # Adjust the y-coordinate as needed
    cv2.line(frame, (0, line_y_coordinate), (frame.shape[1], line_y_coordinate), (255, 0, 255), 10)

    # Write the frame to the output video
    out.write(frame)

    # Read the next frame
    ret, frame = cap.read()

# Print the final car count on the console
print(f"Total Plastic Bag: {plastic_bag_count}")

# Release video capture and writer
cap.release()
out.release()
cv2.destroyAllWindows()
