"""
Sarvam AI Bulbul Text-to-Speech Engine.
Handles API requests, chunking, rate limiting, and seamless audio stitching.
"""

import os
import io
import wave
import time
import base64
import logging
from typing import List, Dict, Any, Optional, Tuple
import requests
from dotenv import load_dotenv

from src.config import SARVAM_TTS_URL, MAX_CHARS_PER_REQUEST
from src.chunker import split_text_into_chunks

# Ensure .env is loaded
load_dotenv()

logger = logging.getLogger(__name__)


def get_api_key() -> Optional[str]:
    """Retrieves the Sarvam API key from environment variables or .env."""
    key = os.getenv("SARVAM_API_KEY", "").strip()
    return key if key else None


def get_masked_api_key() -> str:
    """Returns a safely masked preview of the active API key without exposing secrets."""
    key = get_api_key()
    if not key:
        return "Not configured"
    if len(key) <= 8:
        return "****"
    return f"{key[:6]}...{key[-4:]} ({len(key)} chars)"


def is_api_key_configured() -> bool:
    """Returns True if a valid-looking API key is present."""
    key = get_api_key()
    return bool(key and len(key) > 5)


def _call_sarvam_tts_single_chunk(
    text: str,
    language_code: str,
    speaker: str,
    model: str = "bulbul:v4-flash",
    pace: float = 1.0,
    api_key: Optional[str] = None,
    max_retries: int = 3,
) -> Tuple[Optional[bytes], Optional[str]]:
    """
    Calls Sarvam AI /text-to-speech for a single chunk of text with retries.
    
    Returns:
        (audio_bytes, error_message)
    """
    effective_key = api_key or get_api_key()
    if not effective_key:
        return None, "Sarvam API Key is missing. Please configure SARVAM_API_KEY in .env or the settings panel."

    headers = {
        "api-subscription-key": effective_key,
        "Content-Type": "application/json",
    }

    # Defensive fallback: if speaker is a universal v3 persona, ensure model is bulbul:v3
    effective_model = model
    if model == "bulbul:v4-flash" and ("_" not in speaker):
        effective_model = "bulbul:v3"

    payload = {
        "text": text,
        "target_language_code": language_code,
        "language_code": language_code,
        "model": effective_model,
        "speaker": speaker,
        "pace": float(pace),
        "speech_sample_rate": 22050,
        "enable_preprocessing": True,
    }

    last_error = ""

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(
                SARVAM_TTS_URL,
                json=payload,
                headers=headers,
                timeout=35,
            )

            # Success
            if response.status_code == 200:
                data = response.json()
                audios = data.get("audios", [])
                if not audios or not audios[0]:
                    return None, "Sarvam API returned an empty audio response."
                
                audio_bytes = base64.b64decode(audios[0])
                return audio_bytes, None

            # Rate limit (429) -> exponential backoff
            if response.status_code == 429:
                sleep_time = attempt * 2
                time.sleep(sleep_time)
                last_error = f"Rate limited by Sarvam API (429). Retrying in {sleep_time}s..."
                continue

            # Authentication error (401 / 403)
            if response.status_code in (401, 403):
                return None, f"Authentication failed ({response.status_code}): Invalid or unauthorized Sarvam API key."

            # Bad request (400 or 422)
            try:
                err_data = response.json()
                detail = err_data.get("message") or err_data.get("detail") or str(err_data)
            except Exception:
                detail = response.text[:200]
            
            last_error = f"Sarvam API Error ({response.status_code}): {detail}"
            # For 4xx errors other than 429, don't keep retrying identical invalid payloads
            if 400 <= response.status_code < 500:
                return None, last_error

        except requests.exceptions.Timeout:
            last_error = f"Request timed out (attempt {attempt}/{max_retries})."
            time.sleep(1)
        except requests.exceptions.ConnectionError as ce:
            last_error = f"Network connection error: {str(ce)}"
            time.sleep(1)
        except Exception as e:
            last_error = f"Unexpected error during TTS request: {str(e)}"
            break

    return None, last_error or "Failed to synthesize speech after multiple attempts."


def _create_silence_wav(duration_seconds: float = 0.2, sample_rate: int = 22050, channels: int = 1, sampwidth: int = 2) -> bytes:
    """Generates silent PCM WAV audio bytes for smooth transitions between chunks."""
    num_frames = int(sample_rate * duration_seconds)
    silent_frames = b"\x00" * (num_frames * channels * sampwidth)
    
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wav_out:
        wav_out.setnchannels(channels)
        wav_out.setsampwidth(sampwidth)
        wav_out.setframerate(sample_rate)
        wav_out.writeframes(silent_frames)
    
    return buf.getvalue()


