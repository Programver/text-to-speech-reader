"""
Unit tests for text chunker.
"""

from src.chunker import split_text_into_chunks


def test_short_text():
    text = "Hello world! This is a simple test sentence."
    chunks = split_text_into_chunks(text, max_chars=100)
    assert len(chunks) == 1
    assert chunks[0] == text
    print("✓ test_short_text passed")


def test_empty_text():
    chunks = split_text_into_chunks("", max_chars=100)
    assert chunks == []
    print("✓ test_empty_text passed")


def test_long_text_split():
    sentences = [
        f"This is sentence number {i} providing valuable narration content for testing the audio chunker."
        for i in range(1, 40)
    ]
    long_text = " ".join(sentences)
    chunks = split_text_into_chunks(long_text, max_chars=500)
    
    assert len(chunks) > 1
    for c in chunks:
        assert len(c) <= 500
    
    # Verify no content lost
    rejoined = " ".join(chunks)
    assert "sentence number 1" in rejoined
    assert "sentence number 39" in rejoined
    print(f"✓ test_long_text_split passed ({len(chunks)} chunks formed)")


def test_multilingual_full_stops():
    hindi_text = "यह पहला वाक्य है। यह दूसरा वाक्य है, जो काफी महत्वपूर्ण है। यह तीसरा वाक्य है।"
    chunks = split_text_into_chunks(hindi_text, max_chars=40)
    assert len(chunks) >= 2
    for c in chunks:
        assert len(c) <= 40
    print(f"✓ test_multilingual_full_stops passed ({len(chunks)} chunks formed)")


if __name__ == "__main__":
    test_short_text()
    test_empty_text()
    test_long_text_split()
    test_multilingual_full_stops()
    print("All chunker unit tests passed!")
