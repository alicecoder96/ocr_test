# Implementation Plan: OCR Web Application

**Branch**: `001-ocr-webapp` | **Date**: 2026-03-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ocr-webapp/spec.md`

## Summary

ブラウザ上でカメラを起動して撮影し、撮影した画像を直接 Gemini Flash に渡して
文字テキストを抽出・表示する Streamlit 製 OCR Web アプリを実装する。
ログインフォームで認証済みユーザーのみアクセスを許可し、API の不正利用を防ぐ。
ユーザーは抽出テキストをコピーして利用できる。

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit, Google Generative AI SDK (`google-genai`), Pillow
**Storage**: N/A（セッション内メモリのみ、永続化なし）
**Testing**: pytest
**Target Platform**: ブラウザ（デスクトップ・モバイル対応）/ ローカル実行
**Project Type**: web-app（Streamlit シングルページアプリ）
**Performance Goals**: 撮影から OCR 結果表示まで 60 秒以内
**Constraints**: GEMINI_API_KEY・認証情報は Streamlit secrets（`st.secrets`）で管理・インターネット接続必須
**Deploy Target**: Streamlit Community Cloud
**Scale/Scope**: シングルユーザー想定（同時利用者数の上限なし）

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| 原則 | チェック | 備考 |
|------|---------|------|
| I. OpenCV-First Preprocessing | ✅ | 前処理関数を独立実装し Gemini 前に必ず適用 |
| II. Gemini Flash による文字認識 | ✅ | `gemini-1.5-flash` 使用・APIキーは環境変数 |
| III. Streamlit Web UI | ✅ | Streamlit のみ・追加フレームワークなし |
| IV. シンプルさ優先（YAGNI） | ✅ | `app.py` 1ファイル中心・不要な分割なし |
| V. 環境再現性 | ✅ | `requirements.txt` で依存管理 |

**判定**: 全原則パス。Phase 0 に進む。

## Project Structure

### Documentation (this feature)

```text
specs/001-ocr-webapp/
├── plan.md        # このファイル
├── research.md    # Phase 0 output
├── data-model.md  # Phase 1 output
├── quickstart.md  # Phase 1 output
└── tasks.md       # /speckit.tasks output
```

### Source Code (repository root)

```text
app.py                  # Streamlit アプリ エントリポイント
preprocessing.py        # OpenCV 前処理関数
ocr.py                  # Gemini Flash OCR 関数
requirements.txt        # 依存ライブラリ
.env.example            # 環境変数サンプル
```

**Structure Decision**: Streamlit アプリは `app.py` 1ファイルで UI を担い、
`preprocessing.py` と `ocr.py` に処理を分離して独立テスト可能にする。
Constitution IV（シンプルさ優先）に従い、src/ ディレクトリ階層は作らない。

## Complexity Tracking

> 構成原則違反なし。このセクションは該当なし。

---

## Phase 0: Research

### カメラ入力（Streamlit）

- **Decision**: `st.camera_input()` を使用する
- **Rationale**: Streamlit 1.18+ に標準搭載。ブラウザのカメラ API をラップし、
  撮影した静止画を `PIL.Image` / バイト列で返す。追加ライブラリ不要。
- **Alternatives considered**: `streamlit-webrtc`（リアルタイム映像向け、過剰）

### OpenCV 前処理パイプライン

- **Decision**: グレースケール変換 → CLAHE（コントラスト強調） → 適応的二値化（Otsu 法）
- **Rationale**: 照明ムラや低コントラストに強く、印刷文字・手書き文字の両方に有効。
  各ステップを独立関数として実装し `preprocessing.py` にまとめる。
- **Alternatives considered**: 固定閾値二値化（照明条件依存で精度不安定）

### Gemini Flash OCR

- **Decision**: `google-generativeai` SDK で `gemini-1.5-flash` を呼び出し、
  前処理済み画像を base64 エンコードして multimodal プロンプトに渡す。
- **Rationale**: 高速・低コスト・高精度。独自モデル訓練不要。
- **Alternatives considered**: Gemini Pro（低速・高コスト）、Tesseract（精度低）

### 認証

- **Decision**: `st.session_state` でログイン状態を管理するシンプルなログインフォームを `app.py` に実装する。認証情報（ユーザー名・パスワード）は `st.secrets["AUTH_USERNAME"]` / `st.secrets["AUTH_PASSWORD"]` で管理する。
- **Rationale**: 追加ライブラリ不要。`st.secrets` はソースコードに含まれないため GitHub public リポジトリでも安全。
- **Alternatives considered**: `streamlit-authenticator` ライブラリ（設定が複雑、YAGNI に反する）

### テキストコピー

- **Decision**: Streamlit の `st.code()` + `st.button()` + `pyperclip` は不要。
  `st.text_area()` で表示し、ユーザーが標準のブラウザコピー操作で対応。
  または `st.code(result, language=None)` のコードブロック（コピーアイコン付き）を利用。
- **Rationale**: 追加ライブラリなしで実現可能。Constitution IV に準拠。

---

## Phase 1: Design & Contracts

### data-model.md 相当（インラインに記載）

| エンティティ | 型 | 説明 |
|------------|-----|------|
| `raw_image` | `numpy.ndarray` | カメラ撮影画像（BGR） |
| `preprocessed_image` | `numpy.ndarray` | OpenCV 前処理後画像（グレースケール） |
| `ocr_result` | `str` | Gemini が返すテキスト文字列 |

### インターフェース契約

#### `preprocessing.py`

```python
def preprocess(image: numpy.ndarray) -> numpy.ndarray:
    """
    入力: BGR カラー画像
    出力: 前処理済みグレースケール画像
    処理: グレースケール変換 → CLAHE → Otsu 二値化
    """
```

#### `ocr.py`

```python
def extract_text(image: numpy.ndarray, api_key: str) -> str:
    """
    入力: 前処理済み画像、Gemini API キー
    出力: 抽出テキスト文字列（文字未検出時は空文字列）
    例外: 接続エラー時は RuntimeError を raise
    """
```

### エージェントコンテキスト更新

`.claude/` コンテキストを更新して技術スタックを反映する。

---

## Constitution Check（Phase 1 後再評価）

全原則引き続きパス。設計変更による違反なし。
