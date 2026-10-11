"""
AudioReader - Text-to-Speech Content Reader
Powered by Sarvam AI Bulbul TTS API
"""

import os
import datetime
import streamlit as st

from src.config import (
    SUPPORTED_LANGUAGES,
    SUPPORTED_MODELS,
    get_voices_for_selection,
    SAMPLE_TEXTS,
    MAX_CHARS_PER_REQUEST,
)
from src.doc_processor import (
    extract_document_text,
    get_text_metrics,
)
from src.tts_engine import (
    synthesize_text_to_speech,
    get_api_key,
    get_masked_api_key,
    is_api_key_configured,
)

# ---------------------------------------------------------
# Page Setup & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="AudioReader | Turn Content into Natural Speech",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
        border-radius: 16px;
        padding: 28px 32px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(49, 46, 129, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .brand-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .brand-subtitle {
        font-size: 1.05rem;
        color: #c7d2fe;
        margin-top: 6px;
        margin-bottom: 0;
        font-weight: 400;
    }

    .metric-chip {
        display: inline-flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(8px);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 500;
        color: #e0e7ff;
        margin-top: 14px;
        margin-right: 8px;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }

    .stats-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .stat-item {
        text-align: center;
    }

    .stat-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        font-weight: 600;
    }

    .stat-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 2px;
    }

    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }

    .generate-btn button {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
        color: white !important;
        font-size: 1.05rem !important;
        padding: 12px 24px !important;
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35) !important;
        width: 100% !important;
    }

    .generate-btn button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.45) !important;
    }

    .audio-player-card {
        background: linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 100%);
        border: 1px solid #bbf7d0;
        border-radius: 16px;
        padding: 22px;
        margin-top: 18px;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.08);
    }

    .status-badge-ok {
        background: #dcfce7;
        color: #15803d;
        border: 1px solid #86efac;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        display: inline-block;
    }

    .status-badge-warn {
        background: #fef9c3;
        color: #a16207;
        border: 1px solid #fde047;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        display: inline-block;
    }

    .chunk-alert {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        font-size: 0.88rem;
        color: #1e40af;
        margin-bottom: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "input_text" not in st.session_state:
    st.session_state.input_text = SAMPLE_TEXTS["en-IN"]

if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None

if "audio_metadata" not in st.session_state:
    st.session_state.audio_metadata = None

if "extracted_doc_name" not in st.session_state:
    st.session_state.extracted_doc_name = None

# ---------------------------------------------------------
# Sidebar: Settings & Configuration
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Speech Settings")
    st.caption("Configure voice persona, language, and model")

    # API Key Configuration
    st.markdown("#### 🔑 Sarvam AI API")
    env_configured = is_api_key_configured()

    if env_configured:
        st.markdown(
            f'<div class="status-badge-ok">✓ Active Key: {get_masked_api_key()}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status-badge-warn">⚠ Missing API Key in .env</div>',
            unsafe_allow_html=True,
        )

    # Optional key override in current session without persisting to disk
    user_api_key_override = st.text_input(
        "API Key (Session Override)",
        type="password",
        placeholder="sk_... (leave empty to use .env key)",
        help="Optional: If you wish to provide a different key for this session, enter it here. It is never logged or exposed.",
    )
    active_key = user_api_key_override.strip() if user_api_key_override.strip() else get_api_key()

    st.markdown("---")

    # Model Selection
    st.markdown("#### 🧠 Model Selection")
    model_options = {m["id"]: m["name"] for m in SUPPORTED_MODELS}
    selected_model_id = st.selectbox(
        "TTS Engine Model",
        options=list(model_options.keys()),
        format_func=lambda x: model_options[x],
        index=0,
        help="bulbul:v4-flash is the latest high-fidelity model from Sarvam AI.",
    )

    # Language Selection
    st.markdown("#### 🌐 Language")
    lang_code_to_item = {l["code"]: l for l in SUPPORTED_LANGUAGES}
    selected_lang_code = st.selectbox(
        "Narration Language",
        options=list(lang_code_to_item.keys()),
        format_func=lambda code: f"{lang_code_to_item[code]['name']} ({lang_code_to_item[code]['native']})",
        index=0,
        help="Sarvam Bulbul natively supports 11 Indian languages with high accent accuracy.",
    )

    # Voice / Speaker Selection
    st.markdown("#### 🗣️ Voice Persona")
    available_voices = get_voices_for_selection(selected_model_id, selected_lang_code)
    voice_map = {v["id"]: v for v in available_voices}

    selected_voice_id = st.selectbox(
        "Speaker Voice",
        options=list(voice_map.keys()),
        format_func=lambda vid: f"{voice_map[vid]['name']} ({voice_map[vid]['gender']} • {voice_map[vid]['tone']})",
        index=0,
        help="Select a voice persona tailored to your content tone.",
    )

    # Speaking Pace / Speed Control
    st.markdown("#### ⚡ Speaking Pace")
    speaking_pace = st.slider(
        "Speed Multiplier",
        min_value=0.5,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="1.0 is standard natural pace. 0.8 is slower for clarity, 1.25 is faster for quick listening.",
    )

    st.markdown("---")
    st.caption("🔒 **Security Note:** Keys are read exclusively from environment variables or safe memory inputs, never logged or committed.")

# ---------------------------------------------------------
# Header Section
# ---------------------------------------------------------
st.markdown(
    """
    <div class="main-header">
        <h1 class="brand-title">🎙️ AudioReader</h1>
        <p class="brand-subtitle">Turn your written documents and text into natural, lifelike speech using Sarvam AI Bulbul.</p>
        <div>
            <span class="metric-chip">✨ 11 Indian Languages</span>
            <span class="metric-chip">⚡ Bulbul v4-Flash</span>
            <span class="metric-chip">📄 PDF, DOCX, TXT Support</span>
            <span class="metric-chip">🧩 Auto-Chunking for Long Texts</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Main Workspace: Tabs for Text Input & Document Upload
# ---------------------------------------------------------
tab_editor, tab_upload = st.tabs(["✍️ Text Input & Editor", "📂 Document Upload (PDF / DOCX / TXT)"])

with tab_editor:
    col_tools_left, col_tools_right = st.columns([3, 1])
    with col_tools_left:
        st.markdown("**Enter or paste your text to narrate:**")
    with col_tools_right:
        # Quick sample text loader
        sample_choice = st.selectbox(
            "Load Sample",
            options=["None", "English", "Hindi", "Odia", "Bengali", "Tamil"],
            index=0,
            label_visibility="collapsed",
        )
        if sample_choice != "None":
            sample_code_map = {
                "English": "en-IN",
                "Hindi": "hi-IN",
                "Odia": "od-IN",
                "Bengali": "bn-IN",
                "Tamil": "ta-IN",
            }
            target_sample_code = sample_code_map[sample_choice]
            st.session_state.input_text = SAMPLE_TEXTS.get(target_sample_code, "")

    text_area_val = st.text_area(
        label="Content Editor",
        value=st.session_state.input_text,
        height=260,
        placeholder="Type or paste your content here...",
        label_visibility="collapsed",
    )
    # Sync state
    st.session_state.input_text = text_area_val

with tab_upload:
    st.markdown("**Upload a document to extract readable text:**")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx", "txt"],
        help="Upload standard PDF, Microsoft Word (.docx), or plain text files.",
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        file_name = uploaded_file.name

        with st.spinner(f"Extracting text from {file_name}..."):
            extracted_text, doc_meta, err_msg = extract_document_text(file_bytes, file_name)

        if err_msg:
            st.error(f"⚠️ {err_msg}")
        else:
            st.success(f"✓ Successfully extracted text from **{file_name}** ({len(file_bytes) / 1024:.1f} KB)")
            
            # Document metadata display
            if doc_meta.get("file_type") == "PDF":
                st.info(f"📄 PDF Metadata: {doc_meta.get('num_pages')} total pages inspected.")
            elif doc_meta.get("file_type") == "DOCX":
                st.info(f"📝 DOCX Metadata: {doc_meta.get('paragraphs_count')} paragraphs found.")

            # Load into editor button
            if st.button("📥 Load Extracted Text into Editor", use_container_width=True):
                st.session_state.input_text = extracted_text
                st.session_state.extracted_doc_name = file_name
                st.rerun()

            with st.expander("👁️ Preview Extracted Text", expanded=False):
                st.text_area("Extracted Preview", value=extracted_text, height=200, disabled=True)

# ---------------------------------------------------------
# Text Metrics & Chunking Information
# ---------------------------------------------------------
current_text = st.session_state.input_text.strip()
metrics = get_text_metrics(current_text)

# Metrics Ribbon
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Total Characters", f"{metrics['char_count']:,}")
with col_m2:
    st.metric("Total Words", f"{metrics['word_count']:,}")
with col_m3:
    st.metric("Est. Duration", f"~{metrics['est_duration_minutes']} min")
with col_m4:
    chunks_needed = max(1, (metrics["char_count"] // MAX_CHARS_PER_REQUEST) + (1 if metrics["char_count"] % MAX_CHARS_PER_REQUEST > 0 else 0)) if metrics["char_count"] > 0 else 0
    st.metric("API Chunks", f"{chunks_needed} part(s)")

# Display chunking notification if text exceeds individual API request limit
if metrics["char_count"] > MAX_CHARS_PER_REQUEST:
    st.markdown(
        f"""
        <div class="chunk-alert">
            ℹ️ <strong>Smart Chunking Activated:</strong> Your text is {metrics['char_count']:,} characters, which exceeds Sarvam AI's single-request limit ({MAX_CHARS_PER_REQUEST:,} chars). 
            AudioReader will safely divide your content into <strong>{chunks_needed} sentence-preserved sections</strong>, generate each part, and stitch them into a seamless audio file.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# Audio Generation Action
# ---------------------------------------------------------
st.markdown("<div class='generate-btn'>", unsafe_allow_html=True)
generate_clicked = st.button("🎙️ Generate Audio Narration", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

if generate_clicked:
    if not current_text:
        st.error("Please enter or extract text before generating audio.")
    elif not active_key:
        st.error("Sarvam AI API Key is not detected. Please add your key to `.env` or input it in the sidebar.")
    else:
        # Progress UI
        progress_bar = st.progress(0.0)
        status_box = st.empty()

        def update_progress(current_chunk: int, total_chunks: int, status: str):
            pct = float(current_chunk) / float(total_chunks)
            progress_bar.progress(min(pct, 1.0))
            status_box.info(f"⏳ {status}")

        try:
            with st.spinner("Connecting to Sarvam AI Bulbul TTS..."):
                result = synthesize_text_to_speech(
                    text=current_text,
                    language_code=selected_lang_code,
                    speaker=selected_voice_id,
                    model=selected_model_id,
                    pace=speaking_pace,
                    api_key=active_key,
                    progress_callback=update_progress,
                )

            if result["success"] and result["audio_bytes"]:
                progress_bar.progress(1.0)
                status_box.empty()
                st.session_state.audio_bytes = result["audio_bytes"]
                st.session_state.audio_metadata = {
                    "language": lang_code_to_item[selected_lang_code]["name"],
                    "language_code": selected_lang_code,
                    "voice": voice_map[selected_voice_id]["name"],
                    "voice_id": selected_voice_id,
                    "model": selected_model_id,
                    "pace": speaking_pace,
                    "char_count": result["char_count"],
                    "chunks_count": result["chunks_count"],
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                st.success("🎉 Audio narration successfully generated!")
            else:
                progress_bar.empty()
                status_box.empty()
                st.error(f"Speech generation failed: {result['error']}")

        except Exception as e:
            progress_bar.empty()
            status_box.empty()
            st.error(f"An unexpected error occurred during synthesis: {str(e)}")

# ---------------------------------------------------------
# Audio Output & Download Area
# ---------------------------------------------------------
if st.session_state.audio_bytes is not None:
    meta = st.session_state.audio_metadata or {}
    
    st.markdown("---")
    st.markdown("### 🎧 Generated Audio Player")

    col_player, col_meta = st.columns([3, 2])

    with col_player:
        st.audio(st.session_state.audio_bytes, format="audio/wav")

        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_voice = meta.get("voice_id", "voice")
        safe_lang = meta.get("language_code", "lang")
        download_filename = f"audioreader_{safe_lang}_{safe_voice}_{timestamp_str}.wav"

        st.download_button(
            label="⬇️ Download Audio (WAV)",
            data=st.session_state.audio_bytes,
            file_name=download_filename,
            mime="audio/wav",
            use_container_width=True,
        )

    with col_meta:
        st.markdown(
            f"""
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px;">
                <h5 style="margin-top: 0; color: #1e293b;">📋 Narration Summary</h5>
                <p style="margin: 4px 0; font-size: 0.88rem;"><strong>Language:</strong> {meta.get('language', 'N/A')} (<code>{meta.get('language_code', '')}</code>)</p>
                <p style="margin: 4px 0; font-size: 0.88rem;"><strong>Speaker Persona:</strong> {meta.get('voice', 'N/A')}</p>
                <p style="margin: 4px 0; font-size: 0.88rem;"><strong>Model:</strong> <code>{meta.get('model', '')}</code></p>
                <p style="margin: 4px 0; font-size: 0.88rem;"><strong>Speaking Pace:</strong> {meta.get('pace', 1.0)}x</p>
                <p style="margin: 4px 0; font-size: 0.88rem;"><strong>Characters Synthesized:</strong> {meta.get('char_count', 0):,}</p>
                <p style="margin: 4px 0; font-size: 0.88rem;"><strong>Chunks Merged:</strong> {meta.get('chunks_count', 1)}</p>
                <p style="margin: 4px 0; font-size: 0.78rem; color: #64748b;">Generated at: {meta.get('timestamp', '')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.caption(
    "AudioReader Prototype • Powered by Sarvam AI Bulbul TTS API • "
    "Designed for high-quality multilingual narration"
)
