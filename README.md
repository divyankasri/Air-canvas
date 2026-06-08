# Air Canvas 🎨

A real-time virtual drawing application that allows users to draw in the air using hand gestures detected through a webcam.

## 📌 Project Overview

Air Canvas is a computer vision-based application that tracks hand movements and recognizes gestures using MediaPipe and OpenCV. Users can draw on a virtual canvas without touching any physical device.

## 🚀 Features

* Real-time hand tracking
* Air drawing using index finger gestures
* Gesture-based drawing control
* Canvas clearing using hand gestures
* Smooth cursor movement
* Webcam-based interaction

## 🛠️ Technologies Used

* Python 3.11
* OpenCV
* MediaPipe Hands
* NumPy

## 📂 Project Structure

```text
air-canvas-main/
│
├── main.py
├── gesture_detector.py
├── canvas.py
├── utils.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/divyankasri/Air-canvas.git
```

2. Navigate to the project folder:

```bash
cd Air-canvas
```

3. Create and activate a virtual environment:

```bash
python -m venv .venv
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the application:

```bash
python main.py
```

## 🎮 Controls

| Gesture         | Action       |
| --------------- | ------------ |
| Index Finger Up | Draw         |
| Fist            | Stop Drawing |
| Open Palm       | Clear Canvas |

## 🔮 Future Enhancements

* Multiple brush colors
* Brush size adjustment
* Eraser tool
* Save drawings as images
* Gesture customization

## 👩‍💻 Author

**Divyanka Srivastava**

B.Tech Computer Science Engineering
Jaipur National University

## 📄 License

This project is created for educational and learning purposes.

