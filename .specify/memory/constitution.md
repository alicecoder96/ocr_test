<!--
Sync Impact Report
Version change: N/A → 1.0.0 (initial ratification)
Added sections: Core Principles, Tech Stack, Development Workflow, Governance
Modified principles: N/A (initial)
Removed sections: N/A (initial)
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ no changes needed (generic)
  - .specify/templates/spec-template.md ✅ no changes needed (generic)
  - .specify/templates/tasks-template.md ✅ no changes needed (generic)
Follow-up TODOs: none
-->

# OCR Constitution

## Core Principles

### I. OpenCV-First Preprocessing

画像認識の精度を最大化するため、Gemini Flash へ渡す前に必ず OpenCV で前処理を行う。
前処理には最低限グレースケール変換・ノイズ除去・二値化を含む。
前処理パイプラインは独立した関数として実装し、単体で検証可能であること。

### II. Gemini Flash による文字認識

文字認識には必ず Gemini Flash（`gemini-1.5-flash` 系）を使用する。
独自 OCR モデルの訓練・組み込みは行わない。
API キーは環境変数（`GEMINI_API_KEY`）で管理し、コードにハードコードしてはならない。

### III. Streamlit Web UI

フロントエンドは Streamlit のみで実装する。追加の Web フレームワーク（FastAPI、Flask 等）は不要な複雑性を招くため導入しない。
ユーザーは画像をアップロードし、前処理プレビューと OCR 結果をブラウザ上で確認できること。

### IV. シンプルさ優先（YAGNI）

現時点で必要な機能のみ実装する。バッチ処理・ユーザー認証・データ永続化は明示的に要求されるまで実装しない。
1 ファイルで動作する構成を目指し、不要なモジュール分割は避ける。

### V. 環境再現性

依存ライブラリは `requirements.txt` で管理する。
Python バージョンは 3.11 以上を前提とする。

## Tech Stack

| レイヤー       | 技術                        |
|--------------|---------------------------|
| UI           | Streamlit                 |
| 画像前処理      | OpenCV (`opencv-python`)  |
| 文字認識       | Gemini Flash (Google AI)  |
| 言語          | Python 3.11+              |
| 依存管理       | pip + requirements.txt    |

## Development Workflow

- 実装前に仕様（spec.md）と計画（plan.md）を確認する。
- 前処理関数とGemini呼び出し関数は分離し、それぞれ独立して動作確認できること。
- Streamlit アプリのエントリポイントは `app.py` とする。
- 環境変数が未設定の場合は明確なエラーメッセージを表示する。

## Governance

このコンスティチューションはすべての実装判断の基準となる。
原則に反する実装を行う場合は、理由を plan.md の Complexity Tracking に記録する。
修正は MAJOR/MINOR/PATCH のセマンティックバージョニングに従い、改定日を更新する。

**Version**: 1.0.0 | **Ratified**: 2026-03-29 | **Last Amended**: 2026-03-29
