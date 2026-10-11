# 🎙️ AudioReader — Multilingual Text-to-Speech Content Reader

AudioReader is a modern, high-fidelity web application that transforms written content into natural-sounding speech across 11 Indian languages, powered by **Sarvam AI Bulbul TTS API**.

Designed for students, content creators, book readers, and accessibility users, AudioReader supports direct typing, text pasting, and document uploading (**PDF**, **DOCX**, **TXT**), complete with intelligent sentence-level chunking for long content and seamless audio assembly.

---

## 🌟 Key Features

- **Multilingual Support (11 Indian Languages):**
  - English (`en-IN`), Hindi (`hi-IN`), Bengali (`bn-IN`), Kannada (`kn-IN`), Malayalam (`ml-IN`), Marathi (`mr-IN`), Odia (`od-IN`), Punjabi (`pa-IN`), Tamil (`ta-IN`), Telugu (`te-IN`), Gujarati (`gu-IN`).
- **Verified Voice Personas:**
  - Dynamic voice persona catalog filtered by model and language (Male/Female voices tailored for narration, news, storytelling, and conversational tones).
- **Dual Engine Models:**
  - **Bulbul v4-Flash (Recommended):** High-speed, high-fidelity neural narration with 200+ distinct voice styles.
  - **Bulbul v3 (Stable):** Classic Indian voice personas (`shubh`, `aditya`, `ritu`, `priya`, etc.) with universal coverage.
- **Document Processing:**
  - **PDF Extraction:** Built with `PyMuPDF` with automatic detection and diagnostics for scanned/image-only PDFs.
  - **Word Documents:** Full `.docx` paragraph and table text parsing via `python-docx`.
  - **Text Files:** Encoding-resilient `.txt` reader supporting UTF-8, Latin-1, and Windows CP1252.
- **Smart Sentence Chunking & Audio Stitching:**
  - Automatically divides content exceeding Sarvam AI's single-request limit (2,500 chars) into natural, sentence-preserved sections.
  - Generates audio sequentially with a live progress indicator and stitches segments together with micro-pause smoothing.
- **Audio Controls & Export:**
  - In-browser playback with speed/pace multiplier control (0.5x to 2.0x).
  - One-click instant audio download in standard **WAV** format with dynamic metadata filenames.
- **Security & Privacy:**
  - Never hardcodes or logs secret API keys.
  - Supports `.env` loading and session overrides.

---

## 🛠️ Project Structure

```
text-to-speech_content_reader/
├── app.py                  # Main Streamlit web application
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .env                    # Local secrets (ignored by Git)
├── .gitignore              # Git ignore rules for keys & virtualenv
├── README.md               # Documentation & setup guide
├── run_tests.py            # Comprehensive test suite runner
├── src/
│   ├── __init__.py
│   ├── config.py           # Languages, models, and verified voice catalog
│   ├── chunker.py          # Sentence-aware multilingual text chunker
│   ├── doc_processor.py    # Document extractors (PDF, DOCX, TXT)
│   └── tts_engine.py       # Sarvam AI API client & audio stitching
├── tests/
│   ├── test_chunker.py     # Unit tests for text chunker
│   ├── test_doc_processor.py# Unit tests for document extraction
│   └── test_tts_api.py     # Integration test for live Sarvam TTS
└── test_samples/           # Generated test audio and documents
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10, 3.11, or 3.12
- `ffmpeg` (for audio processing)

### 2. Clone & Setup Virtual Environment
```bash
cd text-to-speech_content_reader
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure API Key
Create a `.env` file in the project root:
```bash
cp .env.example .env
```
Open `.env` and set your Sarvam AI API key:
```ini
SARVAM_API_KEY=your_sarvam_api_key_here
```

> **How to get an API Key:** Sign up at [dashboard.sarvam.ai](https://dashboard.sarvam.ai) and generate an API Subscription Key from the dashboard.

### 4. Run the Application
Launch the Streamlit app:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Running Automated Tests

Run the full verification test suite:
```bash
PYTHONPATH=. ./venv/bin/python run_tests.py
```

This runs:
1. **Sentence Chunker Tests:** Short texts, long multi-paragraph texts, multilingual punctuation (`।`, `.`, `!`).
2. **Document Processing Tests:** Plain text, DOCX, and PDF text extraction.
3. **Live Sarvam TTS API Test:** Verifies live synthesis, audio decoding, and chunk concatenation using the active API key.

---

## 🔒 Security Best Practices
- The `.env` file is included in `.gitignore` and is never committed to source control.
- API keys are masked in the UI (`sk_iu6...gO74 (36 chars)`) and are never written to client logs.
