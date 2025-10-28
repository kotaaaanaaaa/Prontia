# Prontia エージェント仕様 / 運用ガイド

**Prontia** は、React / TypeScript フロントエンドと FastAPI バックエンドを持つチャットアプリケーションで、Azure OpenAI と Cosmos DB に統合されています。

## アーキテクチャ概要

* `frontend/` - React + Vite + Material-UI を利用したチャットインターフェース
* `backend/` - 非同期 Azure 連携を備えた FastAPI サービス

```
root/
├─ backend/
│ └─ src/prontia/
│   ├─ api/ # FastAPI ルーター（DTOに変換して返す）
│   ├─ core/ # 設定・ロギング等（settings.py 等）
│   ├─ db/ # Cosmos DB 非同期操作
│   ├─ dto/ # API DTO
│   ├─ models/ # ドメインモデル
│   ├─ services/ # ドメインロジック（OpenAI/Cosmosをオーケストレート）
│   └─ app.py # エントリポイント
└─ frontend/
  └─ src/
    └─ App.tsx
```

## 主要コンポーネントとパターン

### バックエンドアーキテクチャ（Python / FastAPI）

* **エントリーポイント**: `backend/src/prontia/app.py`
* **API レイヤー**: `backend/src/prontia/api/*.py`
* **サービスレイヤー**: `backend/src/prontia/services/*.py`
* **データレイヤー**: `backend/src/prontia/db/*.py`

**重要なパターン**:
サービス関数はドメインモデルを返し、API エンドポイントがそれを DTO に変換します。

```python
# サービス層はモデルを返す
msg = await service.start_conversation(owner_id=owner_id, content=req.content)
# API 層で DTO レスポンスに変換
res = MessageResponse(id=msg.id, conversation_id=msg.conversation_id, ...)
```

### Azure 連携

* **OpenAI**: `backend/src/prontia/services/openai.py` 会話履歴（直近N件）+ システムプロンプトを用いて Azure OpenAI と通信
* **Cosmos DB**: `owner_id`  単位でパーティション化された自動コンテナ作成付き非同期操作
* **設定管理**: `backend/src/prontia/core/settings.py` 環境変数ベースの設定（接頭辞・型バリデーション込み）

### フロントエンドアーキテクチャ（React / TypeScript）

* **レイアウト**:
  `App.tsx` → `SideMenu` + `MainContents` → `Chat` → (`ChatConversation` + `ChatInput`)
* **テーマ**: 各コンポーネントごとに Material-UI の ThemeProvider をカスタマイズ
* **テスト**: Vitest + React Testing Library（主要コンポーネントのユニット/スナップショット）

## 開発ワークフロー

### バックエンド開発

```bash
cd backend
# 依存の同期
uv sync
# 依存の同期（開発用追加パッケージ）
uv sync --extra dev
# 非同期テストを実行
uv run pytest tests/ -v
# サーバー起動
uv run python -m prontia
```

### フロントエンド開発

```bash
cd frontend
# 依存関係のインストール
npm install
# 開発サーバー起動
npm run dev
# フォーマットとリンティング（Biome + ESLint）
npm run lint
```

### テストパターン

* **バックエンド**: `pytest-asyncio`, `pytest-mock` による非同期サービスのテスト
* **モックパターン**: 統合境界（`cosmosdb.*`, `openai.*`）でモックを適用
* **共通テストデータ**: `backend/tests/test_const.py` 等で集約

例:

```python
@pytest.mark.asyncio
async def test_service_function(mocker: Mocker) -> None:
    m = mocker.patch("prontia.db.cosmosdb.operation")
    result = await target.service_function(params)
    # モック呼び出しと結果を検証
```

## プロジェクト固有の規約

### UUID 生成

* 時系列順にソート可能な UUID を生成するため、`uuid6.uuid7()` を採用
* 会話やメッセージなど全てのエンティティ ID に uuid7 を使用

### メッセージフロー

1. ユーザーがメッセージを送信 → API が会話とユーザーメッセージを作成
2. サービスが Azure OpenAI に会話履歴を送信
3. AI の応答をアシスタントメッセージとして保存
4. 両方のメッセージをフロントエンドへ返却

