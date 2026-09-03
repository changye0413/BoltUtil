# BoltUtil

[English](README.md) | [简体中文](README.zh-CN.md)

## 让 USDT 直接进入您的收款钱包

**BoltUtil 是面向网站、SaaS 和数字业务的非托管 USDT 支付 API 与托管收银台。** 商户后端创建订单，用户向商户配置的钱包支付精确金额，链上确认后 BoltUtil 向商户发送带签名的 Webhook。

[开始使用](https://boltutil.com/zh/auth/register?utm_source=github&utm_medium=referral&utm_campaign=boltutil_repo) · [开发者文档](https://boltutil.com/zh/developer-docs?utm_source=github&utm_medium=referral&utm_campaign=boltutil_repo) · [Node.js 示例](examples/node/boltutil-demo.js) · [集成问答](https://github.com/changye0413/BoltUtil/discussions)

![BoltUtil 非托管 USDT 支付网关](assets/boltutil-home.png)

## 核心能力

- **资金直达商户钱包：** BoltUtil 不要求私钥、助记词或提币权限。
- **五条网络统一接入：** TRON、Ethereum、BNB Smart Chain、Polygon 和 Solana 使用一致的订单、收银台与 Webhook 流程。
- **完整的支付运维能力：** 包括精确金额匹配、确认追踪、签名回调、投递日志、失败重试和人工对账。

BoltUtil 不是交易所、托管钱包或资金归集账户，而是把链上转账与商户业务订单连接起来的支付基础设施。

## 快速接入

1. [注册商户账户](https://boltutil.com/zh/auth/register?utm_source=github&utm_medium=referral&utm_campaign=boltutil_repo)。
2. 添加收款钱包并创建 API Key。
3. 配置 HTTPS Webhook 地址并保存签名密钥。
4. 由商户后端调用 `/api/v1/order/create` 创建订单。
5. 收到回调后先验证签名，再完成发货、充值或开通服务。

```json
{
  "externalOrderId": "ORDER-10001",
  "amount": "49.90",
  "currency": "USDT",
  "network": "TRC20",
  "notifyUrl": "https://merchant.example.com/webhooks/boltutil",
  "returnUrl": "https://merchant.example.com/orders/10001"
}
```

建单响应会返回精确应付金额、收款地址、订单令牌、过期时间和收银台地址。商户必须展示 BoltUtil 返回的应付金额，不能自行取整。

## 支持的 USDT 网络

| API 参数 | 网络 | 代币标准 |
| --- | --- | --- |
| `TRC20` | TRON | TRC20 USDT |
| `ERC20` | Ethereum | ERC20 USDT |
| `BEP20` | BNB Smart Chain | BEP20 USDT |
| `POLYGON` | Polygon PoS | ERC20 兼容 USDT |
| `SOLANA` | Solana | SPL-USDT |

## 公开仓库范围

本仓库是 BoltUtil 的**公开产品说明与商户集成入口**，包含 Node.js、Python、PHP、Go、Java 和 C# 示例。生产平台源代码和私有基础设施属于闭源商业系统，不包含在本仓库中。

公开文档和示例使用 [MIT License](LICENSE)。该许可证仅适用于本仓库公开的文件，不适用于 BoltUtil 的闭源平台、商标、后台、前端、基础设施或托管服务。

## 安全要求

- 使用收到的原始请求体校验 `X-Bolt-Webhook-Signature`。
- 校验 `X-Bolt-Webhook-Timestamp`，拒绝过期回调。
- 将商户订单号、网络、金额和状态与本地记录比对。
- 履约逻辑必须幂等，避免重试造成重复交付。
- API Key 和 Webhook Secret 只能保存在服务端。

## 获取帮助

- 集成问题和产品建议：[GitHub Discussions](https://github.com/changye0413/BoltUtil/discussions)
- 可复现的文档或示例问题：[GitHub Issues](https://github.com/changye0413/BoltUtil/issues/new/choose)
- 开发者文档：[boltutil.com/zh/developer-docs](https://boltutil.com/zh/developer-docs?utm_source=github&utm_medium=referral&utm_campaign=boltutil_repo)
- 安全问题：按照 [SECURITY.md](SECURITY.md) 私下报告
