<div align="center">
  <a href="https://boltutil.com">
    <img src="https://boltutil.com/logo.png" width="120" alt="BoltUtil Logo" />
  </a>
  <h1>BoltUtil Protocol</h1>
  <p><b>面向开发者的非托管 USDT 支付网关 | The Non-Custodial USDT Payment Gateway for Developers</b></p>

  <p>
    <a href="#-简体中文">简体中文</a> | 
    <a href="#-english">English</a>
  </p>

  [![Website](https://img.shields.io/badge/Website-boltutil.com-blue)](https://boltutil.com)
  [![Status](https://img.shields.io/badge/Service-Online-success)](https://boltutil.com)
  [![License](https://img.shields.io/badge/Fee-0%25-orange)](https://boltutil.com)
</div>

---

<a name="-简体中文"></a>
## 🇨🇳 简体中文

### 💡 BoltUtil 是什么？

**BoltUtil** 是一款专为开发者设计的**USDT 收款工具**。

你可以把它理解为一个**“智能的链上会计”**。传统的支付平台会把钱收进平台账户，再结算给你（有跑路风险）；而 BoltUtil **完全不同** —— 我们只负责监控区块链数据。

当用户付款时，资金**直接进入你的个人钱包**。我们监控到到账后，立即通过 API 通知你的服务器发货。

### 🌟 核心优势

* ✅ **0 手续费**：你的钱就是你的，我们不从交易金额中抽成。
* ✅ **资金直达 (非托管)**：配置你的 TRC20/ERC20 钱包地址，资金直达，无中间商，**绝无跑路风险**。
* ✅ **无需 KYC**：不需要复杂的实名认证或公司资质，保护隐私，初始化即可全球收款。
* ✅ **自带收银台**：无需前端开发！调用 API 即可获得一个专业的收银页面（支持移动端/PC端）。
* ✅ **标准 API**：简单的接口设计，几行代码即可对接现有系统。

### 📸 界面概览

为了让您直观了解 BoltUtil，我们准备了以下核心界面演示：

#### 1. 首页 (Home)
> 极简设计，一键开启 Web3 收款之旅。
![Home](assets/home.jpg)

#### 2. 商户控制台 (Console)
> 清晰的数据面板，实时查看订单状态、配置回调地址。
![Console](assets/console.jpg)

#### 3. 开发者文档 (Docs)
> 详尽的接口文档，包含代码示例，助您 5 分钟完成集成。
![Docs](assets/docs.jpg)

#### 4. 标准收银台 (Checkout)
> 无需您编写任何前端代码，直接使用的标准化收银页面，转化率极高。
![Checkout](assets/checkout.jpg)

### 🚀 它是如何工作的？

1.  **发起订单**：你的服务器调用 BoltUtil API 创建订单。
2.  **用户付款**：用户在收银台扫描二维码，向**你的钱包**转账。
3.  **自动识别**：BoltUtil 系统毫秒级识别链上交易。
4.  **回调通知**：我们通过 Webhook (POST请求) 告诉你的服务器：“钱到了，请发货”。

---

<a name="-english"></a>
## 🇺🇸 English

### 💡 What is BoltUtil?

**BoltUtil** is a **non-custodial USDT payment tool** designed specifically for developers.

Think of it as a **"Smart On-Chain Accountant."** Unlike traditional gateways that hold your funds, BoltUtil is different. We only monitor the blockchain.

When a user pays, the funds go **directly to your personal wallet**. Once we detect the transaction, we instantly notify your server via API to fulfill the order.

### 🌟 Key Features

* ✅ **0% Fees**: We do not take a cut from your transaction volume.
* ✅ **Direct Settlement (Non-Custodial)**: Funds go straight to your wallet. We never touch your assets. **Zero platform risk.**
* ✅ **No KYC**: No complex identity verification required. Privacy-first and global ready.
* ✅ **Ready-to-Use Checkout**: No frontend coding needed! Get a professional payment page instantly via API.
* ✅ **Standard API**: Developer-friendly integration in minutes.

### 📸 Visual Interface

#### 1. Homepage
> Minimalist design to start your crypto journey.
![Home](assets/home.jpg)

#### 2. Merchant Console
> Real-time dashboard to monitor orders and configure Webhooks.
![Console](assets/console.jpg)

#### 3. Developer Docs
> Comprehensive guides with code snippets for quick integration.
![Docs](assets/docs.jpg)

#### 4. Standard Checkout
> A high-conversion payment page ready for mobile and desktop.
![Checkout](assets/checkout.jpg)

### 🚀 How It Works

1.  **Create Order**: Your server calls the BoltUtil API.
2.  **User Pays**: User scans the QR code on the checkout page and pays directly to **your wallet**.
3.  **Auto-Detect**: BoltUtil monitors the blockchain network in real-time.
4.  **Webhook**: We send a POST request to your server confirming the payment.

---

## 🛠 Integration Example (集成示例)

```json
// Webhook Payload Example
// 当用户支付成功后，您的服务器会收到如下数据：
{
  "order_id": "ORD_20260217_001",
  "status": "PAID",
  "amount": "100.00",
  "currency": "USDT",
  "hash": "0x123...abc",
  "timestamp": 1771234567
}