### 環境変数設定

`.env` （ローカル開発用。secretsはコミットしない）

```
OPENAI_ENDPOINT=https://your-openai.openai.azure.com/
OPENAI_DEPLOYMENT=gpt-4o-mini
OPENAI_APIKEY=your-key
COSMOSDB_ENDPOINT=https://your-cosmos.documents.azure.com:443/
COSMOSDB_ACCOUNTKEY=your-key
COSMOSDB_DATABASE=prontia
```

### コード品質

* **フロントエンド**: Biome フォーマッタ + ESLint
* **バックエンド**: Ruff によるリンティング + MyPy による型チェック
* **Git フック**: lint-staged によるコミット時の自動フォーマット

## アプリケーション概要

- エージェントは「ユーザーのメッセージに応答するアシスタント」として動作します。
- 会話履歴（直近N件）を文脈として Azure OpenAI に送信し、応答を生成します。
- 生成された応答は Cosmos DB にメッセージ（assistant 役割）として保存され、API レスポンスにも含めて返します。
- 設定は環境変数経由で `backend/src/prontia/core/settings.py` に集約されています。

関連実装の起点:
- API: `backend/src/prontia/api/*.py`
- サービス: `backend/src/prontia/services/*.py`
- OpenAI 連携: `backend/src/prontia/services/openai.py`
- モデル/DTO: `backend/src/prontia/models/*`, `backend/src/prontia/dto/*`
- データアクセス: `backend/src/prontia/db/*.py`

### チャット機能

- 目的: 一般的なチャット応答。
- 入力: ユーザーのメッセージ、会話 ID（新規の場合は作成）。
- 出力: assistant 応答メッセージ。
- 文脈: 同一会話の直近N件（user/assistant）+ システムプロンプト。
- モデル/デプロイ: `OPENAI_DEPLOYMENT`（例: `gpt-4o-mini` など）を利用。

エージェントの挙動は主に以下で決まります:
- システムプロンプト（トーン/制約）
- 推論パラメータ（温度、最大トークンなど）
- 文脈（どの履歴を何件送るか）

### コンテキスト構築（会話履歴）

- `openai.py` で、同一会話の直近N件のメッセージを取得し、OpenAI メッセージ配列に整形します。
- 先頭に system、続けて user/assistant を時系列順で並べます。
- 会話履歴nの上限は設定可能とし、トークン状況に応じて調整可能です。

注意点:
- 大きいメッセージはトークン上限に影響するため、必要であれば切り詰めや要約を検討。
- 画像やファイルなど非テキストは現状対象外（拡張は後述）。


## API 契約（抜粋）

エンドポイントは `backend/src/prontia/api/*.py` に定義されています。

- POST `/conversation/{conversation_id}/messages`（または新規作成用のエンドポイント）
  - 入力（例）:
    ```json
    {
      "owner_id": "<uuid>",
      "content": "こんにちは！",
      "metadata": {}
    }
    ```
  - 出力（例）: ユーザーの投稿とAI応答の2メッセージを返却
    ```json
    {
      "user": { "id": "...", "role": "user", "content": "こんにちは！", "created_at": "..." },
      "assistant": { "id": "...", "role": "assistant", "content": "こんにちは！今日は何をお手伝いできますか？", "created_at": "..." }
    }
    ```

備考:
- ID は `uuid7`（時系列ソート可能）を採用。
- DB パーティションキーは `owner_id`。

## バックエンド実装ポイント

- `services/chat.py`
  - 会話開始・投稿受理・応答生成のオーケストレーション。
  - サービスはドメインモデルを返し、API レイヤーで DTO に変換（プロジェクト規約）。
- `services/openai.py`
  - 会話履歴（直近N件）をロードし、システムプロンプトと共に Azure OpenAI へ送信。
  - 応答テキストを返す。将来的な関数呼び出し（tool calling）拡張ポイント。
- `db/cosmosdb.py`
  - `owner_id` パーティションでの非同期操作。会話・メッセージの保存/取得。
