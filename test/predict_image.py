import os
from ultralytics import YOLO
import cv2

IMAGES_DIR = os.path.join('.', 'images')
OUTPUT_DIR = os.path.join('.', 'output')

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

model_path = os.path.join('.', 'models', 'best1.pt')

# Load a model
model = YOLO(model_path)  # load a custom model

threshold = 0.5

# Define a dictionary mapping class IDs to background colors
background_colors = {
    0: (0, 0, 255),    
    1: (0, 255, 255),
}

# Function to process an image
def process_image(image_path, output_path):
    # Read the image
    frame = cv2.imread(image_path)
    H, W, _ = frame.shape

    results = model(frame)[0]

    plastic_bag_count = 0  # Initialize count of plastic bottles

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            plastic_bag_count += 1  # Increment count for plastic bags

            # Draw bounding box and label on the image
            background_color = background_colors.get(int(class_id), (255, 0, 0))
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), background_color, 10)
            class_label = results.names[int(class_id)].upper()
            text = f'{class_label} {score:.2f}'
            cv2.putText(frame, text, (int(x1), int(y1) - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 5, cv2.LINE_AA)

    # Overlay plastic bottle count on the top left side of the image
    cv2.putText(frame, f'Number of Plastic Bag: {plastic_bag_count}', (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 5, cv2.LINE_AA)

    # Save the processed image to the output folder
    cv2.imwrite(output_path, frame)

# Iterate over images in the input directory
for filename in os.listdir(IMAGES_DIR):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(IMAGES_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename)
        process_image(image_path, output_path)
        print(f"Processed {filename} and saved to {output_path}")
