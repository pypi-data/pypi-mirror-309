from setuptools import setup, find_packages

setup(
    name="hand_gesture_recognizer",
    version="0.1.0",
    description="A library for recognizing hand gestures using MediaPipe",
    author="Umesh Singh Verma",
    packages=find_packages(),
    install_requires=["opencv-python", "mediapipe", "numpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
