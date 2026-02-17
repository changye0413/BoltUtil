<div align="center">
  <img src="https://boltutil.com/logo.png" width="120" alt="BoltUtil Logo" />
  <h1>BoltUtil Protocol</h1>
  <p><b>面向开发者的非托管 USDT 支付网关 | Non-Custodial USDT Payment Gateway for Developers</b></p>

  <p>
    <a href="#simplified-chinese">简体中文</a> | 
    <a href="#english">English</a>
  </p>

  [![Website](https://img.shields.io/badge/Official-Website-blue)](https://boltutil.com)
  [![Status](https://img.shields.io/badge/Service-Online-brightgreen)](https://boltutil.com)
  [![Network](https://img.shields.io/badge/Network-TRC20%20%7C%20ERC20-7B61FF)](https://boltutil.com)
  [![Fee](https://img.shields.io/badge/Fee-0%25-orange)](https://boltutil.com)
</div>

---

<a name="simplified-chinese"></a>
## 🇨🇳 简体中文

### 💡 什么是 BoltUtil？
**BoltUtil** 是一个专为现代开发者设计的**非托管**加密货币收款协议。我们不是资金的中转站，而是一个**智能链上哨兵**。

传统的支付网关会托管您的资金，而 BoltUtil 回归了区块链的本质：**资金直达您的钱包**。我们只负责实时监听地址，并在收到款项后通过 Webhook 第一时间通知您的业务系统。

### 📸 视觉演示 (界面预览)

#### 1. 现代化首页 (Home)
> 极简设计，5 分钟开启您的全球收款之旅。
![首页预览](https://raw.githubusercontent.com/changye0413/BoltUtil/main/assets/index.png)

#### 2. 强大的商户控制台 (Merchant Console)
> 实时监控订单状态、管理结算钱包与 API 密钥。
![控制台预览](https://raw.githubusercontent.com/changye0413/BoltUtil/main/assets/dashboard.png)

#### 3. 极简收银台页面 (Checkout UI)
> 标准化收银页面，适配移动端，无需自行开发前端界面，直接调用。
![收银台预览](https://raw.githubusercontent.com/changye0413/BoltUtil/main/assets/checkout.jpg)

#### 4. 开发者文档 (Developer Docs)
> 标准 RESTful API，提供详细的快速集成指南。
![文档预览](https://raw.githubusercontent.com/changye0413/BoltUtil/main/assets/doc.png)

### 🌟 为什么选择 BoltUtil？
* **0 手续费**: 我们不从您的交易中抽成，仅收取基础服务费或完全免费。
* **资金非托管 (P2P)**: 资金直接进入您的私人钱包（如 MetaMask, Trust Wallet），我们从不接触您的私钥，**没有跑路风险**。
* **无需 KYC**: 隐私至上。无需繁琐的身份审核，仅需邮箱和收款地址即可开始。
* **秒级回调**: 全球分布式节点监控，确保入账后亚秒级触发 Webhook。
* **去中心化**: 核心逻辑基于链上数据校验，防止假充值攻击。

---

<a name="english"></a>
## 🇺🇸 English

### 🚀 What is BoltUtil?
**BoltUtil** is a high-performance, **non-custodial** cryptocurrency payment protocol designed for developers. We are not a fund intermediary, but a **Smart On-chain Sentinel**.

Unlike traditional gateways that hold your funds, BoltUtil settles directly to your wallet. We monitor your addresses in real-time and notify your system via Webhooks the moment a transaction is confirmed.

### 📸 Visual Interface

#### 1. Modern Homepage
> Minimalist design to start your global payment journey in 5 minutes.
![Home Preview](https://raw.githubusercontent.com/your-username/your-repo/main/assets/home.jpg)

#### 2. Powerful Merchant Console
> Monitor order status, manage settlement wallets, and API keys in real-time.
![Console Preview](https://raw.githubusercontent.com/your-username/your-repo/main/assets/console.jpg)

#### 3. Standardized Checkout UI
> Responsive, mobile-ready checkout page. No need for frontend development; call it directly.
![Checkout Preview](https://raw.githubusercontent.com/your-username/your-repo/main/assets/checkout.jpg)

#### 4. Developer Documentation
> Standard RESTful API with a comprehensive quick-start guide.
![Docs Preview](https://raw.githubusercontent.com/your-username/your-repo/main/assets/docs.jpg)

### 🌟 Why BoltUtil?
* **0% Transaction Fee**: We don't take a cut from your payments.
* **Non-Custodial (P2P)**: Funds go directly to your wallet. We never touch your private keys—**Zero platform risk**.
* **No KYC Required**: Privacy-first. Start accepting payments with just an email and a public address.
* **Instant Webhooks**: Distributed global nodes ensure sub-second notification latency.
* **Standardized API**: RESTful endpoints designed by developers, for developers.

---

## 🛠 快速集成 (Quick Integration)

只需 4 步，即可完成集成：

1.  **创建订单 (Create Order)**: 通过后端调用 `/api/v1/orders/create`。
2.  **展示页面 (Display UI)**: 将用户重定向至我们的**标准收银台**。
3.  **链上监控 (On-chain Monitoring)**: 我们的节点集群实时扫描区块链。
4.  **接收回调 (Webhook)**: 您的服务器收到 `POST` 请求后完成发货。

```json
// Webhook 示例数据
{
  "order_id": "ORDER_12345",
  "status": "CONFIRMED",
  "amount": "9.90",
  "hash": "0xabc...123",
  "network": "TRC20"
}
