import streamlit as st
from PIL import Image

from ocr import extract_text, get_api_key

st.set_page_config(page_title="OCR アプリ", layout="centered")

# --- 認証 ---

def check_credentials(username: str, password: str) -> bool:
    try:
        return (
            username == st.secrets["AUTH_USERNAME"]
            and password == st.secrets["AUTH_PASSWORD"]
        )
    except KeyError:
        st.error("認証情報が設定されていません。secrets.toml に AUTH_USERNAME・AUTH_PASSWORD を追加してください。")
        return False

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("ログイン")
    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")
    if st.button("ログイン"):
        if check_credentials(username, password):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("ユーザー名またはパスワードが正しくありません")
    st.stop()

# --- OCR アプリ本体（認証済みのみ表示） ---

st.title("OCR アプリ")
st.caption("カメラで撮影した画像からテキストを抽出します")

if st.button("ログアウト"):
    st.session_state.logged_in = False
    st.rerun()

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
