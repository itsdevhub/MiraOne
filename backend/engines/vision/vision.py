import time

import cv2
import pyautogui
import mediapipe as mp

from .asset_factory import asset_factory
from .one_euro_filter import one_euro_filter
from .utils import landmark_distance


class vision:
    DEAD_ZONE = 5
    CLICK_THRESHOLD = 0.04

    def __init__(self, frame_queue):
        self.capture = cv2.VideoCapture(0)
        self.frame_queue = frame_queue
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.capture.release()
        cv2.destroyAllWindows()

    def run(self):    
        screen_w, screen_h = pyautogui.size()
        filter_x = one_euro_filter(min_cutoff=1.0, beta=0.01)
        filter_y = one_euro_filter(min_cutoff=1.0, beta=0.01)
        clicking = False

        hand_options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=str(asset_factory.hand_landmarker())),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=1
        )

        with mp.tasks.vision.HandLandmarker.create_from_options(hand_options) as landmarker:
            while self.capture.isOpened():
                ret, frame = self.capture.read()
                if not ret:
                    break

                frame = cv2.flip(frame, 1)

                if not self.frame_queue.full():
                    _, buffer = cv2.imencode('.jpg', frame)
                    frame_bytes = buffer.tobytes()
                    self.frame_queue.put(frame_bytes)

                # MediaPipe Image expects RGB for SRGB format.
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

                result = landmarker.detect_for_video(mp_image, int(self.capture.get(cv2.CAP_PROP_POS_MSEC)))

                # Draw landmarks on the BGR frame we display.
                if result.hand_landmarks:
                    for hand_landmarks in result.hand_landmarks:
                        mp.tasks.vision.drawing_utils.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS,
                            mp.tasks.vision.drawing_styles.get_default_hand_landmarks_style(),
                            mp.tasks.vision.drawing_styles.get_default_hand_connections_style(),
                        )
                    
                    hand = result.hand_landmarks[0]  # first hand only
                    index_tip = hand[8]
                    thumb_tip = hand[4]             
                    middle_tip = hand[12]

                    # convert to screen space
                    target_x = int(index_tip.x * screen_w)
                    target_y = int(index_tip.y * screen_h)

                    # --- ONE EURO FILTER ---
                    cur_time = time.time()
                    smooth_x = int(filter_x.filter(target_x, cur_time))
                    smooth_y = int(filter_y.filter(target_y, cur_time))

                    # --- DEAD ZONE (optional) ---
                    dx = smooth_x - pyautogui.position().x
                    dy = smooth_y - pyautogui.position().y

                    if abs(dx) > self.DEAD_ZONE or abs(dy) > self.DEAD_ZONE:
                        # index finger is up → move mouse
                        if index_tip.y < middle_tip.y:
                            pyautogui.moveTo(smooth_x, smooth_y)

                    # --- CLICKING ---
                    pinching = landmark_distance(thumb_tip, index_tip) < self.CLICK_THRESHOLD
                    index_up = index_tip.y < middle_tip.y

                    if pinching and index_up and not clicking:
                        pyautogui.click()

                    clicking = pinching

                cv2.imshow('Hand Tracking', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