- `core/settings.py`
  - 環境変数を一元管理。接頭辞・バリデーション方針に準拠。

## エラーハンドリングとリトライ

- ネットワーク/レート制限: エクスポネンシャルバックオフで再試行（最大回数/全体タイムアウトを設定）。
- 入力バリデーション: 空メッセージ、過大サイズ、禁止語などを事前チェック。
- OpenAI 例外: ステータスコードとメッセージをロギングし、ユーザーには一般化したエラーを返す。
- ログ: `backend/src/prontia/core/logging.py` に従い構造化ログ（会話ID・owner_idを相関IDとして付与）。

## テスト方針

- `pytest-asyncio` + `pytest-mock` を用いて境界でモック。
- OpenAI 呼び出し・Cosmos DB はモック化し、サービスの入出力整合性を検証。
- 代表テスト:
  - `tests/prontia/services/test_chat_service.py`
  - `tests/prontia/services/test_openai_services.py`
  - `tests/prontia/db/test_cosmosdb.py`
  - `tests/prontia/api/test_conversation_api.py`

## 新しいエージェントを追加するには

1. システムプロンプトを設計
   - `models/prompt.py` にテンプレートを追加（必要に応じて変数化）。
2. サービスを実装
   - `services/` にエージェント固有のサービス（例: `analysis_agent.py`）を作成。
   - コンテキスト構築・推論パラメータ・後処理（要約/整形）を定義。
3. API を公開
   - `api/` にエンドポイントを追加。DTO で公開契約を固定化。
4. 永続化・スキーマ
   - 既存のメッセージモデルを流用。必要なら `models/` を拡張しマイグレーション方針を定義。
5. テスト
   - サービス/DB/API それぞれのレベルでモックを活用しカバレッジを確保。

## 今後の拡張（設計メモ）

- Tool Calling（関数呼び出し）
  - 例: 検索、計算、社内API呼び出し。`openai.py` にツール定義・ハンドラの導入。
- RAG（外部知識統合）
  - Cosmos/Blob/検索サービスからのドキュメント拡張。埋め込み・再ランキングの導入。
- ストリーミング応答（SSE/WebSocket）
  - トークンストリームを UI に逐次反映。`conversation.py` にストリームエンドポイントを追加。
- メモリ階層
  - 短期（直近履歴）/長期（ユーザープロファイルや方針）/知識（FAQ）での分離。
- ガードレール
  - 入出力フィルタ、トピック制限、ポリシー違反時の代替文生成。


## 参考

- アーキテクチャ概要: `.github/copilot-instructions.md`
- 主要ファイル:
  - `backend/src/prontia/services/chat.py`
  - `backend/src/prontia/services/openai.py`
  - `backend/src/prontia/api/conversation.py`
  - `backend/src/prontia/models/prompt.py`
  - `backend/src/prontia/db/cosmosdb.py`
  - `backend/src/prontia/core/settings.py`

## 付録: リクエスト/レスポンス例

リクエスト（新規会話開始の一例）

```json
{
  "owner_id": "018fa9cc-6f24-7a20-bd9f-33e4d3a5d6b1",
  "content": "要件を整理したいです。箇条書きで手伝ってください。"
}
```

レスポンス（例）

```json
{
  "user": {
    "id": "018fa9cc-6f24-7a20-bd9f-33e4d3a5d6b2",
    "conversation_id": "018fa9cc-6f24-7a20-bd9f-33e4d3a5d6b0",
    "role": "user",
    "content": "要件を整理したいです。箇条書きで手伝ってください。",
    "created_at": "2025-10-28T01:23:45Z"
  },
  "assistant": {
    "id": "018fa9cc-6f24-7a20-bd9f-33e4d3a5d6b3",
    "conversation_id": "018fa9cc-6f24-7a20-bd9f-33e4d3a5d6b0",
    "role": "assistant",
    "content": "了解しました。まずは現状・目的・制約・成功条件をそれぞれ2–3行で挙げてみましょう。",
    "created_at": "2025-10-28T01:23:46Z"
  }
}
```
