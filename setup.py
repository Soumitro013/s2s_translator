from setuptools import setup, find_packages

setup(
    name="s2s_translator",
    version="1.0.0",
    description="An open-source speech-to-speech translation pipeline for Indic languages",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/s2s-translator",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "openai-whisper",
        "streamlit>=1.20.0",
        "gTTS>=2.3.0",
        "pyttsx3>=2.90",
        "pydub>=0.25.1",
        "soundfile>=0.12.1",
        "numpy>=1.24.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
)
