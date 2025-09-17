# Speech-to-Speech Translation for Indic Languages

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![JOSS](https://joss.theoj.org/papers/placeholder/status.svg)](https://joss.theoj.org/)

An open-source, modular **speech-to-speech (S2S) translation pipeline** for Indic languages.  
The system integrates **Automatic Speech Recognition (ASR)**, **Machine Translation (MT)**, and **Text-to-Speech (TTS)** into a unified Python framework.  

It supports **Indic ↔ English** and **Indic ↔ Indic** translations (via pivot),  
and provides both a **Command-Line Interface (CLI)** and a **Streamlit Web App**.  

---

## ✨ Features
- **ASR**: [Whisper](https://github.com/openai/whisper) (robust, multilingual ASR).  
- **MT**: MarianMT (baseline), [IndicTrans2](https://github.com/AI4Bharat/IndicTrans2) (improved Indic ↔ English translations).  
- **TTS**: gTTS (natural online voices), pyttsx3 (offline fallback).  
- **Interfaces**: CLI (`cli.py`) and Web App (`app.py`).  
- **Languages supported**: Hindi, Bengali, Tamil, and more (via IndicTrans2).  
- **Lightweight**: CPU execution possible (~8–12 sec for a 5s clip).  

---

## 📂 Repository Structure
s2s-translator/
│
├── s2s_translator/              # main source code
│   ├── __init__.py
│   ├── s2s_pipeline.py          # core pipeline (ASR → MT → TTS)
│   ├── utils_lang.py            # language utilities
│   ├── cli.py                   # CLI interface
│   └── app.py                   # Streamlit app
│
├── samples/                     # demo audio files
│   └── demo_hi.wav
│
├── tests/                       # unit tests
│   └── test_pipeline.py
│
├── README.md                    # this file
├── requirements.txt             # dependencies
├── setup.py                     # install script
├── LICENSE                      # MIT License
├── paper.md                     # JOSS article
└── paper.bib                    # references

---

## 🚀 Installation

### Prerequisites
- Python 3.9+  
- [ffmpeg](https://ffmpeg.org/download.html) (required for audio processing).  

### Clone the repository
```bash
git clone https://github.com/yourusername/s2s-translator.git
cd s2s-translator
```

### Create virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate    # Windows
```

### Install dependencies
```bash
pip install -r requirements.txt
```

Or install directly as a package:
```bash
pip install -e .
```

---

## 🛠 Usage

### Command-Line Interface (CLI)
```bash
python s2s_translator/cli.py --input samples/demo_hi.wav --source hi --target en
```

This will:
1. Transcribe Hindi speech.  
2. Translate into English.  
3. Generate English speech output (`output.mp3`).  

### Web App (Streamlit)
```bash
streamlit run s2s_translator/app.py
```

This opens a browser-based interface for uploading audio and selecting source/target languages.  

---

## 📊 Example Workflow

**Input (Hindi):**  
“कल पार्टी है क्या?”  

**ASR (Whisper):**  
“कल पार्टी है क्या?”  

**MT (IndicTrans2):**  
“Is there a party tomorrow?”  

**TTS (gTTS):**  
Natural English speech output (`output.mp3`).  

---

## ✅ Running Tests
We provide a minimal test suite to ensure the pipeline runs correctly.  

```bash
pytest tests/
```

Expected result:  
```
tests/test_pipeline.py .                                           [100%]
1 passed in X.XXs
```

---

## 📚 Citation

If you use this software in your research, please cite:

```bibtex
@article{YourName2025s2s,
  title={An Open-Source Speech-to-Speech Translation Pipeline for Indic Languages},
  author={Your Name},
  journal={Journal of Open Source Software},
  year={2025}
}
```

---

## 📄 License
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.  

---

## 🙏 Acknowledgements
- [Whisper](https://github.com/openai/whisper) (OpenAI) for multilingual ASR.  
- [IndicTrans2](https://github.com/AI4Bharat/IndicTrans2) (AI4Bharat) for translation.  
- [HuggingFace Transformers](https://huggingface.co/transformers/) for model support.  
- [gTTS](https://pypi.org/project/gTTS/) and [pyttsx3](https://pypi.org/project/pyttsx3/) for TTS.  
