from setuptools import setup, find_packages
with open("README.md", encoding="utf-8") as f:
    description = f.read()

setup(
    name="hand_gesture_recognizer_2DCNN",
    version="1.5.2",
    description="A library for recognizing hand gestures using 2D CNN",
    author="Umesh, Ankit, Sukrit, Manan, Siddhant",
    packages=find_packages(),
    install_requires=["opencv-python", "mediapipe", "numpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    long_description=description,
    long_description_content_type="text/markdown"
)
