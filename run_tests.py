"""
Full Verification Test Suite for AudioReader.
Runs unit tests for chunking, document processing, and live TTS generation.
"""

import sys
import os

print("=" * 60)
print("🚀 RUNNING AUDIOREADER TEST SUITE")
print("=" * 60)

# 1. Chunker Test
print("\n[1/3] Testing Smart Sentence Chunker...")
from tests.test_chunker import test_short_text, test_empty_text, test_long_text_split, test_multilingual_full_stops
test_short_text()
test_empty_text()
test_long_text_split()
test_multilingual_full_stops()
print("✅ Chunker tests passed successfully!")

# 2. Document Processing Test
print("\n[2/3] Testing Document Extraction (PDF, DOCX, TXT)...")
from tests.test_doc_processor import test_txt_extraction, test_docx_extraction, test_pdf_extraction, test_metrics_calculation
test_txt_extraction()
test_docx_extraction()
test_pdf_extraction()
test_metrics_calculation()
print("✅ Document extraction tests passed successfully!")

# 3. Live TTS Synthesis Test
print("\n[3/3] Testing Live Sarvam AI Bulbul TTS API Integration...")
from tests.test_tts_api import run_tts_api_test
live_success = run_tts_api_test()
if live_success:
    print("✅ Live Sarvam Bulbul TTS API integration passed successfully!")
else:
    print("❌ Live TTS test failed.")
    sys.exit(1)

print("\n" + "=" * 60)
print("🎉 ALL TESTS PASSED! APPLICATION READY FOR USE.")
print("=" * 60)
