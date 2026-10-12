# BoltUtil v2.1

[English](README.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [Tiếng Việt](README.vi.md) · [Türkçe](README.tr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md)

## USDT ve USDC ödemeleri doğrudan cüzdanınıza.

[Ücretsiz başlayın](https://boltutil.com/tr/auth/register?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=start) · [API belgeleri](https://boltutil.com/tr/developer-docs?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=docs) · [Fiyatlar](https://boltutil.com/tr/pricing?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=pricing)

BoltUtil v2.1; web siteleri, SaaS ürünleri ve WooCommerce mağazaları için saklama hizmeti sunmayan bir stablecoin ödeme API’si ve barındırılan ödeme sayfasıdır. Sunucunuz siparişi oluşturur, müşteri satıcının adresine ödeme yapar. BoltUtil zincir üzerindeki transferi ve onayları doğruladıktan sonra imzalı Webhook gönderir. Özel anahtar veya kurtarma ifadesi istemez.

## Ağlar ve varlıklar

Tek entegrasyon altı ağı ve on bir varlık/ağ çiftini kapsar. TRON’da USDT; Ethereum, Polygon PoS ve Solana’da USDT ile yerel USDC; BNB Smart Chain’de USDT ile Binance-Peg USDC; Base’de Bridged USDT ile yerel USDC desteklenir. Yalnızca hizmetin etkinleştirdiği ve aktif alıcı adresi bulunan yollar görünür. Yerel, köprülenmiş ve sabitlenmiş tokenlar birbirinin yerine kullanılamaz; siparişin sözleşmesini veya mint adresini kontrol edin. Base onayı yapılandırılmış L1 kesinleşme politikasına bağlıdır; sabit süre vaat edilmez.

## Cüzdanla ödeme veya manuel transfer

Adres, ağ ve tam tutar otomatik doldurulur. Müşteri cüzdanını bağlar, bilgileri kontrol eder ve onaylar. Manuel transfer, QR ve adres kopyalama da vardır. MetaMask, OKX Wallet, Trust Wallet, Phantom, TronLink, Bitget Wallet, Binance Wallet, TokenPocket, SafePal ve Base app seçenekleri ağ ve cihaza göre değişir. Bazıları siparişi uygulama tarayıcısında açar; hepsi QR ile telefon/masaüstü oturumu eşleştirmez. Bağlantı kurmak para göndermez. İlk kullanımda kilit açma, bağlantı izni veya ağ değişimi gerekebilir; ağ ücreti için yerel coin gerekir.

## Entegrasyona başlayın

1. Hesap oluşturun, alıcı adreslerini etkinleştirin ve LIVE API Key üretin.
2. Aynı hesapta HTTPS Webhook yapılandırın; sırrı sunucuda tutun.
3. Sipariş oluşturup dönen `checkoutUrl` adresini açın.
4. `payment.amount` değerini yuvarlamadan gösterin; eşzamanlı siparişleri ayırmak için küçük bir fark olabilir.
5. İmza, timestamp, sipariş, token, ağ ve doğrulanmış durumu kontrol edin. Sipariş yalnızca bir kez tamamlanmalıdır.

API en az 1 ve en fazla altı ondalık basamak kabul eder. Node.js, Python, PHP, Go, Java ve C# örnekleri varsayılan olarak USDT kullanır; USDC için izin verilen çifti seçin. OpenAPI ve Postman mevcuttur.

## WooCommerce ve planlar

Ayrı v0.6.1 eklentisi token ve ağ seçimi sunar, siparişi güncellemeden ödemeyi doğrular. Mağazaya dönüş ödeme kanıtı değildir. WordPress 7.0+, PHP 7.4+, WooCommerce 11.1+, HTTPS ve mağaza para birimi USD gerekir; canlı döviz kuru veya kur kilidi sunulmaz. 12 Ekim 2026’da WordPress.org’a gönderildi: otomatik tarama başarılı, manuel inceleme bekleniyor. GitHub Releases ZIP paketini kullanın. Demo mağazasındaki ödemeler gerçek fonlarla yapılır.

Günlük ücretsiz kota ve günlük sipariş sınırı olmayan abonelikler bulunur. Güncel kota, özellik ve ücretler resmi sitededir; ağ ücretleri ayrıdır. Eksik, geç veya belirsiz ödemeler inceleme gerektirir. BoltUtil borsa değildir ve otomatik fiat dönüşümü yapmaz.

Bu depo MIT belgeleri ve örnekleridir; üretim platformu kapalı kaynaklıdır. Eklenti GPLv2 veya üstüdür. Marka adları onay anlamına gelmez. Teknik temel İngilizce rehber ve API referansıdır. Sırları paylaşmayın; güvenlik sorunları için SECURITY.md kullanın.

[USDC rehberi](https://boltutil.com/tr/docs/usdc-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [Base rehberi](https://boltutil.com/tr/docs/base-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [WooCommerce eklentisi](https://github.com/changye0413/boltutil-payments-for-woocommerce) · [Canlı demo](https://shop-test.boltutil.com/)

[Destek ve örnekler](examples/README.md) · [OpenAPI](openapi.yaml) · [Postman](postman/BoltUtil.postman_collection.json) · [Discussions](https://github.com/changye0413/BoltUtil/discussions) · [support@boltutil.com](mailto:support@boltutil.com) · [X: @heyharryzhang](https://x.com/heyharryzhang) · [English](README.md)
