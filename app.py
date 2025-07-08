```python
import gradio as gr
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
import io
import base64

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=True)

def detect_feet(input_image):
    # Convert base64 to image
    if isinstance(input_image, str) and input_image.startswith('data:image'):
        input_image = input_image.split(',')[1]
        img_data = base64.b64decode(input_image)
        img = Image.open(io.BytesIO(img_data))
        img = np.array(img)
    else:
        img = np.array(input_image)

    # Convert to RGB for MediaPipe
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb)
    feet_y = None

    # Process landmarks
    if result.pose_landmarks:
        h, w, _ = img.shape
        feet_landmarks = []
        for id, lm in enumerate(result.pose_landmarks.landmark):
            if id in [27, 28, 31, 32]:  # Heels and toes keypoints
                if lm.visibility > 0.5:  # Only use high-confidence keypoints
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
                    feet_landmarks.append(lm.y)
        if feet_landmarks:
            feet_y = sum(feet_landmarks) / len(feet_landmarks)  # Average normalized Y (0-1)

    # Convert image back to base64
    _, buffer = cv2.imencode('.png', img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    img_base64 = f'data:image/png;base64,{img_base64}'

    return [img_base64, feet_y or 0.9]  # Default to bottom if no feet detected

iface = gr.Interface(
    fn=detect_feet,
    inputs=gr.Image(type="numpy", label="Input Image"),
    outputs=[
        gr.Image(type="numpy", label="Image with Feet Marked"),
        gr.Number(label="Feet Y-Coordinate")
    ],
    title="Deepsite Feet Detection",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
