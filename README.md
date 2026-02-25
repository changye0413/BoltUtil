<div align="center">
  <img src="https://boltutil.com/logo.png" alt="BoltUtil Logo" width="120" />
  <h1>BoltUtil Protocol</h1>
  <p><b>面向开发者的非托管 USDT 支付网关</b></p>
  <p><i>Enterprise-Grade Non-Custodial USDT Payment Infrastructure</i></p>

  <p>
    <a href="#-简体中文">简体中文</a> | 
    <a href="#-english">English</a> | 
    <a href="#-español">Español</a> | 
    <a href="#-français">Français</a> | 
    <a href="#-português">Português</a> | 
    <a href="#-türkçe">Türkçe</a> | 
    <a href="#-tiếng-việt">Tiếng Việt</a> | 
    <a href="#-pусский">Русский</a> | 
    <a href="#-بالعربية">العربية</a> | 
    <a href="#-हिन्दी">हिन्दी</a> | 
    <a href="#-日本語">日本語</a> | 
    <a href="#-한국어">한국어</a>
  </p>

  [![Website](https://img.shields.io/badge/Website-boltutil.com-blue)](https://boltutil.com)
  [![License](https://img.shields.io/badge/License-MIT-green)](https://boltutil.com)
  [![Uptime](https://img.shields.io/badge/Uptime-99.9%25-brightgreen)](https://boltutil.com)
  [![Fee](https://img.shields.io/badge/Fee-0%25-orange)](https://boltutil.com)
</div>

---

<a name="-简体中文"></a>
## 🇨🇳 简体中文

### 💡 核心价值
BoltUtil 是一个**非托管**的支付监听协议。资金不经过平台，直接从用户钱包到达您的钱包，杜绝任何资金冻结或平台跑路风险。

### 🌟 项目优势
* **多链兼容**：完美支持 **USDT-TRC20**, **USDT-ERC20** (6位精度) 及 **USDT-BEP20** (18位精度)。
* **零丢单监控**：针对 BEP20 的 18 位高精度数据执行 `BigDecimal` 无损转换，确保 `11.508976` 等复杂订单 100% 匹配。
* **内置收银台**：提供预构建的**收银台页面**，无需开发前端，一个链接即可发起收款。
* **0 手续费**：平台不抽取任何交易佣金，利润全归商家。

### 🛠️ 技术架构
1. **API 调用**：发起 `POST /v1/order/create`。
2. **分布式监听**：节点集群实时扫描链上 `Transfer` 事件。
3. **安全回调**：通过 **HMAC-SHA256** 签名进行异步 Webhook 通知。

### 🔒 安全机制
* **分布式共识**：多节点确认确认数，防御链上回滚攻击。
* **精度护盾**：专门修复 BEP20 精度偏移问题，确保账目分毫不差。

---

<a name="-english"></a>
## 🇺🇸 English

### 💡 Core Value
BoltUtil is a **non-custodial** payment listener. Funds never touch our platform—they move directly from the user's wallet to yours, eliminating any risk of fund freezing or platform exit scams.

### 🌟 Key Advantages
* **Multi-Chain Support**: Native compatibility for **USDT-TRC20**, **USDT-ERC20** (6 decimals), and **USDT-BEP20** (18 decimals).
* **Zero-Loss Monitoring**: Uses `BigDecimal` lossless conversion for BEP20's 18-decimal data, ensuring 100% matching for complex amounts like `11.508976`.
* **Built-in Checkout**: Includes a **Ready-to-Use Checkout Page**. No frontend development required—launch payments via a simple URL.
* **0% Transaction Fee**: We take no commission. Your profits stay 100% yours.

### 🛠️ Technical Architecture
1. **API Call**: Initiate `POST /v1/order/create`.
2. **Distributed Listening**: Node clusters scan on-chain `Transfer` events in real-time.
3. **Secure Webhook**: Asynchronous notification secured with **HMAC-SHA256** signatures.

### 🔒 Security Features
* **Distributed Consensus**: Multi-node confirmation count to prevent blockchain rollback attacks.
* **Precision Shield**: Specialized logic to fix BEP20 decimal offsets, ensuring perfect accounting.



---

<a name="-español"></a>
## 🇪🇸 Español

### 💡 Valor Central
BoltUtil es un protocolo de escucha de pagos **no custodiado**. Los fondos van directamente de la billetera del usuario a la suya.

### 🌟 Ventajas Clave
* **Multicadena**: Soporte para **USDT-TRC20**, **USDT-ERC20** (6 decimales) y **USDT-BEP20** (18 decimales).
* **Monitoreo de Alta Precisión**: Conversión `BigDecimal` para BEP20, garantizando coincidencia del 100% en pedidos como `11.508976`.
* **Checkout Integrado**: **Página de pago lista para usar** incluida. Sin necesidad de desarrollo frontend.
* **Comisión del 0%**: No retenemos ningún porcentaje de sus ventas.

### 🛠️ Arquitectura Técnica
1. **Llamada API**: `POST /v1/order/create`.
2. **Escucha Distribuida**: Escaneo en tiempo real de eventos `Transfer`.
3. **Webhook Seguro**: Firmas **HMAC-SHA256** para notificaciones.

### 🔒 Seguridad
* **Consenso Distribuido**: Validación multi-nodo contra ataques de rollback.
* **Escudo de Precisión**: Elimina errores de redondeo en redes BSC/BEP20.

---

<a name="-français"></a>
## 🇫🇷 Français

### 💡 Valeur Fondamentale
BoltUtil est un protocole de paiement **non-custodial**. Les fonds circulent directement entre portefeuilles P2P.

### 🌟 Avantages
* **Multi-chaîne**: Support complet de **USDT-TRC20**, **ERC20** (6 décimales) et **BEP20** (18 décimales).
* **Matching Parfait**: Utilisation de `BigDecimal` pour les 18 décimales de la BEP20 (ex: `11.508976`).
* **Page de Paiement Incluse**: Interface de paiement **prête à l'emploi**. Zéro développement frontend requis.
* **Frais de 0%**: Aucune commission prélevée sur vos transactions.

### 🛠️ Architecture & Sécurité
* **Flux**: API REST -> Cluster de Noeuds -> Webhook asynchrone (**HMAC-SHA256**).
* **Protection**: Consensus multi-noeuds pour prévenir les attaques de rollback et bouclier de précision décimale.

---

<a name="-português"></a>
## 🇧🇷 Português

### 💡 Valor Principal
Protocolo de pagamento **não-custodial**. Os fundos vão direto para sua carteira.

### 🌟 Vantagens
* **Suporte Multi-Chain**: **USDT-TRC20**, **ERC20** (6 decimais) e **BEP20** (18 decimais).
* **Precisão Total**: Conversão `BigDecimal` para garantir que valores como `11.508976` no BEP20 batam 100%.
* **Checkout Integrado**: **Página de checkout pronta**. Sem necessidade de programar o front-end.
* **Taxa 0%**: Fique com 100% do seu lucro.

### 🛠️ Arquitetura e Segurança
* **Processo**: API -> Monitoramento em tempo real -> Webhook com assinatura **HMAC-SHA256**.
* **Segurança**: Consenso distribuído contra rollback e tratamento rigoroso de decimais.

---

<a name="-türkçe"></a>
## 🇹🇷 Türkçe

### 💡 Temel Değer
**Gözetimsiz (Non-custodial)** ödeme protokolü. Fonlar doğrudan sizin cüzdanınıza geçer.

### 🌟 Avantajlar
* **Çoklu Ağ**: **USDT-TRC20**, **ERC20** (6 ondalık) ve **BEP20** (18 ondalık) desteği.
* **Hassas İzleme**: BEP20'nin 18 ondalık verisi için `BigDecimal` dönüşümü, `%100` eşleşme sağlar.
* **Hazır Ödeme Sayfası**: Geliştirme gerektirmeyen **Checkout sayfası**.
* **%0 Komisyon**: İşlemlerinizden pay almayız.

### 🛠️ Teknik Mimari ve Güvenlik
* **Sistem**: API çağrısı -> Dağıtık düğüm izleme -> **HMAC-SHA256** imzalı güvenli Webhook.
* **Koruma**: Rollback saldırılarına karşı çoklu düğüm onayı ve ondalık hassasiyet kalkanı.

---

<a name="-tiếng-việt"></a>
## 🇻🇳 Tiếng Việt

### 💡 Giá trị cốt lõi
Giao thức thanh toán **phi lưu ký (non-custodial)**. Tiền chuyển thẳng từ ví khách hàng sang ví của bạn.

### 🌟 Ưu điểm
* **Đa chuỗi**: Hỗ trợ **USDT-TRC20**, **ERC20** (6 số thập phân) và **BEP20** (18 số thập phân).
* **Khớp lệnh chính xác**: Chuyển đổi `BigDecimal` cho BEP20, đảm bảo khớp đơn hàng `11.508976` 100%.
* **Trang thanh toán tích hợp**: Có sẵn **trang Checkout**, không cần phát triển giao diện người dùng.
* **Phí 0%**: Giữ trọn 100% lợi nhuận của bạn.

### 🛠️ Kiến trúc & Bảo mật
* **Quy trình**: Gọi API -> Theo dõi chuỗi khối -> Thông báo Webhook qua chữ ký **HMAC-SHA256**.
* **Bảo mật**: Cơ chế đồng thuận đa nút chống tấn công rollback và khiên bảo vệ độ chính xác thập phân.

---

<a name="-pусский"></a>
## 🇷🇺 Русский

### 💡 Основная ценность
**Некастодиальный** платежный протокол. Средства поступают напрямую на ваш кошелек.

### 🌟 Преимущества
* **Мультичейн**: Поддержка **USDT-TRC20**, **ERC20** (6 знаков) и **BEP20** (18 знаков).
* **Точный мониторинг**: `BigDecimal` преобразование для BEP20, 100% совпадение сумм (напр. `11.508976`).
* **Готовый чекаут**: Встроенная **платежная страница**. Не нужно разрабатывать фронтенд.
* **0% комиссия**: Вся прибыль остается у вас.

### 🛠️ Архитектура и Безопасность
* **Логика**: API запрос -> Распределенные узлы мониторинга -> Webhook с подписью **HMAC-SHA256**.
* **Защита**: Консенсус нескольких узлов против отката транзакций и защита точности BEP20.

---

<a name="-بالعربية"></a>
## 🇸🇦 العربية

### 💡 القيمة الأساسية
بروتوكول دفع **غير احتجازي**. تتدفق الأموال مباشرة من محفظة المستخدم إلى محفظتك.

### 🌟 المميزات
* **دعم متعدد الشبكات**: يدعم **USDT-TRC20** و **ERC20** (6 خانات) و **BEP20** (18 خانة).
* **مطابقة دقيقة**: استخدام `BigDecimal` لشبكة BEP20 لضمان مطابقة الطلبات المعقدة بنسبة 100%.
* **صفحة دفع جاهزة**: تتضمن **صفحة Checkout** مدمجة. لا حاجة لتطوير الواجهة الأمامية.
* **عمولة 0%**: لا نقتطع أي عمولات من مبيعاتك.

### 🛠️ المعمارية والأمان
* **العملية**: استدعاء API -> مراقبة الشبكة -> تنبيه Webhook بتوقيع **HMAC-SHA256**.
* **الحماية**: إجماع العقد الموزعة ضد هجمات الارتداد ودرع حماية دقة الكسور العشرية.

---

<a name="-हिन्दी"></a>
## 🇮🇳 हिन्दी

### 💡 मुख्य मूल्य
यह एक **नॉन-कस्टोडियल** पेमेंट प्रोटोकॉल है। फंड सीधे आपके वॉलेट में पहुंचता है।

### 🌟 लाभ
* **मल्टी-चेन**: **USDT-TRC20**, **ERC20** (6 दशमलव) और **BEP20** (18 दशमलव) का समर्थन।
* **सटीक मॉनिटरिंग**: BEP20 के लिए `BigDecimal` का उपयोग, ताकि `11.508976` जैसे ऑर्डर 100% मैच हों।
* **इन-बिल्ट चेकआउट**: **रेडी-टू-यूज़ पेमेंट पेज**। कोई फ्रंटएंड डेवलपमेंट की आवश्यकता नहीं।
* **0% शुल्क**: हम आपकी बिक्री पर कोई कमीशन नहीं लेते हैं।

### 🛠️ आर्किटेक्चर और सुरक्षा
* **प्रक्रिया**: API कॉल -> डिस्ट्रीब्यूटेड नोड मॉनिटरिंग -> **HMAC-SHA256** हस्ताक्षरित Webhook।
* **सुरक्षा**: रोलबैक हमलों से बचने के लिए मल्टी-नोड पुष्टिकरण और सटीकता शील्ड।

---

<a name="-日本語"></a>
## 🇯🇵 日本語

### 💡 コアバリュー
BoltUtilは**非管財型（ノンカストディアル）**決済プロトコルです。資金はプラットフォームを経由せず、直接あなたのウォレットに届きます。

### 🌟 主な利点
* **マルチチェーン対応**: **USDT-TRC20**, **ERC20** (6桁) および **BEP20** (18桁) を完全にサポート。
* **高精度マッチング**: BEP20の18桁データに `BigDecimal` 無損変換を適用し、`11.508976` 等の注文を100%照合。
* **支払いページ内蔵**: 構築済みの**チェックアウトページ**を提供。フロントエンド開発不要で即座に導入可能。
* **手数料 0%**: 取引手数料は一切かかりません。利益はすべてあなたのものです。

### 🛠️ 技術アーキテクチャとセキュリティ
* **フロー**: API呼び出し -> 分散ノードによるリアルタイム監視 -> **HMAC-SHA256** 署名付きWebhook通知。
* **防御機能**: ロールバック攻撃を防ぐ複数ノード合意形成と、小数点誤差を排除する精度シールド。

---

<a name="-한국어"></a>
## 🇰🇷 한국어

### 💡 핵심 가치
BoltUtil은 **비수탁형(Non-custodial)** 결제 리스너 프로토콜입니다. 자금은 플랫폼을 거치지 않고 고객의 지갑에서 귀하의 지갑으로 직접 전송됩니다.

### 🌟 주요 장점
* **멀티체인 지원**: **USDT-TRC20**, **ERC20** (6자리) 및 **BEP20** (18자리) 완벽 호환.
* **제로 손실 모니터링**: BEP20의 18자리 데이터를 `BigDecimal`로 무손실 변환하여 `11.508976`과 같은 주문을 100% 매칭.
* **체크아웃 페이지 내장**: 즉시 사용 가능한 **결제 페이지(Checkout)** 제공. 프론트엔드 개발 없이 링크 하나로 결제 가능.
* **수수료 0%**: 플랫폼 이용에 따른 거래 수수료가 전혀 없습니다.

### 🛠️ 기술 아키텍처 및 보안
* **프로세스**: API 호출 -> 분산 노드 실시간 스캔 -> **HMAC-SHA256** 서명 기반 비동기 Webhook 알림.
* **보안 기능**: 블록체인 롤백 공격 방지를 위한 다중 노드 합의 및 소수점 오차 방지 정밀 실드.

---

## 🔒 通用验证 (Security Validation)



1. **分布式共识**：至少 3 个节点确认链上状态变化才触发通知。
2. **精度护盾 (Precision Shield)**：专为 **BEP20** 打造的 `BigDecimal` 处理逻辑。
3. **HMAC 签名**：确保 Webhook 数据未被篡改。

---
© 2026 BoltUtil Protocol. Built by Developers, for Developers.
