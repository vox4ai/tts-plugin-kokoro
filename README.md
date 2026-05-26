# tts-plugin-kokoro

<p align="center">
  <img src="https://via.placeholder.com/1200x400/1a1a1a/ffffff?text=tts-plugin-kokoro" alt="tts-plugin-kokoro Banner" width="1200">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/pypi-latest-blue.svg" alt="PyPI version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.10%2B-yellow.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/maintained%3F-yes-brightgreen.svg" alt="Maintained">
</p>

<p align="center">
  <a href="https://github.com/vox4ai/tts-plugin-kokoro">Website</a> •
  <a href="https://github.com/vox4ai/tts-plugin-kokoro/issues">Report Bug</a> •
  <a href="https://github.com/vox4ai/tts-plugin-kokoro/contributing">Contributing</a>
</p>

---

## 🚀 Overview

Kokoro-TTS Engine Connector for `tts-plugin-bridge`.

This plugin allows the bridge to use the Kokoro-82M model for high-quality, lightweight local speech synthesis.

## 📦 Installation

### 1. System Dependencies
Kokoro requires `espeak-ng` for phonemization.

- **Ubuntu/Debian**: `sudo apt-get install espeak-ng`
- **macOS**: `brew install espeak-ng`
- **Windows**: Download the `.msi` from [espeak-ng releases](https://github.com/espeak-ng/espeak-ng/releases).

### 2. Python Setup
```bash
cd repos/tts-plugin-kokoro
uv sync
```

### 3. Model Setup
The model files are not included in the repository. Run the provided download script to fetch them from Hugging Face:

```bash
uv run python scripts/download_models.py
```

This will download `kokoro-v1_0.pth` and other necessary files into the `models/` directory.

## 🛠 Usage

The connector is automatically discovered via `entry_points`. You can specify the following parameters in the `TTSRequest`:

- `voice` (extra): The voice ID to use (e.g., `af_heart`). Defaults to `af_heart`.
- `speed` (float): The speech rate.
- `lang_code` (extra): The language code (e.g., `a` for American English, `j` for Japanese). Defaults to `a`.

## 🔍 Testing

Run the tests using `pytest`:

```bash
uv run pytest
```

## 📜 License

MIT License
