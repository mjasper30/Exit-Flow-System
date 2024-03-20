import os
from ultralytics import YOLO
import cv2

# No need to specify the path for live camera

cap = cv2.VideoCapture(0)  # Use the default camera (device index 0)
ret, frame = cap.read()
H, W, _ = frame.shape

# Path for output video
video_path_out = 'videos/live_output.mp4'

# Define the model path
model_path = os.path.join('.', 'models', 'best1.pt')

# Load a model
model = YOLO(model_path)  # Load a custom model

threshold = 0.5

# Set the y-coordinate for the horizontal line
line_y = int(H * 0.7)
plastic_bags_crossed_line = set()

# Define a dictionary mapping class IDs to background colors
background_colors = {
    0: (0, 0, 255),    
    1: (0, 255, 255),
}

# Create a video writer
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(
    *'MP4V'), 30, (W, H))

while ret:
    results = model(frame)[0]
    for idx, result in enumerate(results.boxes.data.tolist()):
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            # Check if the center of the bounding box crosses the line
            center_y = (y1 + y2) / 2
            if center_y > line_y and int(class_id) not in plastic_bags_crossed_line:
                plastic_bags_crossed_line.add(int(idx+1))

            class_label = results.names[int(class_id)].upper()
            text = f'{class_label} {score:.2f}'  # Include idx+1 as ID

            # Get the size of the text
            (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)

            # Get the background color based on the class ID
            background_color = background_colors.get(int(class_id), (0, 0, 0))

            # Draw bounding box and label on the image
            color = (0, 0, 0)  # Black text color for bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), background_color, 2)

            # Draw a colored background for the text
            cv2.rectangle(frame, (int(x1), int(y1) - text_height - 20),
                          (int(x1) + text_width, int(y1)), background_color, cv2.FILLED)

            # Draw text on the colored background
            cv2.putText(frame, text, (int(x1), int(y1) - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)

    # Draw the plastic bag count on the side
    plastic_bag_count_text = f"Number of plastic bags: {len(plastic_bags_crossed_line)}"
    cv2.putText(frame, plastic_bag_count_text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    # Draw a horizontal line indicating the threshold line
    cv2.line(frame, (0, line_y), (frame.shape[1], line_y), (255, 0, 255), 2)

    # Write the frame to the output video
    out.write(frame)

    # Show the processed frame
    cv2.imshow('Frame', frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Read the next frame
    ret, frame = cap.read()

# Print the final plastic bag count on the console
print(f"Total Plastic Bags: {len(plastic_bags_crossed_line)}")

# Release video capture and writer
cap.release()
out.release()
cv2.destroyAllWindows()
