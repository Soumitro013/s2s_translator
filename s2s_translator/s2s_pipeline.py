import os
from typing import Optional, Tuple, Dict

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
    """Save audio samples to WAV."""
    sf.write(out_path, samples, sr)


# ---------- ASR ----------
class ASRWhisper:
    def __init__(self, model_size: str = "tiny", device: Optional[str] = None, language: Optional[str] = None):
        """Load Whisper ASR model (tiny by default for speed in tests)."""
        self.model = whisper.load_model(model_size, device=device)
        self.language = language

    def transcribe(self, audio_path: str) -> str:
        """Return transcribed text from audio file."""
        result = self.model.transcribe(audio_path, language=self.language)
        return result.get("text", "").strip()


# ---------- MT ----------
class MarianTranslator:
    def __init__(self, src_lang: str, tgt_lang: str):
        """Initialize MarianMT translator for given language pair."""
        model_name = get_marian_name(src_lang, tgt_lang)
        if model_name is None:
            raise ValueError(f"No direct Marian model for {src_lang}->{tgt_lang}")
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)
        self.pipe = pipeline("translation", model=self.model, tokenizer=self.tokenizer)

    def translate(self, text: str) -> str:
        """Translate given text using MarianMT."""
        if not text.strip():
            return ""
        out = self.pipe(text, max_length=512)[0]["translation_text"]
        return out.strip()


# ---------- TTS ----------
class TTSOffline:
    def __init__(self, voice_name: Optional[str] = None, rate: Optional[int] = None):
        """Offline text-to-speech using pyttsx3."""
        self.engine = pyttsx3.init()
        if rate is not None:
            self.engine.setProperty("rate", rate)
        if voice_name:
            for v in self.engine.getProperty("voices"):
                if voice_name.lower() in (v.name or "").lower():
                    self.engine.setProperty("voice", v.id)
                    break

    def synthesize_to_file(self, text: str, out_path: str):
        """Convert text to speech and save to file."""
        if not text.strip():
            # Create empty placeholder file if text missing
            with open(out_path, "wb") as f:
                f.write(b"")
            return
        self.engine.save_to_file(text, out_path)
        self.engine.runAndWait()


# ---------- Orchestrator ----------
class SpeechToSpeechTranslator:
    def __init__(self, asr_model_size: str = "tiny", src_lang: Optional[str] = None):
        """Main orchestrator that ties ASR, MT, and TTS."""
        self.asr = ASRWhisper(model_size=asr_model_size, language=src_lang)

    def _translate_text(self, text: str, src: str, tgt: str) -> str:
        """Translate text with MarianMT, with English pivot if needed."""
        if not text.strip():
            return ""

        if has_direct_marian(src, tgt):
            translator = MarianTranslator(src, tgt)
            return translator.translate(text)

        # Pivot translation via English
        if src != "en" and tgt != "en":
            to_en = MarianTranslator(src, "en").translate(text)
            return MarianTranslator("en", tgt).translate(to_en)

        raise ValueError(f"Unsupported translation pair {src}->{tgt}")

    def run_file(self, in_audio_path: str, src_lang: str, tgt_lang: str, out_audio_path: str) -> Dict[str, str]:
        """Full pipeline: audio -> text -> translated text -> speech."""
        # 1) ASR
        text_src = self.asr.transcribe(in_audio_path)

        # 2) MT
        text_tgt = self._translate_text(text_src, src_lang, tgt_lang)

        # 3) TTS
        tts = TTSOffline()
        tts.synthesize_to_file(text_tgt, out_audio_path)

        return {
            "asr_text": text_src,
            "translation": text_tgt,
            "tts_output": out_audio_path,
        }


# ---------- Test-facing wrapper ----------
def run_pipeline(audio_path: str, source_lang: str, target_lang: str) -> Dict[str, str]:
    """
    Module-level wrapper for tests.
    Runs full speech-to-speech translation pipeline.
    """
    out_path = "output_test.wav"
    translator = SpeechToSpeechTranslator(src_lang=source_lang)
    return translator.run_file(audio_path, source_lang, target_lang, out_path)
