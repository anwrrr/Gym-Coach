# Gym-Coach

Gym-Coach uses a webcam, MediaPipe pose landmarks, and OpenCV to give on-screen feedback for three dumbbell exercises: bicep curls, lateral raises, and push presses.

## Requirements

- Python 3.10
- A working webcam

## Install and run

```bash
git clone https://github.com/anwrrr/Gym-Coach.git
cd Gym-Coach
python -m pip install -r requirements.txt
python Gym-Coach/Gym-Coach.py
```

At the menu, press `1` for bicep curls, `2` for lateral raises, or `3` for push presses. In the bicep curl mode, press `l` or `r` to choose an arm. Press `q` to return to the menu, then `q` again to exit.

The program reads from the default camera (device `0`). If the camera cannot be opened, check that it is connected and that another application is not using it.

See [demo.mp4](demo.mp4) for a demonstration.
