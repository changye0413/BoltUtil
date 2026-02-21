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

BoltUtil 不存储资金，只负责“监听”和“通知”。我们通过分布式节点集群（Node Clusters）实时扫描 TRON、Ethereum 和 BSC 等主流公链。



### 核心运作流程：
1. **API 调用**：服务端发起 `POST /v1/order/create`。
2. **唯一标识**：系统为每笔订单分配唯一的付款金额（微小偏移）或临时地址。
3. **链上确认**：BoltUtil 节点确认交易哈希（Transaction Hash）及其确认数。
4. **安全回调**：通过 **HMAC-SHA256** 签名的 Webhook 通知您的服务器。

---

<a name="-简体中文"></a>
## 🇨🇳 简体中文：深度解析

### 💡 为什么选择 BoltUtil？
传统的支付网关是“资金池”模式，而 BoltUtil 是“广播监听”模式。
* **绝对安全**：资金从用户钱包 **直达** 您的钱包。没有中间账户，不存在“平台跑路”或“资金冻结”。
* **开发友好**：提供预构建的收银台 UI，只需一个 `window.location.href` 即可完成集成。
* **全球合规**：无需 KYC，保护隐私，适合去中心化应用（dApps）和跨境贸易。

### 🌟 核心优势
* **0 手续费**：平台不抽取交易百分比，仅对 API 调用配额计费。
* **秒级响应**：自研节点集群，确保链上到账后 1-3 秒内触发回调。

---

<a name="-english"></a>
## 🇺🇸 English: Deep Dive

### 💡 Why BoltUtil?
Traditional gateways are "Middlemen." BoltUtil is a "Listener."
* **Zero Trust**: Funds flow P2P (Peer-to-Peer). We never touch your private keys or your money.
* **Developer Centric**: RESTful APIs, comprehensive documentation, and SDKs for rapid deployment.
* **Non-Custodial**: Your assets remain under your control at all times.

### 🌟 Key Performance
* **Reliability**: 99.9% uptime with redundant nodes across multiple regions.
* **Security**: Webhooks are secured with HMAC signatures to prevent spoofing attacks.

---

<a name="-español"></a>
## 🇪🇸 Español
**Pasarela de pago USDT no custodiada.** Diseñada para desarrolladores que buscan autonomía.
* **Liquidación Directa**: El dinero llega a tu billetera personal sin intermediarios.
* **Sin KYC**: Privacidad total para operaciones globales.

<a name="-français"></a>
## 🇫🇷 Français
**Infrastructure de paiement USDT décentralisée.** * **Sécurité Maximale**: Aucun risque de gel des fonds car BoltUtil ne détient jamais vos actifs.
* **Intégration Rapide**: Checkout prêt à l'emploi adaptable sur mobile et desktop.

<a name="-português"></a>
## 🇧🇷 Português
**Gateway de pagamento USDT descentralizado.**
* **Taxas Zero**: Não cobramos porcentagem sobre suas vendas.
* **P2P Real**: Transferências diretas na blockchain, monitoradas em tempo real.

<a name="-türkçe"></a>
## 🇹🇷 Türkçe
**Gözetimsiz kripto ödeme altyapısı.**
* **Doğrudan Cüzdana**: Fonlar platformda beklemez, anında cüzdanınıza geçer.
* **Kolay Entegrasyon**: Modern API ve dökümantasyon desteği.

<a name="-tiếng-việt"></a>
## 🇻🇳 Tiếng Việt
**Cổng thanh toán USDT phi lưu ký dành cho nhà phát triển.**
* **Không giữ tiền**: Tiền chuyển thẳng vào ví của bạn, loại bỏ rủi ro sàn sập.
* **Phí 0%**: Tối ưu hóa lợi nhuận cho doanh nghiệp của bạn.

<a name="-pусский"></a>
## 🇷🇺 Русский
**Некастодиальный шлюз для приема USDT.**
* **Прямые расчеты**: Деньги сразу приходят на ваш кошелек.
* **Безопасность**: Подтверждение транзакций через распределенную сеть узлов.

<a name="-بالعربية"></a>
## 🇸🇦 العربية
**بوابة دفع USDT غير احتجازية للمطورين.**
* **بدون وسيط**: تصل الأموال إلى محفظتك الشخصية فوراً.
* **0% رسوم**: احتفظ بكامل أرباحك دون عمولات خفية.

<a name="-हिन्दी"></a>
## 🇮🇳 हिन्दी
**डेवलपर्स के लिए नॉन-कस्टोडियल पेमेंट गेटवे।**
* **सीधा भुगतान**: फंड सीधे आपके वॉलेट में जाता है।
* **कोई केवाईसी नहीं**: पूर्ण गोपनीयता और वैश्विक पहुंच।

<a name="-日本語"></a>
## 🇯🇵 日本語
**開発者向け非管財型（ノンカストディアル）USDT決済ゲートウェイ。**
* **資金凍結リスクゼロ**: プラットフォームを通さず、直接ウォレットへ送金されます。
* **高機能API**: Webhookによる即時通知とセキュアな署名検証。

<a name="-한국어"></a>
## 🇰🇷 한국어
**개발자를 위한 비수탁형 USDT 결제 인프라.**
* **직접 정산**: 자산은 항상 귀하의 통제하에 있으며, 지갑으로 직접 입금됩니다.
* **0% 수수료**: 거래 금액에서 수수료를 차감하지 않습니다.

---

## 🔒 安全机制 (Security Features)

为了防止假充值和回滚攻击，BoltUtil 采用了以下策略：



1. **多节点共识**：至少 3 个节点确认链上高度变化才触发回调。
2. **HMAC 签名**：每条通知包含 `X-Bolt-Signature`，防止恶意伪造。
3. **防止重放**：包含时间戳校验，确保请求具有唯一性。

---

## 🌐 开发者资源
- **官网**: [boltutil.com](https://boltutil.com)
- **文档**: [docs.boltutil.com](https://boltutil.com/developer-docs)
- **API 状态**: [status.boltutil.com](https://boltutil.com)

---
© 2026 BoltUtil Protocol. Built by Developers, for Developers.
