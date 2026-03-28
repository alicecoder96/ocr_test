import io

import streamlit as st
from PIL import Image
from google import genai
from google.genai import types

# 利用可能なモデル定義: (モデルID, セレクトボックス表示名)
MODELS = [
    ("gemini-2.5-flash", "gemini-2.5-flash　⭐⭐⭐⭐　速い・高精度（推奨）"),
    ("gemini-2.5-pro",   "gemini-2.5-pro　　⭐⭐⭐⭐⭐　最高精度・低速"),
    ("gemini-2.0-flash-lite", "gemini-2.0-flash-lite　⭐⭐⭐　最速・標準精度"),
]


def extract_text(image: Image.Image, api_key: str, model: str) -> str:
    """
    入力: 画像 (PIL.Image)、Gemini API キー (str)、モデル名 (str)
    出力: 抽出テキスト文字列（文字未検出時は空文字列）
    例外: 接続エラー時は RuntimeError を raise
    """
    client = genai.Client(api_key=api_key)

    buf = io.BytesIO()
    image.save(buf, format="PNG")
    image_bytes = buf.getvalue()

    try:
        response = client.models.generate_content(
            model=model,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
                "この画像に含まれるテキストをすべて抽出してください。テキストのみを返し、説明は不要です。テキストがない場合は何も返さないでください。",
            ],
        )
        result = response.text.strip() if response.text else ""
        return result
    except Exception as e:
        raise RuntimeError(f"Gemini API エラー: {e}") from e


def get_api_key() -> str:
    """Streamlit secrets から API キーを取得する。未設定時は RuntimeError を raise。"""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        raise RuntimeError(
            "GEMINI_API_KEY が設定されていません。\n"
            "ローカル: .streamlit/secrets.toml に GEMINI_API_KEY = \"your_key\" を追加してください。\n"
            "Streamlit Community Cloud: アプリの Settings > Secrets に追加してください。"
        )
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY が空です。有効な API キーを設定してください。")
    return api_key
