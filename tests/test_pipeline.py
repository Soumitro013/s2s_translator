import os
from s2s_translator import s2s_pipeline

def test_pipeline_runs():
    """
    Basic smoke test: check if pipeline runs end-to-end
    on a sample Hindi audio file and returns expected keys.
    """
    sample_path = os.path.join("samples", "demo_hi.wav")

    # Run pipeline (adjust function name if different in your code)
    result = s2s_pipeline.run_pipeline(
        audio_path=sample_path,
        source_lang="hi",
        target_lang="en"
    )

    # Check pipeline output has expected structure
    assert isinstance(result, dict)
    assert "asr_text" in result
    assert "translation" in result
    assert "tts_output" in result
