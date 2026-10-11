"""
Integration test for Sarvam AI Bulbul TTS API.
Validates live synthesis, audio decoding, and chunk stitching.
"""

import os
from dotenv import load_dotenv
from src.tts_engine import synthesize_text_to_speech, is_api_key_configured, get_masked_api_key

load_dotenv()


def run_tts_api_test():
    print(f"API Key configured: {is_api_key_configured()} ({get_masked_api_key()})")
    assert is_api_key_configured(), "API Key not found in .env"

    test_text = "Welcome to AudioReader. This is a live synthesis test verifying the Sarvam AI Bulbul Text-to-Speech integration."
    print("Testing bulbul:v4-flash with speaker shubh_en_narration...")
    res = synthesize_text_to_speech(
        text=test_text,
        language_code="en-IN",
        speaker="shubh_en_narration",
        model="bulbul:v4-flash",
        pace=1.0,
    )

    if not res["success"]:
        print(f"FAILED: {res['error']}")
        return False

    print(f"SUCCESS! Received {len(res['audio_bytes'])} bytes of audio. Chunks: {res['chunks_count']}")
    
    # Save test sample
    os.makedirs("test_samples", exist_ok=True)
    sample_path = "test_samples/test_output.wav"
    with open(sample_path, "wb") as f:
        f.write(res["audio_bytes"])
    print(f"Saved test audio to {sample_path}")
    return True


if __name__ == "__main__":
    success = run_tts_api_test()
    if not success:
        exit(1)
