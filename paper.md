---
title: "An Open-Source Speech-to-Speech Translation Pipeline for Indic Languages"
authors:
  - name: "Your Name"
    affiliation: 1
affiliations:
  - name: "Your Institution, Department, City, Country"
    index: 1
date: 2025-09-17
bibliography: paper.bib
---

# Summary

India’s linguistic diversity, with 22 scheduled languages and hundreds of dialects, creates barriers to communication, education, and digital inclusion. While commercial systems such as Google Translate [@wu2016google] and Microsoft Translator provide speech translation, they are closed-source, often limited to major global languages, and primarily text-focused.  

This software presents an **open-source, end-to-end speech-to-speech (S2S) translation pipeline** for Indic languages. The system integrates **Automatic Speech Recognition (ASR)**, **Machine Translation (MT)**, and **Text-to-Speech (TTS)** modules into a modular Python framework. It supports multiple Indic languages through **Whisper-based transcription** [@radford2023whisper], **IndicTrans2-based translation** [@ramesh2023indictrans2], and **gTTS/pyttsx3 synthesis**, with both command-line and web interfaces. Demonstrations show that the system produces intelligible speech translations across languages with acceptable latency on CPU-only execution.  

By making the design and code openly available, this work offers a practical baseline for developers and researchers exploring multilingual speech technologies in low-resource contexts.  

# Statement of Need

Most existing translation systems are commercial, restricted to major languages, or focused on text rather than speech. Open-source alternatives for **Indic speech-to-speech translation** remain scarce. Researchers and developers working with Indian languages require deployable, modular, and extensible pipelines that integrate ASR, MT, and TTS without proprietary constraints.  

This software provides such a pipeline, enabling:  

- **Research** in speech translation for Indic and low-resource languages.  
- **Practical applications** in education, healthcare, and accessibility.  
- **Extensibility**, allowing future integration of new ASR/MT/TTS models.  

# Software Description

## Pipeline Overview

The system consists of three sequential modules:  

1. **Automatic Speech Recognition (ASR)**  
   - Model: OpenAI Whisper (small).  
   - Converts spoken input into source-language text.  

2. **Machine Translation (MT)**  
   - Baseline: MarianMT (Helsinki-NLP) [@junczys2018marian].  
   - Improved: IndicTrans2 [@ramesh2023indictrans2].  
   - Translates transcribed text into the target language.  

3. **Text-to-Speech (TTS)**  
   - Baseline: pyttsx3 (offline).  
   - Improved: gTTS (Google TTS).  
   - Converts translated text into spoken output.  

This modular design allows components to be swapped or upgraded independently.  

## Implementation

- **Language:** Python 3.11  
- **Core Libraries:** HuggingFace Transformers [@wolf2020transformers], Whisper, gTTS, Streamlit, PyDub, NumPy, SoundFile.  
- **Deployment:** CLI (`cli.py`) and Streamlit Web App (`app.py`).  
- **Performance:** ~8–12 sec to process a 5-second audio clip on CPU (Whisper-small).  

## Example Workflow

1. **Input (Hindi Audio):** “कल पार्टी है क्या?”  
2. **ASR (Whisper):** → “कल पार्टी है क्या?”  
3. **MT (IndicTrans2):** → “Is there a party tomorrow?”  
4. **TTS (gTTS):** → English audio output.  

The system supports **Indic ↔ English** and **Indic ↔ Indic** translations (via English pivot).  

# Discussion

The pipeline demonstrates that open-source tools can be effectively combined into a deployable S2S system for Indic languages. While the individual models exist separately, this integration contributes a **unified, reusable framework** that lowers the barrier for researchers and developers working on multilingual speech.  

**Strengths:**  
- Modular and extensible architecture.  
- Supports multiple Indic languages.  
- Lightweight and accessible.  

**Limitations:**  
- Not real-time on CPU.  
- gTTS requires internet.  
- Limited code-mixing handling.  

# Future Directions

- Integration of Coqui TTS or VITS for offline synthesis.  
- Deployment on mobile/edge devices with Whisper Tiny/Medium.  
- Support for Hinglish and other code-mixed speech.  
- Optimization for real-time use cases.  

# Acknowledgements

We thank the open-source communities behind Whisper, HuggingFace, and AI4Bharat for making their models and libraries publicly available.  

# References
