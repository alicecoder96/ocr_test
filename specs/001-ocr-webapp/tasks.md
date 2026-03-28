# Tasks: OCR Web Application

**Input**: Design documents from `/specs/001-ocr-webapp/`
**Prerequisites**: plan.md ✅, spec.md ✅

---

## Phase 1: Setup（プロジェクト初期化）

**Purpose**: 依存関係の定義とプロジェクト構造の作成

- [x] T001 `requirements.txt` を作成する（streamlit, opencv-python, google-generativeai, Pillow）
- [x] T002 [P] `.env.example` を作成する（`GEMINI_API_KEY=your_key_here`）
- [x] T003 [P] `app.py`・`preprocessing.py`・`ocr.py` の空ファイルを作成する

---

## Phase 2: Foundational（共通基盤）

**Purpose**: 全ユーザーストーリーで使われる共通処理の実装

**⚠️ CRITICAL**: このフェーズ完了まで US1・US2 の実装は開始しない

- [x] T004 ~~`preprocessing.py` に `preprocess(image: np.ndarray) -> np.ndarray` を実装する~~ （前処理廃止により不要）
- [x] T005 `ocr.py` に `extract_text(image: np.ndarray, api_key: str) -> str` を実装する（Gemini Flash multimodal 呼び出し・文字未検出時は空文字列・接続エラー時は RuntimeError）
- [x] T006 `ocr.py` に `st.secrets` から `GEMINI_API_KEY` を読み込む処理と未設定時のエラーメッセージを実装する

**Checkpoint**: `preprocessing.py` と `ocr.py` が単独で動作確認できる状態

---

## Phase 3: User Story 1 - カメラで撮影して文字を抽出する (Priority: P1) 🎯 MVP

**Goal**: カメラ撮影 → 前処理 → Gemini OCR → 結果表示の一連フローを完成させる

**Independent Test**: アプリを起動し、カメラで文字を撮影すると認識テキストが表示されることを確認する

### Implementation for User Story 1

- [x] T007 [US1] `app.py` に Streamlit ページ基本設定（タイトル・レイアウト）を実装する
- [x] T008 [US1] `app.py` に `st.camera_input()` によるカメラ入力 UI を実装する
- [x] T009 [US1] `app.py` に撮影画像を `numpy.ndarray` に変換する処理を実装する（PIL → OpenCV 変換）
- [x] T010 [US1] `app.py` に `preprocess()` → `extract_text()` の呼び出しフローを実装する
- [x] T011 [US1] `app.py` に処理中スピナー（`st.spinner()`）を実装する
- [x] T012 [US1] `app.py` に OCR 結果テキストの表示（`st.code()`）を実装する
- [x] T013 [US1] `app.py` に文字未検出時・エラー発生時のメッセージ表示を実装する
- [x] T014 [US1] `app.py` にカメラ非対応デバイス・権限拒否時のエラーハンドリングを実装する

**Checkpoint**: US1 が独立して動作確認できる。撮影 → テキスト表示の一連フローが機能する

---

## Phase 4: User Story 2 - 抽出テキストをコピーする (Priority: P2)

**Goal**: OCR 結果をワンクリックでクリップボードにコピーできるようにする

**Independent Test**: OCR 結果が表示された状態でコピーボタンを押すとクリップボードに内容が入ることを確認する

### Implementation for User Story 2

- [x] T015 [US2] `app.py` の結果表示部分を `st.code(result, language=None)` に変更してコピーアイコンを有効化する（T012 を更新）

**Checkpoint**: US1・US2 が両方独立して動作確認できる

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: 品質・使いやすさの向上

- [x] T016 [P] `README.md` を作成する（セットアップ手順・`GEMINI_API_KEY` の設定方法・起動コマンド・Streamlit Community Cloud デプロイ手順）
- [x] T017 `app.py` の UI テキストを日本語で統一する（ラベル・エラーメッセージ）
- [ ] T018 [P] `requirements.txt` のバージョンを固定する（`pip freeze` ベース）

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 依存なし・即開始可能
- **Foundational (Phase 2)**: Phase 1 完了後・US1/US2 をブロック
- **US1 (Phase 3)**: Phase 2 完了後に開始
- **US2 (Phase 4)**: Phase 3 完了後（T012 を更新するため）
- **Polish (Phase 5)**: 全 US 完了後

### Parallel Opportunities

```bash
# Phase 1 内で並列実行可能:
T002: .env.example 作成
T003: 空ファイル作成

# Phase 2 内は順次実行（T004 → T005 → T006）

# Phase 5 内で並列実行可能:
T016: README 作成
T018: requirements.txt バージョン固定
```

---

## Implementation Strategy

### MVP First（US1 のみ）

1. Phase 1: Setup 完了
2. Phase 2: Foundational 完了（CRITICAL）
3. Phase 3: US1 完了
4. **STOP & VALIDATE**: カメラ撮影 → OCR 結果表示を手動確認
5. 動作確認後 US2 へ

### Incremental Delivery

1. Setup + Foundational → 基盤完成
2. US1 完了 → **MVP デモ可能**
3. US2 完了 → コピー機能追加
4. Polish → リリース準備完了

---

## Notes

- [P] = 異なるファイルを扱い、依存関係のないタスク（並列実行可能）
- [USn] = 対応するユーザーストーリー
- T015 は T012 の更新タスク（`st.text_area` → `st.code` への変更）
- `st.camera_input()` は Streamlit 1.18+ が必要
