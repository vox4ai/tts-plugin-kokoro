import pytest
from unittest.mock import patch, MagicMock
from tts_plugin_kokoro.connector import KokoroConnector


@pytest.mark.asyncio
async def test_is_available_all_present():
    """Verify that is_available returns True when all dependencies are present."""
    connector = KokoroConnector()
    with patch("shutil.which", return_value="/usr/bin/espeak-ng"), \
         patch("pathlib.Path.exists", return_value=True):
        assert await connector.is_available() is True


@pytest.mark.asyncio
async def test_is_available_missing_espeak():
    """Verify that is_available returns False when espeak-ng is missing."""
    connector = KokoroConnector()
    with patch("shutil.which", return_value=None), \
         patch("pathlib.Path.exists", return_value=True):
        assert await connector.is_available() is False


@pytest.mark.asyncio
async def test_is_available_missing_model():
    """Verify that is_available returns False when model file is missing."""
    connector = KokoroConnector()
    with patch("shutil.which", return_value="/usr/bin/espeak-ng"), \
         patch("pathlib.Path.exists", return_value=False):
        assert await connector.is_available() is False


@pytest.mark.asyncio
async def test_get_pipeline_cache():
    """Verify that pipeline caching works correctly."""
    connector = KokoroConnector()
    with patch("kokoro.KPipeline") as mock_kp:
        mock_kp.return_value = MagicMock()

        p1 = await connector._get_pipeline("a")
        p2 = await connector._get_pipeline("a")

        assert p1 is p2  # Same instance
        mock_kp.assert_called_once_with(lang_code="a", model=str(connector.model_path))


@pytest.mark.asyncio
async def test_get_pipeline_different_lang():
    """Verify that different lang codes create different pipelines."""
    connector = KokoroConnector()
    with patch("kokoro.KPipeline") as mock_kp:
        mock_kp.side_effect = [MagicMock(), MagicMock()]

        p1 = await connector._get_pipeline("a")
        p2 = await connector._get_pipeline("j")

        assert p1 is not p2
        assert mock_kp.call_count == 2


@pytest.mark.asyncio
async def test_get_pipeline_init_failure():
    """Verify that KPipeline initialization failure raises RuntimeError."""
    connector = KokoroConnector()
    with patch("kokoro.KPipeline", side_effect=RuntimeError("Model load failed")):
        with pytest.raises(RuntimeError, match="Failed to initialize KPipeline"):
            await connector._get_pipeline("a")


@pytest.mark.asyncio
async def test_get_pipeline_import_error():
    """Verify that missing kokoro package raises ImportError."""
    connector = KokoroConnector()
    with patch("kokoro.KPipeline", side_effect=ImportError("kokoro not installed")):
        with pytest.raises(ImportError, match="kokoro package not installed"):
            await connector._get_pipeline("a")


@pytest.mark.asyncio
async def test_close_clears_pipelines():
    """Verify that close() clears all loaded pipelines."""
    connector = KokoroConnector()
    with patch("kokoro.KPipeline") as mock_kp:
        mock_kp.return_value = MagicMock()

        await connector._get_pipeline("a")
        assert len(connector._pipelines) == 1

        await connector.close()
        assert len(connector._pipelines) == 0
