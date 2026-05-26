import pytest
import numpy as np
from tts_plugin_kokoro.connector import KokoroConnector
from tts_plugin_bridge.protocol import TTSRequest
import soundfile as sf
import io


@pytest.mark.asyncio
async def test_synthesize_integration():
    """Verify synthesis with the real Kokoro model."""
    # Note: This test requires model files to be present in repos/tts-plugin-kokoro/models/
    # If models are missing, this test is expected to fail (is_available will be False)
    connector = KokoroConnector()

    if not await connector.is_available():
        pytest.skip(
            "Kokoro model files or espeak-ng not found. Skipping integration test."
        )

    req = TTSRequest(text="This is a test of the Kokoro TTS integration.", speed=1.0)
    resp = await connector.synthesize(req)

    assert resp.success is True
    assert resp.audio_data is not None

    # Verify that the audio data is a valid WAV file
    with io.BytesIO(resp.audio_data) as buf:
        data, samplerate = sf.read(buf)
        assert samplerate == 24000
        assert len(data) > 0
        assert isinstance(data, np.ndarray)
