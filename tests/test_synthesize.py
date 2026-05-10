import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import numpy as np
from tts_plugin_kokoro.connector import KokoroConnector
from tts_plugin_bridge.protocol import TTSRequest


@pytest.mark.asyncio
async def test_synthesize_success():
    """Verify that synthesize returns a successful response with audio data."""
    connector = KokoroConnector()
    req = TTSRequest(text="Hello world", speed=1.0)

    # Mock for KPipeline - returns a generator of (graphemes, phonemes, audio)
    mock_pipeline = MagicMock()
    mock_pipeline.return_value = [
        ("Hello", "həˈloʊ", np.zeros(24000)),
        (" world", "wɜːld", np.zeros(24000)),
    ]

    with patch.object(KokoroConnector, "_get_pipeline", new_callable=AsyncMock) as mock_get_pipeline, \
         patch.object(connector, "_run_synthesis") as mock_run_synth, \
         patch.object(connector, "_numpy_to_wav") as mock_to_wav:

        mock_get_pipeline.return_value = mock_pipeline
        mock_run_synth.return_value = np.zeros(48000)
        mock_to_wav.return_value = b"fake_wav_data"

        resp = await connector.synthesize(req)

        assert resp.success is True
        assert resp.audio_data == b"fake_wav_data"
        mock_run_synth.assert_called_once()


@pytest.mark.asyncio
async def test_synthesize_invalid_voice():
    """Verify that synthesize returns a failure response when an invalid voice is used."""
    connector = KokoroConnector()
    req = TTSRequest(text="Hello", extra={"voice": "invalid_voice"})

    with patch.object(KokoroConnector, "_get_pipeline", new_callable=AsyncMock) as mock_get_pipeline, \
         patch.object(KokoroConnector, "_run_synthesis", side_effect=ValueError("Voice not found")):

        mock_get_pipeline.return_value = MagicMock()
        resp = await connector.synthesize(req)

        assert resp.success is False
        assert "Voice not found" in resp.error


@pytest.mark.asyncio
async def test_synthesize_import_error():
    """Verify that synthesize handles Kokoro package missing gracefully."""
    connector = KokoroConnector()
    req = TTSRequest(text="Hello")

    with patch.object(KokoroConnector, "_get_pipeline", side_effect=ImportError("Kokoro not installed")):
        resp = await connector.synthesize(req)

        assert resp.success is False
        assert "kokoro package not installed" in resp.error.lower()


@pytest.mark.asyncio
async def test_synthesize_empty_audio_chunks():
    """Verify that synthesize returns failure when no audio chunks are generated."""
    connector = KokoroConnector()
    # TTSRequest text must have at least 1 character. 
    # To test empty audio chunks, we synthesize a valid text but mock the pipeline to return nothing.
    req = TTSRequest(text="valid text", speed=1.0)

    mock_pipeline = MagicMock()
    mock_pipeline.return_value = []  # Empty generator

    with patch.object(KokoroConnector, "_get_pipeline", new_callable=AsyncMock, return_value=mock_pipeline):
        resp = await connector.synthesize(req)

        assert resp.success is False
        assert "No audio generated" in resp.error


@pytest.mark.asyncio
async def test_synthesize_with_all_params():
    """Verify that synthesize works with all parameters specified."""
    connector = KokoroConnector()
    req = TTSRequest(
        text="Test with all params",
        speed=1.5,
        extra={"voice": "custom_voice", "lang_code": "j"}
    )

    mock_pipeline = MagicMock()

    with patch.object(KokoroConnector, "_get_pipeline", new_callable=AsyncMock, return_value=mock_pipeline) as mock_get_pipeline, \
         patch.object(connector, "_run_synthesis", return_value=np.zeros(24000)), \
         patch.object(connector, "_numpy_to_wav", return_value=b"wav_data"):

        resp = await connector.synthesize(req)

        assert resp.success is True
        assert resp.audio_data == b"wav_data"
        mock_get_pipeline.assert_called_once_with("j")


@pytest.mark.asyncio
async def test_synthesize_file_not_found():
    """Verify that synthesize handles missing model file gracefully."""
    connector = KokoroConnector(model_path="nonexistent/path/model.pth")
    req = TTSRequest(text="Hello")

    with patch("shutil.which", return_value="/usr/bin/espeak-ng"), \
         patch("kokoro.KPipeline", side_effect=FileNotFoundError("Model not found")):
        resp = await connector.synthesize(req)

        assert resp.success is False
        # The connector catches FileNotFoundError and returns its message directly.
        # But wait, in _get_pipeline it might be wrapped in RuntimeError if KPipeline init fails.
        # Let's check the implementation.
        assert "Model not found" in resp.error


@pytest.mark.asyncio
async def test_synthesize_soundfile_error():
    """Verify that synthesize handles soundfile conversion error gracefully."""
    connector = KokoroConnector()
    req = TTSRequest(text="Hello")

    mock_pipeline = MagicMock()

    with patch.object(KokoroConnector, "_get_pipeline", new_callable=AsyncMock, return_value=mock_pipeline), \
         patch.object(connector, "_run_synthesis", return_value=np.zeros(24000)), \
         patch.object(connector, "_numpy_to_wav", side_effect=RuntimeError("Soundfile error")):

        resp = await connector.synthesize(req)

        assert resp.success is False
        assert "Soundfile error" in resp.error or "Unexpected error" in resp.error
