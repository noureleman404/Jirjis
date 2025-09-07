# Jirjis (جرجس) 🎬

"Because no one should get up in the middle of movie night."

Jirjis (جرجس) is a computer vision system inspired by Jarvis from Iron Man, designed to let you control your laptop remotely with hand gestures.
Currently, it allows you to control system volume using just your fingers ✌️.

## In the future, Jirjis will support:

- ▶️ Play/Pause control of videos

- 🖥️ Running in the background (so the app doesn’t ruin your movie night by popping up)

## ✨ Features

- 📸 Real-time hand tracking powered by MediaPipe

- 🔊 Volume control using the distance between your thumb and index finger

- 🎚️ Smooth visual feedback with a live volume bar overlay

- ⌨️ Press q to quit at any time

## 🎥 Demo

- Pinch fingers closer → 🔉 Volume decreases

- Spread fingers apart → 🔊 Volume increases

---

## 🛠️ Tech Stack

* Python 3.x

* OpenCV
  → for video capture & visualization

- MediaPipe
 → for hand detection & landmark tracking

- PyCaw
  → for system volume control

## 📂 Project Structure
```
jirjis/
│
├── handTrackingModule.py   # Hand tracking utilities (detects landmarks, positions, etc.)
├── volum_control.py        # Main app: gesture-based volume control
└── README.md               # You are here
```

## 🚀 Getting Started
1. Clone the repo
```bash
git clone https://github.com/your-username/jirjis.git
cd jirjis
```

3. Install dependencies
```bash
pip install opencv-python mediapipe comtypes pycaw numpy
```

5. Run Jirjis
```bash
python volum_control.py
```

## 🙌 Future Plans

 - Adding play/pause gesture control

 - Run Jirjis in the background

 - Extend gestures to skip/rewind video

## 💡 Inspiration

This project started as a fun solution for lazy movie nights 🎬, when no one wanted to get up to adjust the volume.
It’s named Jirjis (جرجس) as a funny spin on Jarvis from Iron Man.

## 🤝 Contributing

Pull requests are welcome! Got a cool gesture idea? Send it over.
