import os
from typing import Optional, Tuple, List

import numpy as np
import soundfile as sf
from pydub import AudioSegment

# ASR
import whisper

# MT
from transformers import MarianMTModel, MarianTokenizer, pipeline

# TTS
import pyttsx3

from utils_lang import has_direct_marian, get_marian_name

# ---------- Audio Utils ----------

def load_audio_to_wav(path: str, target_sr: int = 16000) -> Tuple[np.ndarray, int]:
    """Load audio with pydub and convert to mono WAV float32 at target_sr."""
    audio = AudioSegment.from_file(path)
    audio = audio.set_frame_rate(target_sr).set_channels(1)
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    # Normalize 16-bit PCM to [-1, 1]
    if audio.sample_width == 2:
        samples = samples / 32768.0
    return samples, target_sr

def save_wav(samples: np.ndarray, sr: int, out_path: str):
    sf.write(out_path, samples, sr)

# ---------- ASR ----------
class ASRWhisper:
    def __init__(self, model_size: str = "small", device: Optional[str] = None, language: Optional[str] = None):
        self.model = whisper.load_model(model_size, device=device)
        self.language = language  # e.g., 'hi', 'en'

    def transcribe(self, audio_path: str) -> str:
        result = self.model.transcribe(audio_path, language=self.language)
        return result.get("text", "").strip()

# ---------- MT ----------
class MarianTranslator:
    def __init__(self, src_lang: str, tgt_lang: str):
        model_name = get_marian_name(src_lang, tgt_lang)
        if model_name is None:
            raise ValueError(f"No direct Marian model for {src_lang}->{tgt_lang}")
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)
        self.pipe = pipeline("translation", model=self.model, tokenizer=self.tokenizer)

    def translate(self, text: str) -> str:
        if not text.strip():
            return ""
        out = self.pipe(text, max_length=512)[0]["translation_text"]
        return out.strip()

# ---------- TTS ----------
class TTSOffline:
    def __init__(self, voice_name: Optional[str] = None, rate: Optional[int] = None):
        self.engine = pyttsx3.init()
        if rate is not None:
            self.engine.setProperty('rate', rate)
        if voice_name:
            # Try to find a matching voice by name substring
            for v in self.engine.getProperty('voices'):
                if voice_name.lower() in (v.name or '').lower():
                    self.engine.setProperty('voice', v.id)
                    break

    def synthesize_to_file(self, text: str, out_path: str):
        self.engine.save_to_file(text, out_path)
        self.engine.runAndWait()

# ---------- Orchestrator ----------
class SpeechToSpeechTranslator:
    def __init__(self, asr_model_size: str = "small", src_lang: Optional[str] = None):
        self.asr = ASRWhisper(model_size=asr_model_size, language=src_lang)

    def _translate_text(self, text: str, src: str, tgt: str) -> str:
        if has_direct_marian(src, tgt):
            translator = MarianTranslator(src, tgt)
            return translator.translate(text)

        # Fallback: pivot via English
        if src != 'en' and tgt != 'en':
            to_en = MarianTranslator(src, 'en').translate(text)
            to_tgt = MarianTranslator('en', tgt).translate(to_en)
            return to_tgt

        # If one side is English but direct model missing, try reverse + pivot
        if src == 'en' and not has_direct_marian('en', tgt):
            raise ValueError(f"No Marian model available for en->{tgt}. Add one in utils_lang.")
        if tgt == 'en' and not has_direct_marian(src, 'en'):
            raise ValueError(f"No Marian model available for {src}->en. Add one in utils_lang.")
        raise ValueError(f"Unsupported translation pair {src}->{tgt}")

    def run_file(self, in_audio_path: str, src_lang: str, tgt_lang: str, out_audio_path: str) -> dict:
        # 1) ASR
        text_src = self.asr.transcribe(in_audio_path)

        # 2) MT
        text_tgt = self._translate_text(text_src, src_lang, tgt_lang)

        # 3) TTS
        tts = TTSOffline()
        tts.synthesize_to_file(text_tgt, out_audio_path)

        return {
            "asr_text": text_src,
            "translated_text": text_tgt,
            "out_audio": out_audio_path,
        }
