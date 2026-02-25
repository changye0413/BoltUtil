<div align="center">
  <img src="https://boltutil.com/logo.png" alt="BoltUtil Logo" width="120" />
  <h1>BoltUtil Protocol</h1>
  <p><b>面向开发者的企业级非托管 USDT 支付基础设施</b></p>
  <p><i>The Enterprise-Grade Non-Custodial USDT Payment Infrastructure</i></p>

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
  [![Docs](https://img.shields.io/badge/Docs-QuickStart-green)](https://docs.boltutil.com)
  [![Fee](https://img.shields.io/badge/Fee-0%25-orange)](https://boltutil.com)
</div>

---

<a name="-简体中文"></a>
## 🇨🇳 简体中文

### 📖 项目介绍
BoltUtil 是一套专为开发者设计的**非托管（Non-custodial）**支付监听协议。资金通过 P2P 方式**直达您的私有钱包**，平台不触碰私钥，彻底杜绝资金冻结或跑路风险。内置**生产级收银台页面**，无需前端开发即可实现跨平台支付体验。

### 🛠️ 技术架构
* **多链监听**：实时扫描 **TRC20/ERC20** (6位精度) 及 **BEP20** (18位精度) 的 `Transfer` 事件。
* **高精度匹配**：针对 BEP20 执行 `BigDecimal` 无损转换，确保 `11.508976` 等订单 100% 匹配。
* **签名安全**：回调采用 **HMAC-SHA256** 算法，将参数按 ASCII 升序排列并结合 `API_SECRET` 计算签名。
* **验证机制**：服务端通过校验 `X-Bolt-Signature` 及 `timestamp`（防止重放攻击）确保回调真实性。

### 🔒 安全机制
* **分布式共识**：基于多节点确认，有效防御链上回滚攻击。
* **精度护盾**：专为 BEP20 打造，消除浮点数精度偏移导致的丢单痛点。
* **幂等处理**：每个通知含唯一 `trade_no` (Hash)，防止系统重复入账。

🔗 **[进入官网](https://boltutil.com)** | **[阅读文档](https://docs.boltutil.com)**

---

<a name="-english"></a>
## 🇺🇸 English

### 📖 Project Introduction
BoltUtil is a **non-custodial** payment listener protocol. Funds flow P2P **directly to your private wallet**. We never touch your private keys, eliminating risks of fund freezing or exit scams. Features a **production-ready checkout page** for an instant cross-platform payment experience without frontend development.

### 🛠️ Technical Architecture
* **Multi-Chain Scanning**: Real-time monitoring of `Transfer` events for **TRC20/ERC20** (6 decimals) and **BEP20** (18 decimals).
* **Precision Matching**: Uses `BigDecimal` for BEP20 to ensure 100% matching for complex amounts like `11.508976`.
* **Security Signature**: Webhooks use **HMAC-SHA256**. Parameters are sorted by ASCII and hashed with your `API_SECRET`.
* **Validation**: Servers verify the `X-Bolt-Signature` and `timestamp` (to prevent replay attacks) to ensure authenticity.

### 🔒 Security Features
* **Distributed Consensus**: Multi-node confirmations to defend against blockchain rollback attacks.
* **Precision Shield**: Specialized BEP20 logic to eliminate decimal offset errors.
* **Idempotency**: Every notification includes a unique `trade_no` (Hash) to prevent duplicate processing.

🔗 **[Official Website](https://boltutil.com)** | **[Documentation](https://docs.boltutil.com)**

---

<a name="-español"></a>
## 🇪🇸 Español

### 📖 Introducción del Proyecto
BoltUtil es un protocolo de escucha de pagos **no custodiado**. Los fondos fluyen P2P **directamente a su billetera privada**. Incluye una **página de pago lista para producción**, eliminando la necesidad de desarrollo frontend.

### 🛠️ Arquitectura Técnica
* **Monitoreo Multicadena**: Seguimiento de eventos `Transfer` en **TRC20/ERC20** (6 decimales) y **BEP20** (18 decimales).
* **Firma de Seguridad**: Webhooks protegidos con **HMAC-SHA256**. Los parámetros se ordenan por ASCII y se cifran con su `API_SECRET`.
* **Validación**: Verificación de `X-Bolt-Signature` y `timestamp` para evitar ataques de repetición.

### 🔒 Mecanismos de Seguridad
* **Consenso Distribuido**: Confirmación multi-nodo contra ataques de rollback.
* **Escudo de Precisión**: Lógica `BigDecimal` para evitar errores en redes BEP20.
* **Idempotencia**: `trade_no` único por notificación para evitar duplicados.

🔗 **[Sitio Web](https://boltutil.com)** | **[Documentación](https://docs.boltutil.com)**

---

<a name="-français"></a>
## 🇫🇷 Français

### 📖 Présentation du Projet
BoltUtil est un protocole de paiement **non-custodial**. Les fonds sont transférés en P2P **directement vers votre portefeuille**. Comprend une **page de paiement prête à l'emploi** pour une intégration sans développement frontend.

### 🛠️ Architecture Technique
* **Scan Multi-chaîne**: Surveillance en temps réel des réseaux **TRC20/ERC20** (6 décimales) et **BEP20** (18 décimales).
* **Signature HMAC**: Utilisation de **HMAC-SHA256** pour sécuriser les notifications Webhook avec votre `API_SECRET`.
* **Validation**: Vérification obligatoire de `X-Bolt-Signature` et du `timestamp` côté serveur.

### 🔒 Sécurité
* **Consensus Distribué**: Protection contre les attaques de rollback via des confirmations multi-nœuds.
* **Bouclier de Précision**: Gestion `BigDecimal` pour garantir 100% de correspondance sur BEP20.

🔗 **[Site Officiel](https://boltutil.com)** | **[Documentation](https://docs.boltutil.com)**

---

<a name="-português"></a>
## 🇧🇷 Português

### 📖 Introdução ao Projeto
BoltUtil é um protocolo **não-custodial**. O dinheiro vai **direto para sua carteira privada**. Oferece uma **página de checkout profissional**, dispensando desenvolvimento front-end.

### 🛠️ Arquitetura Técnica
* **Monitoramento Multi-Chain**: Suporte para **TRC20/ERC20** (6 decimais) e **BEP20** (18 decimais).
* **Assinatura de Segurança**: Webhooks com **HMAC-SHA256**. Parâmetros ordenados por ASCII e combinados com seu `API_SECRET`.
* **Validação de Callback**: Verificação de `X-Bolt-Signature` e carimbo de data/hora (timestamp).

### 🔒 Segurança
* **Consenso Distribuído**: Confirmações multi-nó contra ataques de rollback na blockchain.
* **Escudo de Precisão**: Conversão `BigDecimal` para evitar perdas em transações BEP20.

🔗 **[Site Oficial](https://boltutil.com)** | **[Documentação](https://docs.boltutil.com)**

---

<a name="-türkçe"></a>
## 🇹🇷 Türkçe

### 📖 Proje Tanıtımı
BoltUtil, geliştiriciler için **gözetimsiz (non-custodial)** bir ödeme dinleme protokolüdür. Fonlar P2P olarak **doğrudan cüzdanınıza** ulaşır. Hazır **ödeme sayfası (checkout)** ile frontend geliştirmeye gerek kalmadan entegrasyon sağlar.

### 🛠️ Teknik Mimari
* **Çoklu Ağ İzleme**: **TRC20/ERC20** (6 ondalık) ve **BEP20** (18 ondalık) ağlarında gerçek zamanlı Transfer takibi.
* **Güvenli İmza**: Webhook'lar **HMAC-SHA256** kullanır. Parametreler ASCII sırasına göre dizilir ve `API_SECRET` ile imzalanır.
* **Doğrulama**: Sunucu tarafında `X-Bolt-Signature` ve `timestamp` kontrolü ile güvenlik sağlanır.

### 🔒 Güvenlik Mekanizması
* **Dağıtık Mutabakat**: Rollback saldırılarına karşı çoklu düğüm onayı.
* **Hassasiyet Kalkanı**: BEP20 ağındaki ondalık hatalarını önleyen `BigDecimal` mantığı.

🔗 **[Web Sitesi](https://boltutil.com)** | **[Dökümantasyon](https://docs.boltutil.com)**

---

<a name="-tiếng-việt"></a>
## 🇻🇳 Tiếng Việt

### 📖 Giới thiệu Dự án
BoltUtil là giao thức giám sát thanh toán **phi lưu ký (non-custodial)**. Tiền chuyển P2P **trực tiếp vào ví của bạn**. Cung cấp **trang thanh toán chuyên nghiệp**, không cần phát triển giao diện người dùng.

### 🛠️ Kiến trúc Kỹ thuật
* **Giám sát Đa chuỗi**: Theo dõi sự kiện `Transfer` trên **TRC20/ERC20** (6 số thập phân) và **BEP20** (18 số thập phân).
* **Chữ ký Bảo mật**: Webhook sử dụng thuật toán **HMAC-SHA256**, kết hợp với `API_SECRET` để tạo chữ ký an toàn.
* **Xác thực Webhook**: Kiểm tra `X-Bolt-Signature` và `timestamp` để ngăn chặn tấn công phát lại.

### 🔒 Cơ chế Bảo mật
* **Đồng thuận Đa nút**: Xác nhận từ nhiều nút để chống lại các cuộc tấn công rollback chuỗi khối.
* **Khiên chính xác**: Sử dụng `BigDecimal` để đảm bảo khớp 100% các đơn hàng trên mạng BEP20.

🔗 **[Trang chủ](https://boltutil.com)** | **[Tài liệu](https://docs.boltutil.com)**

---

<a name="-pусский"></a>
## 🇷🇺 Русский

### 📖 О проекте
BoltUtil — это **некастодиальный** протокол мониторинга платежей. Средства поступают **напрямую на ваш кошелек**. Включает **готовую платежную страницу**, не требующую фронтенд-разработки.

### 🛠️ Техническая архитектура
* **Мультичейн сканирование**: Мониторинг сетей **TRC20/ERC20** (6 знаков) и **BEP20** (18 знаков).
* **Безопасная подпись**: Webhook использует **HMAC-SHA256**. Параметры сортируются по ASCII и хешируются с вашим `API_SECRET`.
* **Валидация**: Проверка `X-Bolt-Signature` и `timestamp` на стороне сервера для защиты от атак.

### 🔒 Механизмы безопасности
* **Распределенный консенсус**: Подтверждение несколькими узлами для защиты от отката транзакций.
* **Защита точности**: Логика `BigDecimal` для исключения ошибок округления в сети BEP20.

🔗 **[Сайт](https://boltutil.com)** | **[Документация](https://docs.boltutil.com)**

---

<a name="-بالعربية"></a>
## 🇸🇦 العربية

### 📖 مقدمة عن المشروع
BoltUtil هو بروتوكول دفع **غير احتجازي**. تتدفق الأموال **إلى محفظتك الخاصة مباشرة**. يتضمن **صفحة دفع جاهزة** للاستخدام الفوري دون حاجة لتطوير الواجهة الأمامية.

### 🛠️ المعمارية التقنية
* **مراقبة الشبكات**: تتبع معاملات **TRC20/ERC20** (6 خانات) و **BEP20** (18 خانة).
* **توقيع آمن**: يستخدم Webhook خوارزمية **HMAC-SHA256** مع مفتاح `API_SECRET` الخاص بك.
* **التحقق من البيانات**: التحقق من `X-Bolt-Signature` و `timestamp` لمنع هجمات التكرار.

### 🔒 آليات الأمان
* **إجماع العقد**: تأكيد من عقد متعددة لضمان عدم التلاعب بالمعاملات.
* **درع الدقة**: منطق `BigDecimal` لضمان مطابقة المبالغ في شبكة BEP20 بنسبة 100%.

🔗 **[الموقع الرسمي](https://boltutil.com)** | **[التوثيق](https://docs.boltutil.com)**

---

<a name="-हिन्दी"></a>
## 🇮🇳 हिन्दी

### 📖 प्रोजेक्ट परिचय
BoltUtil एक **नॉन-कस्टोडियल** पेमेंट मॉनिटरिंग प्रोटोकॉल है। फंड **सीधे आपके निजी वॉलेट** में जाता है। इसमें **रेडी-टू-यूज़ चेकआउट पेज** शामिल है, जिससे फ्रंटएंड डेवलपमेंट की ज़रूरत नहीं पड़ती।

### 🛠️ तकनीकी आर्किटेक्चर
* **मल्टी-चेन मॉनिटरिंग**: **TRC20/ERC20** (6 दशमलव) और **BEP20** (18 दशमलव) का रियल-टाइम स्कैन।
* **सुरक्षित हस्ताक्षर**: Webhook में **HMAC-SHA256** एल्गोरिथ्म और `API_SECRET` का उपयोग किया जाता है।
* **सत्यापन**: सुरक्षा के लिए `X-Bolt-Signature` और `timestamp` की जांच।

### 🔒 सुरक्षा तंत्र
* **डिस्ट्रीब्यूटेड नोड्स**: रोलबैक हमलों से सुरक्षा के लिए मल्टी-नोड पुष्टिकरण।
* **सटीकता शील्ड**: BEP20 नेटवर्क के लिए `BigDecimal` आधारित सटीक गणना।

🔗 **[वेबसाइट](https://boltutil.com)** | **[दस्तावेज़](https://docs.boltutil.com)**

---

<a name="-日本語"></a>
## 🇯🇵 日本語

### 📖 プロジェクト紹介
BoltUtilは、開発者向けの**非管財型（ノンカストディアル）**決済監視プロトコルです。資金はP2Pで**あなたのウォレットへ直接**届きます。開発不要の**チェックアウトページ**を内蔵し、即座に導入可能です。

### 🛠️ 技術アーキテクチャ
* **マルチチェーン監視**: **TRC20/ERC20** (6桁) と **BEP20** (18桁) の `Transfer` イベントをリアルタイム監視。
* **署名セキュリティ**: Webhookには **HMAC-SHA256** を採用。パラメータをASCII順にソートし `API_SECRET` で署名。
* **検証プロセス**: サーバー側で `X-Bolt-Signature` と `timestamp` を検証し、リプレイ攻撃を防止。

### 🔒 セキュリティメカニズム
* **分散合意**: 複数ノードによる確認で、ブロックチェーンのロールバック攻撃を防御。
* **精度シールド**: `BigDecimal` 処理により、BEP20の小数点誤差による丢弾（入金漏れ）を完全に排除。

🔗 **[公式サイト](https://boltutil.com)** | **[ドキュメント](https://docs.boltutil.com)**

---

<a name="-한국어"></a>
## 🇰🇷 한국어

### 📖 프로젝트 소개
BoltUtil은 개발자를 위한 **비수탁형(Non-custodial)** 결제 모니터링 프로토콜입니다. 자금은 P2P 방식으로 **귀하의 개인 지갑으로 직접** 입금됩니다. 프론트엔드 개발이 필요 없는 **결제 페이지(Checkout)**를 제공합니다.

### 🛠️ 기술 아키텍처
* **멀티체인 스캔**: **TRC20/ERC20** (6자리) 및 **BEP20** (18자리) 네트워크의 실시간 감시.
* **보안 서명**: Webhook은 **HMAC-SHA256** 알고리즘을 사용하며 `API_SECRET`으로 암호화됩니다.
* **검증 매커니즘**: 서버에서 `X-Bolt-Signature`와 `timestamp`를 확인하여 위조 및 재전송 공격을 방지합니다.

### 🔒 보안 기능
* **분산 합의**: 다중 노드 확인을 통해 블록체인 롤백 공격으로부터 보호합니다.
* **정밀 실드**: BEP20의 소수점 오차를 해결하기 위한 `BigDecimal` 무손실 처리.

🔗 **[공식 웹사이트](https://boltutil.com)** | **[문서 페이지](https://docs.boltutil.com)**

---
© 2026 BoltUtil Protocol. Built by Developers, for Developers.