def stitch_wav_bytes(wav_list: List[bytes], pause_between_chunks_sec: float = 0.15) -> bytes:
    """
    Seamlessly concatenates multiple WAV byte sequences into a single valid WAV file,
    normalizing headers and inserting natural brief pauses.
    """
    if not wav_list:
        return b""
    if len(wav_list) == 1:
        return wav_list[0]

    try:
        combined_frames = bytearray()
        first_params = None

        for idx, wav_data in enumerate(wav_list):
            with wave.open(io.BytesIO(wav_data), "rb") as wav_in:
                params = wav_in.getparams()
                frames = wav_in.readframes(wav_in.getnframes())

                if first_params is None:
                    first_params = params

                combined_frames.extend(frames)

                # Add small silence between chunks, but not after the last chunk
                if idx < len(wav_list) - 1 and pause_between_chunks_sec > 0:
                    num_silence_frames = int(params.framerate * pause_between_chunks_sec)
                    silence = b"\x00" * (num_silence_frames * params.nchannels * params.sampwidth)
                    combined_frames.extend(silence)

        out_buf = io.BytesIO()
        with wave.open(out_buf, "wb") as wav_out:
            wav_out.setnchannels(first_params.nchannels)
            wav_out.setsampwidth(first_params.sampwidth)
            wav_out.setframerate(first_params.framerate)
            wav_out.writeframes(combined_frames)

        return out_buf.getvalue()

    except Exception as e:
        logger.warning(f"Error during wave module stitching, falling back to pydub: {e}")
        try:
            from pydub import AudioSegment
            combined_segment = AudioSegment.empty()
            silence_segment = AudioSegment.silent(duration=int(pause_between_chunks_sec * 1000))

            for idx, wav_data in enumerate(wav_list):
                seg = AudioSegment.from_file(io.BytesIO(wav_data), format="wav")
                combined_segment += seg
                if idx < len(wav_list) - 1:
                    combined_segment += silence_segment

            out_buf = io.BytesIO()
            combined_segment.export(out_buf, format="wav")
            return out_buf.getvalue()
        except Exception as pydub_err:
            logger.error(f"Fallback stitching also failed: {pydub_err}")
            # If all fails, return first chunk as emergency fallback
            return wav_list[0]


def synthesize_text_to_speech(
    text: str,
    language_code: str = "en-IN",
    speaker: str = "shubh",
    model: str = "bulbul:v4-flash",
    pace: float = 1.0,
    api_key: Optional[str] = None,
    progress_callback=None,
) -> Dict[str, Any]:
    """
    Main speech generation entry point.
    Handles text chunking, sequential API queries, progress tracking, and audio assembly.
    
    Returns:
        Dict with keys:
            success (bool),
            audio_bytes (bytes),
            chunks_count (int),
            char_count (int),
            error (str or None)
    """
    clean_text = text.strip()
    if not clean_text:
        return {
            "success": False,
            "audio_bytes": None,
            "chunks_count": 0,
            "char_count": 0,
            "error": "Input text is empty. Please provide text or upload a document.",
        }

    # Split into chunks under the API limit
    chunks = split_text_into_chunks(clean_text, max_chars=MAX_CHARS_PER_REQUEST)
    total_chunks = len(chunks)

    wav_chunks: List[bytes] = []

    for idx, chunk in enumerate(chunks, 1):
        if progress_callback:
            progress_callback(
                current_chunk=idx,
                total_chunks=total_chunks,
                status=f"Synthesizing section {idx} of {total_chunks} ({len(chunk)} characters)...",
            )

        audio_bytes, err = _call_sarvam_tts_single_chunk(
            text=chunk,
            language_code=language_code,
            speaker=speaker,
            model=model,
            pace=pace,
            api_key=api_key,
        )

        if err or not audio_bytes:
            return {
                "success": False,
                "audio_bytes": None,
                "chunks_count": total_chunks,
                "char_count": len(clean_text),
                "error": f"Failed on section {idx}/{total_chunks}: {err}",
            }

        wav_chunks.append(audio_bytes)

    # Stitch all chunks together seamlessly
    if progress_callback and total_chunks > 1:
        progress_callback(
            current_chunk=total_chunks,
            total_chunks=total_chunks,
            status="Merging narrated audio segments into a seamless track...",
        )

    final_audio = stitch_wav_bytes(wav_chunks)

    return {
        "success": True,
        "audio_bytes": final_audio,
        "chunks_count": total_chunks,
        "char_count": len(clean_text),
        "error": None,
    }
