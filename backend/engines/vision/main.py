from pathlib import Path

import cv2
import mediapipe as mp


BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
# GestureRecognizer = mp.tasks.vision.GestureRecognizer
# GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
DrawingUtils = mp.tasks.vision.drawing_utils
DrawingStyles = mp.tasks.vision.drawing_styles
HandLandmarksConnections = mp.tasks.vision.HandLandmarksConnections

# Create hand landmarker
BASE_DIR = Path(__file__).resolve().parent
hand_landmarker_path = str(BASE_DIR / 'model_assets' / 'hand_landmarker.task')
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=hand_landmarker_path),
    running_mode=VisionRunningMode.VIDEO
)

# options = GestureRecognizerOptions(
#     # base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
#     base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
#     running_mode=VisionRunningMode.VIDEO
# )

def run_vision(frame_queue):
    cap = cv2.VideoCapture(0)

    with HandLandmarker.create_from_options(options) as landmarker:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)

            if not frame_queue.full():
                _, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                frame_queue.put(frame_bytes)

            # MediaPipe Image expects RGB for SRGB format.
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

            result = landmarker.detect_for_video(mp_image, int(cap.get(cv2.CAP_PROP_POS_MSEC)))

            # Draw landmarks on the BGR frame we display.
            if result.hand_landmarks:
                for hand_landmarks in result.hand_landmarks:
                    DrawingUtils.draw_landmarks(
                        frame,
                        hand_landmarks,
                        HandLandmarksConnections.HAND_CONNECTIONS,
                        DrawingStyles.get_default_hand_landmarks_style(),
                        DrawingStyles.get_default_hand_connections_style(),
                    )

            cv2.imshow('Hand Tracking', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
