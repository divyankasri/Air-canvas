"""MediaPipe-based hand landmark tracking and gesture recognition."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import cv2
import mediapipe as mp
import numpy as np
from typing import Any

Point = Tuple[int, int]


@dataclass
class GestureResult:
    gesture: str
    cursor: Optional[Point]
    landmarks: Optional[Any]
    finger_states: Dict[str, bool]


class GestureDetector:
    """Encapsulates MediaPipe Hands and lightweight gesture heuristics."""

    def __init__(
        self,
        max_num_hands: int = 1,
        detection_confidence: float = 0.7,
        tracking_confidence: float = 0.5,
    ) -> None:
        self.mp_hands = mp.solutions.hands
        self._hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )
        self._drawing_utils = mp.solutions.drawing_utils
        self._drawing_styles = mp.solutions.drawing_styles

    def close(self) -> None:
        """Release MediaPipe resources."""
        self._hands.close()

    def process(self, frame: np.ndarray) -> GestureResult:
        """Run the MediaPipe graph and return gesture metadata."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self._hands.process(rgb)
        landmarks = result.multi_hand_landmarks[0] if result.multi_hand_landmarks else None
        h, w = frame.shape[:2]
        cursor = None
        finger_states: Dict[str, bool] = {"index": False, "middle": False, "ring": False, "pinky": False}

        if landmarks is not None:
            cursor = self._landmark_to_point(landmarks, self.mp_hands.HandLandmark.INDEX_FINGER_TIP, w, h)
            finger_states = self._get_finger_states(landmarks)

        gesture = self._interpret_gesture(finger_states)
        return GestureResult(gesture=gesture, cursor=cursor, landmarks=landmarks, finger_states=finger_states)

    def draw_hand_annotations(
        self,
        frame: np.ndarray,
        landmarks: Any,
    ) -> None:
        """Overlay the landmark skeleton on the webcam feed."""
        self._drawing_utils.draw_landmarks(
            frame,
            landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self._drawing_styles.get_default_hand_landmarks_style(),
            self._drawing_styles.get_default_hand_connections_style(),
        )

    def _get_finger_states(self, landmarks: Any) -> Dict[str, bool]:
        mh = self.mp_hands.HandLandmark
        tips = {"index": mh.INDEX_FINGER_TIP, "middle": mh.MIDDLE_FINGER_TIP, "ring": mh.RING_FINGER_TIP, "pinky": mh.PINKY_TIP}
        pips = {"index": mh.INDEX_FINGER_PIP, "middle": mh.MIDDLE_FINGER_PIP, "ring": mh.RING_FINGER_PIP, "pinky": mh.PINKY_PIP}
        states: Dict[str, bool] = {}
        for name in tips:
            tip = landmarks.landmark[tips[name]]
            pip = landmarks.landmark[pips[name]]
            states[name] = tip.y < pip.y
        return states

    def _interpret_gesture(self, finger_states: Dict[str, bool]) -> str:
        idx = finger_states["index"]
        mid = finger_states["middle"]
        ring = finger_states["ring"]
        pinky = finger_states["pinky"]

        if idx and mid and ring and pinky:
            return "clear"
        if not idx and not mid and not ring and not pinky:
            return "fist"
        if idx and not mid and not ring and not pinky:
            return "draw"
        return "idle"

    @staticmethod
    def _landmark_to_point(
        landmarks: Any,
        index: mp.solutions.hands.HandLandmark,
        width: int,
        height: int,
    ) -> Point:
        lm = landmarks.landmark[index]
        return int(lm.x * width), int(lm.y * height)
