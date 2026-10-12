# BoltUtil v2.1

[English](README.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [Tiếng Việt](README.vi.md) · [Türkçe](README.tr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md)

## USDT와 USDC 결제, 내 지갑으로 직접.

[무료로 시작](https://boltutil.com/ko/auth/register?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=start) · [API 문서](https://boltutil.com/ko/developer-docs?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=docs) · [요금](https://boltutil.com/ko/pricing?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=pricing)

BoltUtil v2.1은 웹사이트, SaaS, WooCommerce 스토어를 위한 비수탁 스테이블코인 결제 API와 호스팅 결제 페이지입니다. 판매자 서버가 주문을 만들고 고객은 판매자의 수취 주소로 송금합니다. BoltUtil은 온체인 전송과 확인 조건을 검증한 뒤 서명된 Webhook을 보냅니다. 개인 키나 복구 문구를 요구하지 않습니다.

## 네트워크와 자산

하나의 연동으로 6개 네트워크와 11개 자산/네트워크 조합을 지원합니다. TRON은 USDT, Ethereum·Polygon PoS·Solana는 USDT와 네이티브 USDC, BNB Smart Chain은 USDT와 Binance-Peg USDC, Base는 Bridged USDT와 네이티브 USDC를 지원합니다. 서비스가 활성화하고 판매자의 수취 주소가 활성 상태인 경로만 표시됩니다. 네이티브·브리지·페그 토큰은 서로 대체할 수 없습니다. 주문에 지정된 컨트랙트 또는 mint를 확인하세요. Base 확인은 설정된 L1 최종성 정책에 따르며 고정 완료 시간을 보장하지 않습니다.

## 지갑 결제 또는 수동 송금

수취 주소, 네트워크, 정확한 금액이 자동 입력되고 고객이 지갑에서 검토하고 승인합니다. 수동 송금, QR, 주소 복사도 유지됩니다. MetaMask, OKX Wallet, Trust Wallet, Phantom, TronLink, Bitget Wallet, Binance Wallet, TokenPocket, SafePal, Base app의 선택지는 네트워크와 기기에 따라 달라집니다. 일부는 앱 내 브라우저에서 주문을 여는 방식이며 모든 지갑이 QR로 휴대폰과 데스크톱 세션을 연결하는 것은 아닙니다. 연결만으로 송금하지 않습니다. 처음에는 잠금 해제, 연결 승인, 네트워크 변경이 필요할 수 있으며 수수료용 네이티브 코인이 필요합니다.

## 연동 시작

1. 계정을 만들고 수취 주소를 활성화한 뒤 LIVE API Key를 발급합니다.
2. 같은 판매자 계정에서 HTTPS Webhook을 설정하고 비밀값을 서버에 보관합니다.
3. 주문을 만들고 응답의 `checkoutUrl`을 엽니다.
4. `payment.amount`를 반올림 없이 표시합니다. 동시 주문 식별 때문에 원래 금액과 조금 다를 수 있습니다.
5. 서명, timestamp, 주문, 자산, 네트워크, 확인된 상태를 검증하고 중복 처리 없이 이행합니다.

API 최소 금액은 1이고 소수점 이하 최대 6자리입니다. Node.js, Python, PHP, Go, Java, C# 예제의 기본값은 USDT입니다. USDC는 활성 조합으로 변경하세요. OpenAPI와 Postman도 제공합니다.

## WooCommerce와 요금제

별도 플러그인 v0.6.1은 토큰과 네트워크를 선택하고 결제 검증 후 주문을 업데이트합니다. 스토어로 돌아오는 것만으로 결제 완료가 되지 않습니다. WordPress 7.0+, PHP 7.4+, WooCommerce 11.1+, HTTPS, 스토어 통화 USD가 필요하며 실시간 환율 견적이나 고정은 제공하지 않습니다. 2026년 10월 12일 WordPress.org에 제출되어 자동 스캔을 통과했고 수동 심사를 기다립니다. 공개 전에는 GitHub Releases의 ZIP을 설치하세요. 데모 스토어 구매는 실제 자금을 사용합니다.

매일 무료 주문 한도가 있으며 구독은 일일 주문 수 제한이 없습니다. 최신 한도·혜택·요금은 공식 사이트를 확인하세요. 네트워크 수수료는 별도입니다. 부족·지연·귀속 불명 결제는 검토가 필요합니다. BoltUtil은 거래소나 자동 법정통화 환전 서비스가 아닙니다.

공개 문서와 예제는 MIT이며 운영 플랫폼 소스는 비공개입니다. 플러그인은 GPLv2 이상입니다. 브랜드 표시는 공식 보증을 의미하지 않습니다. 영어 가이드와 API를 기술 기준으로 사용하세요. 비밀값을 공개하지 말고 보안 제보는 SECURITY.md를 따르세요.

[USDC 가이드](https://boltutil.com/ko/docs/usdc-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [Base 가이드](https://boltutil.com/ko/docs/base-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [WooCommerce 플러그인](https://github.com/changye0413/boltutil-payments-for-woocommerce) · [데모 스토어](https://shop-test.boltutil.com/)

[지원 및 예제](examples/README.md) · [OpenAPI](openapi.yaml) · [Postman](postman/BoltUtil.postman_collection.json) · [Discussions](https://github.com/changye0413/BoltUtil/discussions) · [support@boltutil.com](mailto:support@boltutil.com) · [X: @heyharryzhang](https://x.com/heyharryzhang) · [English](README.md)
