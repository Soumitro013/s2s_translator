import argparse
from s2s_pipeline import SpeechToSpeechTranslator

def main():
    parser = argparse.ArgumentParser(description="Speech-to-Speech Translator CLI")
    parser.add_argument("--in", dest="in_audio", required=True, help="Input audio path")
    parser.add_argument("--src", dest="src", required=True, help="Source language code (e.g., hi)")
    parser.add_argument("--tgt", dest="tgt", required=True, help="Target language code (e.g., en)")
    parser.add_argument("--out", dest="out_audio", default="out.wav", help="Output WAV path")
    parser.add_argument("--asr", dest="asr_size", default="small", help="Whisper size: tiny/base/small/medium/large")

    args = parser.parse_args()

    s2s = SpeechToSpeechTranslator(asr_model_size=args.asr, src_lang=args.src)
    result = s2s.run_file(args.in_audio, args.src, args.tgt, args.out_audio)
    print("ASR (L1):", result["asr_text"])
    print("Translation (L2):", result["translated_text"])
    print("Saved L2 audio to:", result["out_audio"])

if __name__ == "__main__":
    main()
