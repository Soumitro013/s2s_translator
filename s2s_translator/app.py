import streamlit as st
import os
import tempfile
from s2s_pipeline import SpeechToSpeechTranslator
from utils_lang import LANG_NAMES

st.set_page_config(page_title="S2S Translator", page_icon="🗣️", layout="centered")
st.title("🗣️ Speech-to-Speech Translator (Open-Source)")
st.caption("ASR → MT → TTS | Whisper + MarianMT + pyttsx3 | Works offline after first run")


with st.sidebar:
    st.header("Settings")
    asr_size = st.selectbox("ASR Model Size (Whisper)", ["tiny", "base", "small", "medium"], index=2)
    src = st.selectbox("Source Language (L1)", list(LANG_NAMES.keys()), format_func=lambda k: f"{k} - {LANG_NAMES[k]}", index=1)
    tgt = st.selectbox("Target Language (L2)", list(LANG_NAMES.keys()), format_func=lambda k: f"{k} - {LANG_NAMES[k]}" , index=0)
    st.info("Tip: For best results, keep L1 and L2 different and ensure MarianMT has that pair or will pivot via English.")

uploaded = st.file_uploader("Upload an audio file (wav/mp3/m4a)", type=["wav","mp3","m4a","flac","ogg"])

col1, col2 = st.columns(2)
with col1:
    st.write("**Input (L1) Audio**")
with col2:
    st.write("**Output (L2) Audio**")


if uploaded is not None:
    st.audio(uploaded, format="audio/wav")
    if st.button("Translate 🔄", use_container_width=True):
        with st.spinner("Running ASR → MT → TTS..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded.name)[1]) as tmp_in:
                tmp_in.write(uploaded.read())
                tmp_in.flush()
                in_path = tmp_in.name

            out_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name

            s2s = SpeechToSpeechTranslator(asr_model_size=asr_size, src_lang=src)
            result = s2s.run_file(in_path, src, tgt, out_path)

        st.success("Done!")
        st.subheader("Transcripts")
        st.markdown(f"**ASR (L1):** {result['asr_text']}")
        st.markdown(f"**Translation (L2):** {result['translated_text']}")
        st.audio(out_path, format="audio/wav")
        st.download_button("Download L2 Audio", data=open(out_path, "rb").read(), file_name="translation_L2.wav")


st.markdown("---")
st.caption("Built with ❤️ using Whisper, MarianMT, and pyttsx3. Add more language pairs in `utils_lang.py`.")
