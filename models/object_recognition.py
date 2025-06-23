from pathlib import Path

import cv2
import pygame
from gtts import gTTS


def speech(text):
    print(text)
    language = 'en'

    # Set path relative to the repo root
    output_dir = Path(__file__).parent / "assets" / "sounds"
    output_dir.mkdir(parents=True, exist_ok=True)  # Create if not exists

    output_path = output_dir / "output.mp3"

    # Generate and save audio
    output = gTTS(text=text, lang=language, slow=False)
    output.save(str(output_path))

    pygame.mixer.init()
    pygame.mixer.music.load(output_path)
    pygame.mixer.music.play()

    # Wait for it to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()

def draw_bbox(image, boxes, labels, confidences, colors=None):
    """
    Draw bounding boxes on image
    """
    if colors is None:
        colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

    for i, (box, label, conf) in enumerate(zip(boxes, labels, confidences)):
        x1, y1, x2, y2 = map(int, box)
        color = colors[i % len(colors)]

        # Draw bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

        # Draw label and confidence
        label_text = f"{label}: {conf:.2f}"
        label_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
        cv2.rectangle(image, (x1, y1 - label_size[1] - 10), (x1 + label_size[0], y1), color, -1)
        cv2.putText(image, label_text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    return image


def recognize_objects(frame, yolo_model, detected_labels):
    """
    Main function to recognize faces and detect objects in real-time
    """

    detected_objects = []
    results = yolo_model(frame, verbose=False)

    yolo_boxes = []
    yolo_labels = []
    yolo_confidences = []

    for r in results:
        if r.boxes is not None:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                yolo_boxes.append([x1, y1, x2, y2])

                conf = box.conf[0].cpu().numpy()
                yolo_confidences.append(conf)

                cls_id = int(box.cls[0].cpu().numpy())
                class_name = yolo_model.names[cls_id]
                yolo_labels.append(class_name)

                # Add to detected objects (exclude person class since we handle faces separately)
                if class_name not in detected_objects:
                    detected_objects.append(class_name)

    frame = draw_bbox(frame, yolo_boxes, yolo_labels, yolo_confidences)

    return frame, yolo_labels