# ECサイト商品売上データ - 機械学習予測モデル用データ仕様

## 概要
本ECサイトシステムのデータを活用して機械学習予測モデルを構築するためのデータ説明書です。
リレーショナルデータベース構造から特徴量を抽出し、複数の予測タスクに対応可能な設計となっています。

## データベース構造

### テーブル構成
- **categories**: 商品カテゴリー情報（5カテゴリー）
- **products**: 商品マスター（25商品）
- **customers**: 顧客情報（15顧客）
- **orders**: 注文情報（20注文）
- **order_items**: 注文明細（34明細）

## 主要予測タスクと目的変数

### 1. 売上予測モデル（回帰）
**目的変数**: `total_amount` (orders.total_amount)
- **説明**: 注文の総金額を予測
- **活用場面**: 月次売上予測、予算計画、在庫計画

### 2. 購入確率予測モデル（分類）
**目的変数**: `will_purchase` (派生変数)
- **説明**: 顧客が次回購入するかどうかの二値分類
- **定義**: 過去30日以内に購入した顧客 = 1, それ以外 = 0
- **活用場面**: マーケティング施策、リターゲティング

### 3. 商品推薦モデル（分類・ランキング）
**目的変数**: `product_preference` (派生変数)
- **説明**: 顧客が特定商品を購入する確率
- **活用場面**: レコメンデーション、クロスセル

### 4. 顧客生涯価値予測（回帰）
**目的変数**: `customer_lifetime_value` (派生変数)
- **説明**: 顧客の将来的な総購入金額
- **計算**: 過去の購入パターンから算出
- **活用場面**: 顧客セグメンテーション、優良顧客の特定

## 特徴量設計

### 顧客特徴量
- **基本情報**: customer_id, 登録日からの経過日数（registration_days）
- **購入履歴**: 総購入回数（total_orders）、総購入金額（total_spent）
- **購入パターン**: 平均注文金額（avg_order_value）、最終購入からの日数（days_since_last_order）
- **商品嗜好**: 最も購入するカテゴリー（favorite_category）

### 商品特徴量
- **基本情報**: 価格（price）、原価（cost）、利益率（profit_margin = (price-cost)/price）
- **カテゴリー**: category_id（ワンホットエンコーディング推奨）
- **在庫**: 在庫数（stock_quantity）
- **売上実績**: 総販売数（total_sold）、総売上（total_revenue）

### 時間特徴量
- **時系列**: 年、月、曜日、四半期
- **季節性**: 月による季節フラグ
- **トレンド**: 過去N日間の売上トレンド

### 注文特徴量
- **金額**: 商品合計（subtotal）、配送料（shipping_cost）、税額（tax_amount）
- **構成**: 注文内商品数（items_count）、平均単価（avg_item_price）

## データ前処理

### 欠損値処理
- 数値項目: 中央値または平均値で補完
- カテゴリ項目: 最頻値または'unknown'で補完

### 特徴量エンジニアリング
```sql
-- 顧客の購入傾向特徴量
SELECT 
    c.id as customer_id,
    COUNT(o.id) as total_orders,
    SUM(o.total_amount) as total_spent,
    AVG(o.total_amount) as avg_order_value,
    MAX(o.order_date) as last_order_date,
    JULIANDAY('now') - JULIANDAY(MAX(o.order_date)) as days_since_last_order
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id;
```

### スケーリング
- **数値特徴量**: StandardScaler または MinMaxScaler
- **カテゴリ特徴量**: One-hot encoding または Label encoding

## モデル選択指針

### 売上予測
- **線形回帰**: ベースライン
- **Random Forest**: 非線形関係の捕捉
- **XGBoost**: 高精度が必要な場合
- **LSTM**: 時系列パターンが重要な場合

### 分類タスク
- **ロジスティック回帰**: 解釈性重視
- **Random Forest**: バランス型
- **SVM**: 高次元データ
- **Neural Networks**: 複雑なパターン

## 評価指標

### 回帰タスク
- **RMSE**: 予測精度の基本指標
- **MAE**: 外れ値の影響を抑えた評価
- **R²**: 説明力の評価

### 分類タスク
- **Accuracy**: 全体的な正解率
- **Precision/Recall**: 不均衡データの場合
- **AUC-ROC**: 閾値に依存しない評価
- **F1-Score**: PrecisionとRecallの調和平均

## データ分割戦略
- **学習用**: 70%
- **検証用**: 15% 
- **テスト用**: 15%
- **時系列分割**: 過去データで学習、未来データで評価

## 注意事項
- データリーケージの防止（未来の情報を使用しない）
- カテゴリ不均衡への対処（SMOTE等の利用検討）
- 季節性やトレンドの考慮
- 定期的なモデル再学習の実装

## ファイル構成
- `data/`: CSV形式の学習データ
- `schema.sql`: データベース構造定義
- `csv_loader.py`: データ読み込み機能
- `sales_analyzer.py`: 基本分析機能（特徴量生成の参考）