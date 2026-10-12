# BoltUtil v2.1

[English](README.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [Tiếng Việt](README.vi.md) · [Türkçe](README.tr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md)

## USDT・USDC 決済を、あなたのウォレットへ直接。

[無料で始める](https://boltutil.com/ja/auth/register?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=start) · [API ドキュメント](https://boltutil.com/ja/developer-docs?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=docs) · [料金](https://boltutil.com/ja/pricing?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=pricing)

BoltUtil v2.1 は、Web サイト、SaaS、WooCommerce ストア向けの非カストディ型ステーブルコイン決済 API とホスト型決済ページです。加盟店のサーバーが注文を作成し、購入者が加盟店の受取アドレスへ送金します。BoltUtil はオンチェーン送金と承認条件を確認し、署名付き Webhook を送ります。秘密鍵やリカバリーフレーズは要求しません。

## 対応ネットワークと資産

6 ネットワーク、11 種類の資産・ネットワーク組み合わせを共通の手順で接続できます。TRON は USDT、Ethereum・Polygon PoS・Solana は USDT とネイティブ USDC、BNB Smart Chain は USDT と Binance-Peg USDC、Base は Bridged USDT とネイティブ USDC に対応します。サービスで有効化され、加盟店の受取アドレスが有効な経路のみ表示します。ネイティブ、ブリッジ、ペッグ版は別の資産です。注文指定のコントラクトまたは Mint を使用してください。Base の承認は設定された L1 ファイナリティ方針に従い、一定時間での完了を保証しません。

## ウォレット決済と手動送金

受取アドレス、ネットワーク、正確な金額を自動入力し、購入者がウォレット内で確認・承認します。手動送金、QR コード、アドレスコピーも利用できます。MetaMask、OKX Wallet、Trust Wallet、Phantom、TronLink、Bitget Wallet、Binance Wallet、TokenPocket、SafePal、Base app の入口はネットワークと端末によって変わります。アプリ内ブラウザーで注文を開く方式もあり、すべてが QR によるスマートフォンと PC のセッション接続に対応するわけではありません。接続だけでは送金しません。初回はロック解除、接続許可、ネットワーク切替が必要な場合があり、手数料にはネットワークのネイティブ通貨が必要です。

## 導入手順

1. アカウントを作成し、受取アドレスを有効化して LIVE API Key を発行します。
2. 同じ加盟店アカウントで HTTPS Webhook を設定し、署名用シークレットをサーバーに保存します。
3. 注文を作成し、返された `checkoutUrl` を開きます。
4. `payment.amount` を丸めずに表示します。同時注文を区別するため、元の金額と少し異なる場合があります。
5. 署名、timestamp、注文、資産、ネットワーク、承認済み状態を検証し、重複履行を防ぎます。

API の最小金額は 1、小数点以下は最大 6 桁です。Node.js・Python・PHP・Go・Java・C# の例は USDT が初期値です。USDC では有効な組み合わせに変更してください。OpenAPI と Postman もあります。

## WooCommerce と料金

別の v0.6.1 プラグインで通貨・ネットワークを選択できます。検証後に注文を更新し、ストアへのリダイレクトだけでは支払済みにしません。WordPress 7.0+、PHP 7.4+、WooCommerce 11.1+、HTTPS、ストア通貨 USD が必要です。リアルタイム為替見積もりやレート固定は提供しません。2026 年 10 月 12 日に WordPress.org へ提出し、自動スキャンは合格、手動審査待ちです。公開前は GitHub Releases の ZIP を使用してください。デモストアの購入には実際の資金を使います。

毎日の無料注文枠と、日次注文数の制限がないサブスクリプションがあります。最新の枠・特典・料金は公式サイトをご確認ください。ネットワーク手数料は別途発生します。不足・遅延・帰属不明の支払いは確認が必要です。取引所や自動法定通貨換算サービスではありません。

公開ドキュメントと例は MIT、商用プラットフォーム本体は非公開です。プラグインは GPLv2 以降です。ブランド名は公式の推奨を意味しません。技術仕様は英語ガイドと API リファレンスを基準とし、秘密情報は公開せず、安全性の報告は SECURITY.md に従ってください。

[USDC ガイド](https://boltutil.com/ja/docs/usdc-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [Base ガイド](https://boltutil.com/ja/docs/base-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [WooCommerce プラグイン](https://github.com/changye0413/boltutil-payments-for-woocommerce) · [デモストア](https://shop-test.boltutil.com/)

[サポートと例](examples/README.md) · [OpenAPI](openapi.yaml) · [Postman](postman/BoltUtil.postman_collection.json) · [Discussions](https://github.com/changye0413/BoltUtil/discussions) · [support@boltutil.com](mailto:support@boltutil.com) · [X: @heyharryzhang](https://x.com/heyharryzhang) · [English](README.md)
