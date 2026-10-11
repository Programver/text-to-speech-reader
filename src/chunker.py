"""
Smart text chunking module for natural-sounding TTS synthesis.
Respects sentence boundaries, punctuation, and character limits.
"""

import re
from typing import List

# Sentence ending punctuation across English and Indian scripts
SENTENCE_ENDINGS = r'(?<=[.!?।\n])\s+'


def split_text_into_chunks(text: str, max_chars: int = 1800) -> List[str]:
    """
    Splits long text into manageable chunks respecting sentence and paragraph boundaries.
    
    Args:
        text: Input text string
        max_chars: Maximum characters allowed per chunk (default 1800, well within Sarvam's 2500 limit)
        
    Returns:
        List of clean text chunks.
    """
    clean_text = text.strip()
    if not clean_text:
        return []

    if len(clean_text) <= max_chars:
        return [clean_text]

    # Split first by paragraphs
    paragraphs = [p.strip() for p in re.split(r'\n{2,}', clean_text) if p.strip()]
    
    chunks: List[str] = []
    current_chunk = ""

    for paragraph in paragraphs:
        # If paragraph alone fits within remaining space in current chunk
        candidate = f"{current_chunk}\n\n{paragraph}".strip() if current_chunk else paragraph
        if len(candidate) <= max_chars:
            current_chunk = candidate
            continue

        # If current chunk has content and paragraph doesn't fit, flush current chunk
        if current_chunk:
            chunks.append(current_chunk)
            current_chunk = ""

        # If paragraph itself fits in a fresh chunk
        if len(paragraph) <= max_chars:
            current_chunk = paragraph
            continue

        # Paragraph is too long: split into sentences
        sentences = [s.strip() for s in re.split(SENTENCE_ENDINGS, paragraph) if s.strip()]
        
        for sentence in sentences:
            candidate = f"{current_chunk} {sentence}".strip() if current_chunk else sentence
            if len(candidate) <= max_chars:
                current_chunk = candidate
                continue

            # Flush current chunk if it has text
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""

            # If sentence itself is still longer than max_chars (rare run-on sentence), split by commas or words
            if len(sentence) > max_chars:
                sub_parts = _split_long_sentence(sentence, max_chars)
                for part in sub_parts:
                    if len(f"{current_chunk} {part}".strip()) <= max_chars:
                        current_chunk = f"{current_chunk} {part}".strip() if current_chunk else part
                    else:
                        if current_chunk:
                            chunks.append(current_chunk)
                        current_chunk = part
            else:
                current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def _split_long_sentence(sentence: str, max_chars: int) -> List[str]:
    """Fallback splitting for sentences that exceed max_chars on clause or word boundaries."""
    # Try splitting on clause punctuation: comma, semicolon, dash
    clause_splits = [c.strip() for c in re.split(r'(?<=[,;:\-—])\s+', sentence) if c.strip()]
    parts: List[str] = []
    cur = ""

    for clause in clause_splits:
        cand = f"{cur} {clause}".strip() if cur else clause
        if len(cand) <= max_chars:
            cur = cand
        else:
            if cur:
                parts.append(cur)
                cur = ""
            if len(clause) <= max_chars:
                cur = clause
            else:
                # Word-level chunking
                words = clause.split()
                w_cur = ""
                for word in words:
                    w_cand = f"{w_cur} {word}".strip() if w_cur else word
                    if len(w_cand) <= max_chars:
                        w_cur = w_cand
                    else:
                        if w_cur:
                            parts.append(w_cur)
                        w_cur = word
                if w_cur:
                    cur = w_cur

    if cur:
        parts.append(cur)

    return parts
