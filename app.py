import streamlit as st
from PIL import Image

from ocr import extract_text, get_api_key

st.set_page_config(page_title="OCR アプリ", layout="centered")
st.title("OCR アプリ")
st.caption("カメラで撮影した画像からテキストを抽出します")

# API キーの確認
try:
    api_key = get_api_key()
except RuntimeError as e:
    st.error(str(e))
    st.stop()

# カメラ入力
image_data = st.camera_input("カメラで撮影してください")

if image_data is not None:
    pil_image = Image.open(image_data)

    with st.spinner("テキストを抽出中..."):
        try:
            result = extract_text(pil_image, api_key)
        except RuntimeError as e:
            st.error(f"エラーが発生しました: {e}")
            st.stop()

    if result:
        st.subheader("抽出結果")
        st.code(result, language=None)
    else:
        st.info("テキストが検出されませんでした。文字が写るように撮影してください。")
