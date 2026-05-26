# tts-plugin-kokoro

Kokoro-TTS Engine Connector for `tts-plugin-bridge`.

## 🛠 概要
- **役割**: Kokoro-82M モデルを使用した高品質かつ軽量なローカル音声合成を `tts-plugin-bridge` に提供する。
- **主要機能**:
    - 完全オフラインでの音声合成。
    - 複数の音声モデル（voice）と言語（lang_code）のサポート。

## ⚙️ 前提条件
- **espeak-ng** (phonemization 用) がインストールされていること。
- **Kokoro モデルファイル** が `models/` ディレクトリに配置されていること。

## 🚀 開発・実行
- **パッケージ管理**: `uv`
- **テスト**: `pytest`

## 🔗 関連リポジトリ
- `repos/tts-plugin-bridge`: コアフレームワーク
