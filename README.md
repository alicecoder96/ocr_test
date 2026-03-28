# OCR アプリ

カメラで撮影した画像からテキストを抽出する Streamlit 製 Web アプリです。
OpenCV で画像を前処理し、Gemini Flash で文字認識を行います。
元画像・前処理済み画像それぞれの認識結果を並べて確認できます。

## セットアップ

```bash
uv venv --python 3.11
source .venv/bin/activate
uv pip install -r requirements.txt
```

## API キーの設定（ローカル）

`.streamlit/secrets.toml.example` をコピーして API キーを設定します：

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

`.streamlit/secrets.toml` を編集：

```toml
GEMINI_API_KEY = "your_key_here"
```

## 起動

```bash
streamlit run app.py
```

## Streamlit Community Cloud へのデプロイ

1. このリポジトリを GitHub に push する
2. [share.streamlit.io](https://share.streamlit.io) でアプリを作成し、リポジトリを連携する
3. アプリの **Settings > Secrets** に以下を追加する：

```toml
GEMINI_API_KEY = "your_key_here"
```

4. デプロイを実行する
