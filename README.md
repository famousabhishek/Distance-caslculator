📏 Real-Time Object Measurement Tool (Python)

This project is a real-time distance and area measurement tool built with Python, OpenCV, and Mediapipe.
It allows you to use your phone camera as a webcam and measure distances & areas of objects directly from the video feed.

🚀 Features

📷 Use your phone camera or default webcam

📏 Measure distances in cm, inches, feet, and meters

📐 Calculate areas of shapes:

Rectangle

Square

Circle

🖱 Interactive buttons:

Reset

Undo

Quit

⚡ Works in real-time

🛠 Technologies & Packages Used

Python 3.10.0 → main programming language

OpenCV → video streaming & image processing

NumPy → mathematical calculations

Mediapipe → object detection & tracking

⚡ Why Python 3.10.0?

The latest Python versions had compatibility issues with Mediapipe and some NumPy versions.

Downgrading to Python 3.10.0 fixed these issues.

Used numpy==1.26.4 for stable performance.

🖥 Installation Guide
1️⃣ Clone this repository
git clone https://github.com/your-username/object-measurement-tool.git
cd object-measurement-tool

2️⃣ Create a virtual environment (recommended)
python -m venv venv

Activate it:

Windows: venv\Scripts\activate

Linux/Mac: source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

If requirements.txt is not available, install manually:

pip install opencv-python numpy==1.26.4 mediapipe

📷 How to Use

1. Run the script
   python measure.py

2. Input Camera Source

Leave blank → use default webcam

Enter IP (e.g., http://192.168.0.101:8080) → use phone camera
(📌 You can install apps like IP Webcam (Android) or DroidCam to turn your phone into a camera.)

3. Start Measuring

Click two points → measure distance (cm, inches, feet, meters)

Select shape (Rectangle, Circle, Square) → click points → area will be calculated

Use buttons (Reset, Undo, Quit) to control

🐞 Challenges Faced

❌ Errors installing Mediapipe on the latest Python → solved by using Python 3.10.0

⚠️ NumPy version conflict → fixed with numpy==1.26.4

🔎 Sometimes gives wrong results for long objects because the camera view makes them look smaller than real life (still working on solving this!)

🎯 Future Improvements

✅ Add calibration system for accurate real-world measurements

✅ Improve object detection with AI models

✅ Convert project into a desktop/mobile app
