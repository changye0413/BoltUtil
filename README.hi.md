# BoltUtil v2.1

[English](README.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [Tiếng Việt](README.vi.md) · [Türkçe](README.tr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md)

## USDT और USDC भुगतान सीधे आपके वॉलेट में।

[मुफ़्त शुरू करें](https://boltutil.com/hi/auth/register?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=start) · [API दस्तावेज़](https://boltutil.com/hi/developer-docs?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=docs) · [कीमतें](https://boltutil.com/hi/pricing?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=pricing)

BoltUtil v2.1 वेबसाइट, SaaS और WooCommerce स्टोर के लिए एक नॉन-कस्टोडियल स्टेबलकॉइन भुगतान API और होस्ट किया गया चेकआउट है। व्यापारी का सर्वर ऑर्डर बनाता है और ग्राहक व्यापारी के पते पर भुगतान करता है। BoltUtil ऑन-चेन ट्रांसफ़र और आवश्यक पुष्टियों की जाँच के बाद हस्ताक्षरित Webhook भेजता है। यह निजी कुंजी या रिकवरी फ़्रेज़ नहीं माँगता।

## नेटवर्क और एसेट

एक इंटीग्रेशन में छह नेटवर्क और ग्यारह एसेट/नेटवर्क संयोजन हैं। TRON पर USDT; Ethereum, Polygon PoS और Solana पर USDT व नेटिव USDC; BNB Smart Chain पर USDT व Binance-Peg USDC; Base पर Bridged USDT व नेटिव USDC उपलब्ध हैं। केवल सेवा द्वारा सक्रिय और व्यापारी के सक्रिय प्राप्तकर्ता पते वाले रूट दिखते हैं। नेटिव, ब्रिज्ड और पेग्ड टोकन एक-दूसरे के विकल्प नहीं हैं; ऑर्डर का सही कॉन्ट्रैक्ट या mint इस्तेमाल करें। Base की पुष्टि कॉन्फ़िगर की गई L1 फ़ाइनलिटी नीति पर निर्भर है; निश्चित समय की गारंटी नहीं है।

## वॉलेट भुगतान या मैनुअल ट्रांसफ़र

पता, नेटवर्क और सटीक राशि अपने आप भरी जाती है। ग्राहक वॉलेट जोड़कर जानकारी जाँचता है और पुष्टि करता है। मैनुअल ट्रांसफ़र, QR और पता कॉपी करना भी उपलब्ध है। MetaMask, OKX Wallet, Trust Wallet, Phantom, TronLink, Bitget Wallet, Binance Wallet, TokenPocket, SafePal और Base app के विकल्प नेटवर्क और डिवाइस पर निर्भर हैं। कुछ ऐप के ब्राउज़र में ऑर्डर खोलते हैं; सभी फ़ोन और डेस्कटॉप सेशन को QR से पेयर नहीं करते। वॉलेट जोड़ने से पैसे नहीं भेजे जाते। पहली बार अनलॉक, अनुमति या नेटवर्क बदलना पड़ सकता है; नेटवर्क फ़ीस के लिए नेटिव कॉइन चाहिए।

## इंटीग्रेशन शुरू करें

1. खाता बनाएँ, प्राप्तकर्ता पते सक्रिय करें और LIVE API Key बनाएँ।
2. उसी व्यापारी खाते में HTTPS Webhook सेट करें; सीक्रेट सर्वर पर रखें।
3. ऑर्डर बनाएँ और लौटाया गया `checkoutUrl` खोलें।
4. `payment.amount` बिना राउंड किए दिखाएँ; एक साथ बने ऑर्डर अलग पहचानने के लिए राशि में थोड़ा अंतर हो सकता है।
5. हस्ताक्षर, timestamp, ऑर्डर, टोकन, नेटवर्क और पुष्ट स्थिति जाँचें। ऑर्डर केवल एक बार पूरा करें।

API की न्यूनतम राशि 1 है और अधिकतम छह दशमलव स्थान हैं। Node.js, Python, PHP, Go, Java और C# उदाहरणों में USDT डिफ़ॉल्ट है; USDC के लिए अधिकृत जोड़ी चुनें। OpenAPI और Postman भी हैं।

## WooCommerce और योजनाएँ

अलग प्लगइन v0.6.1 टोकन और नेटवर्क चुनने देता है, और भुगतान जाँचने के बाद ऑर्डर अपडेट करता है। स्टोर पर लौटना भुगतान का प्रमाण नहीं है। WordPress 7.0+, PHP 7.4+, WooCommerce 11.1+, HTTPS और स्टोर मुद्रा USD चाहिए; लाइव विनिमय दर या रेट लॉक नहीं मिलता। 12 अक्टूबर 2026 को WordPress.org में जमा किया गया: ऑटोमैटिक स्कैन पास, मैनुअल समीक्षा लंबित। डायरेक्टरी में प्रकाशन तक GitHub Releases का ZIP इस्तेमाल करें। डेमो स्टोर की खरीद में वास्तविक पैसे लगते हैं।

दैनिक मुफ़्त ऑर्डर कोटा और दैनिक ऑर्डर सीमा के बिना सब्सक्रिप्शन उपलब्ध हैं। मौजूदा कोटा, लाभ और शुल्क आधिकारिक साइट पर देखें; नेटवर्क फ़ीस अलग है। कम, देर से या अस्पष्ट भुगतान की समीक्षा चाहिए। BoltUtil एक्सचेंज नहीं है और अपने आप फ़िएट में नहीं बदलता।

इस रिपॉज़िटरी के दस्तावेज़ और उदाहरण MIT हैं; प्रोडक्शन प्लेटफ़ॉर्म का स्रोत निजी है। प्लगइन GPLv2 या बाद का है। ब्रांड नाम आधिकारिक समर्थन नहीं दर्शाते। अंग्रेज़ी गाइड और API तकनीकी आधार हैं। सीक्रेट सार्वजनिक न करें; सुरक्षा समस्याओं के लिए SECURITY.md देखें।

[USDC गाइड](https://boltutil.com/hi/docs/usdc-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [Base गाइड](https://boltutil.com/hi/docs/base-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [WooCommerce प्लगइन](https://github.com/changye0413/boltutil-payments-for-woocommerce) · [डेमो स्टोर](https://shop-test.boltutil.com/)

[सहायता और उदाहरण](examples/README.md) · [OpenAPI](openapi.yaml) · [Postman](postman/BoltUtil.postman_collection.json) · [Discussions](https://github.com/changye0413/BoltUtil/discussions) · [support@boltutil.com](mailto:support@boltutil.com) · [X: @heyharryzhang](https://x.com/heyharryzhang) · [English](README.md)
