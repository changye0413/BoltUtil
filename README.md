<div align="center">
  <img src="https://boltutil.com/logo.png" alt="BoltUtil Logo" width="120" />
  <h1>BoltUtil Protocol</h1>
  <p><b>面向开发者的非托管 USDT 支付网关</b></p>
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
  [![License](https://img.shields.io/badge/License-MIT-green)](https://boltutil.com)
  [![Uptime](https://img.shields.io/badge/Uptime-99.9%25-brightgreen)](https://boltutil.com)
  [![Fee](https://img.shields.io/badge/Fee-0%25-orange)](https://boltutil.com)
</div>

---

## 🛠️ 技术架构 (Technical Architecture)

BoltUtil 不存储资金，只负责“监听”和“通知”。我们通过分布式节点集群（Node Clusters）实时扫描多链网络。

- **多链支持**：原生兼容 **TRON (TRC20)**, **Ethereum (ERC20)** 和 **BNB Smart Chain (BEP20)**。
- **高精度处理**：针对 **BEP20 USDT** 的 18 位精度执行 `BigDecimal` 无损转换，确保 `11.508976` 等高精度订单 100% 匹配。

---

<a name="-简体中文"></a>
## 🇨🇳 简体中文
**面向开发者的非托管 USDT 支付网关。**
* **多链兼容**：完美支持 **USDT-TRC20**、**USDT-ERC20** 及 **USDT-BEP20** 协议。
* **绝对安全**：资金 P2P 直达您的钱包。没有平台资金池，杜绝“资金冻结”风险。
* **开发友好**：支持 Webhook 异步通知，采用 **HMAC-SHA256** 安全签名。
* **0 手续费**：平台不从交易中抽取佣金，您的利润 100% 归您。

<a name="-english"></a>
## 🇺🇸 English
**Enterprise-grade Non-Custodial USDT payment gateway.**
* **Multi-Chain Support**: Seamless integration for **USDT-TRC20**, **USDT-ERC20**, and **USDT-BEP20 (BSC)**.
* **Direct Settlement**: Funds flow directly from customer to your wallet. No middlemen, no custodial risk.
* **Precision Shield**: Specialized in handling the 18-decimal complexity of **BEP20** tokens to prevent order mismatches.
* **0% Transaction Fee**: Keep 100% of your revenue. We only charge for API usage.

<a name="-español"></a>
## 🇪🇸 Español
**Pasarela de pago USDT no custodiada para desarrolladores.**
* **Soporte Multicadena**: Compatible con protocolos **USDT (TRC20, ERC20, BEP20)**.
* **Sin Custodia**: Los fondos se transfieren directamente a su billetera privada. Evite bloqueos de cuentas.
* **Seguridad Avanzada**: Notificaciones Webhook protegidas por firmas HMAC-SHA256.
* **Comisión 0%**: Sin cargos por transacción, ideal para economías de escala.

<a name="-français"></a>
## 🇫🇷 Français
**Infrastructure de paiement USDT décentralisée.**
* **Compatibilité Étendue**: Prend en charge les standards **USDT-TRC20**, **ERC20** et **BEP20**.
* **P2P Réel**: Paiements directs de portefeuille à portefeuille. BoltUtil ne touche jamais à vos fonds.
* **Fiabilité**: Monitoring en temps réel des nœuds de blockchain pour une confirmation instantanée.
* **Frais Nuls**: Profitez d'une solution sans commission sur le volume des ventes.

<a name="-português"></a>
## 🇧🇷 Português
**Gateway de pagamento USDT descentralizado e seguro.**
* **Suporte Multi-Chain**: Integrado com redes **TRON (TRC20)**, **Ethereum (ERC20)** e **BSC (BEP20)**.
* **Custódia Zero**: O dinheiro cai direto na sua conta. Sem risco de plataforma ou congelamento de saldo.
* **Precisão de Dados**: Tratamento rigoroso de decimais para **USDT-BEP20**, garantindo conciliação perfeita.
* **Taxa 0%**: Sem cobrança de porcentagem sobre o faturamento.

<a name="-türkçe"></a>
## 🇹🇷 Türkçe
**Geliştiriciler için gözetimsiz (non-custodial) USDT ödeme altyapısı.**
* **Çoklu Ağ Desteği**: **USDT-TRC20**, **USDT-ERC20** ve **USDT-BEP20** protokolleriyle tam uyum.
* **Doğrudan Cüzdana**: Fonlar doğrudan sizin cüzdanınıza geçer. Aracı yok, bekleme süresi yok.
* **Güvenlik**: HMAC-SHA256 imzalı Webhook bildirimleri ile sahte ödemelere son.
* **%0 Komisyon**: İşlem başına ücret ödemeyin, kârınızı maksimize edin.

<a name="-tiếng-việt"></a>
## 🇻🇳 Tiếng Việt
**Cổng thanh toán USDT phi lưu ký dành cho nhà phát triển.**
* **Hỗ trợ đa chuỗi**: Tích hợp hoàn hảo **USDT (TRC20, ERC20, BEP20)**.
* **Thanh toán trực tiếp**: Tiền chuyển thẳng vào ví cá nhân của bạn. Không lo bị khóa tài khoản hoặc sàn sập.
* **Xử lý chính xác**: Thuật toán xử lý 18 chữ số thập phân của **BEP20** giúp khớp đơn hàng 100%.
* **Phí 0%**: Không thu phí chiết khấu giao dịch.

<a name="-pусский"></a>
## 🇷🇺 Русский
**Некастодиальный платежный шлюз USDT для разработчиков.**
* **Поддержка мультичейн**: Полная совместимость с **USDT-TRC20**, **USDT-ERC20** и **USDT-BEP20 (BSC)**.
* **Прямые расчеты**: Средства поступают сразу на ваш кошелек. Безопасность уровня блокчейн.
* **Точность**: Безошибочная обработка 18 знаков после запятой для транзакций **BEP20**.
* **0% комиссия**: Мы не берем процент с ваших продаж.

<a name="-بالعربية"></a>
## 🇸🇦 العربية
**بوابة دفع USDT غير احتجازية للمطورين التقنيين.**
* **دعم الشبكات المتعددة**: متوافق تماماً مع بروتوكولات **TRC20**, **ERC20**, و **BEP20**.
* **تسوية مباشرة**: تتدفق الأموال من العميل إلى محفظتك مباشرة. لا يوجد طرف ثالث يتحكم بأموالك.
* **دقة متناهية**: معالجة احترافية لـ 18 خانة عشرية لعملات **USDT-BEP20**.
* **عمولة 0%**: احتفظ بكامل أرباحك دون أي استقطاعات من المعاملات.

<a name="-हिन्दी"></a>
## 🇮🇳 हिन्दी
**डेवलपर्स के लिए नॉन-कस्टोडियल USDT पेमेंट गेटवे।**
* **मल्टी-चैन सपोर्ट**: **USDT-TRC20**, **USDT-ERC20**, और **USDT-BEP20** के लिए पूर्ण समर्थन।
* **सीधा सेटलमेंट**: फंड सीधे आपके निजी वॉलेट में जाता है। फंड फ्रीज होने का कोई डर नहीं।
* **सटीक डेटा**: **BEP20** की 18-दशमलव जटिलता को संभालने में माहिर।
* **0% लेनदेन शुल्क**: अपनी कमाई का 100% हिस्सा अपने पास रखें।

<a name="-日本語"></a>
## 🇯🇵 日本語
**開発者向け非管財型（ノンカストディアル）USDT決済ゲートウェイ。**
* **マルチチェーン対応**: **USDT-TRC20**、**ERC20**、および **BEP20 (BSC)** をシームレスに統合。
* **ダイレクト決済**: 資金は顧客からあなたのウォレットへ直接送金されます。プラットフォームによる凍結リスクなし。
* **高精度同期**: **BEP20** の18桁小数を正確に処理し、入金漏れを完全に防止します。
* **手数料 0%**: 取引手数料は一切かかりません。

<a name="-한국어"></a>
## 🇰🇷 한국어
**개발자를 위한 비수탁형(Non-Custodial) USDT 결제 인프라.**
* **멀티체인 지원**: **USDT-TRC20**, **USDT-ERC20**, **USDT-BEP20** 프로토콜 완벽 지원.
* **직접 정산**: 자금은 플랫폼을 거치지 않고 귀하의 지갑으로 즉시 입금됩니다.
* **정밀한 처리**: **BEP20**의 18자리 소수점 오차를 완벽히 해결하여 정확한 주문 매칭 보장.
* **수수료 0%**: 거래 수수료가 없어 비즈니스 수익성을 극대화합니다.

---

## 🔒 安全机制 (Security Features)

1. **分布式共识**：基于多节点确认，有效防御链上回滚攻击。
2. **签名验证**：所有回调均包含 `X-Bolt-Signature` (HMAC-SHA256)，确保数据未被篡改。
3. **精度护盾 (Precision Shield)**：专为 **BEP20** 打造的 `BigDecimal` 处理逻辑，杜绝精度丢失。

---

## 🌐 开发者资源
- **官网**: [boltutil.com](https://boltutil.com)
- **文档**: [docs.boltutil.com](https://boltutil.com/developer-docs)
- **API 状态**: [status.boltutil.com](https://boltutil.com)

---
© 2026 BoltUtil Protocol. Built by Developers, for Developers.
