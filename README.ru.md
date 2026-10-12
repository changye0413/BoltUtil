# BoltUtil v2.1

[English](README.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [Tiếng Việt](README.vi.md) · [Türkçe](README.tr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md)

## Принимайте USDT и USDC напрямую на свой кошелёк.

[Начать бесплатно](https://boltutil.com/ru/auth/register?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=start) · [Документация API](https://boltutil.com/ru/developer-docs?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=docs) · [Тарифы](https://boltutil.com/ru/pricing?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=pricing)

BoltUtil v2.1 — API платежей в стейблкоинах и размещённая платёжная страница без хранения средств платформой. Подходит для сайтов, SaaS и магазинов WooCommerce. Сервер продавца создаёт заказ; клиент переводит средства на адрес продавца. После проверки перевода и подтверждений BoltUtil отправляет подписанный Webhook. Приватные ключи и seed-фразы не требуются.

## Сети и активы

Шесть сетей, один процесс интеграции и одиннадцать сочетаний актив/сеть. TRON поддерживает USDT. Ethereum, Polygon PoS и Solana — USDT и нативный USDC. BNB Smart Chain — USDT и Binance-Peg USDC. Base — Bridged USDT и нативный USDC. Доступны только включённые сервисом маршруты с активным адресом продавца. Нативные, мостовые и привязанные токены не взаимозаменяемы: проверяйте контракт или mint заказа. Подтверждение Base зависит от настроенной политики финальности L1; фиксированный срок не гарантируется.

## Подключение кошелька или ручной перевод

Адрес, сеть и точная сумма заполняются автоматически; клиент проверяет и подтверждает операцию в кошельке. Ручной перевод, QR-код и копирование адреса сохранены. MetaMask, OKX Wallet, Trust Wallet, Phantom, TronLink, Bitget Wallet, Binance Wallet, TokenPocket, SafePal и Base app отображаются в зависимости от сети и устройства. Часть вариантов открывает заказ во встроенном браузере приложения; не все поддерживают сопряжение телефона с компьютером по QR. Подключение не переводит средства. Могут потребоваться разблокировка, разрешение и смена сети; комиссии оплачиваются её нативной монетой.

## Начало работы

1. Создайте аккаунт, включите адреса приёма и создайте LIVE API Key.
2. Настройте HTTPS Webhook в том же аккаунте. Храните секрет на сервере.
3. Создайте заказ и откройте полученный `checkoutUrl`.
4. Покажите `payment.amount` без округления: сумма может немного отличаться для различения одновременных заказов.
5. Проверьте подпись, timestamp, заказ, актив, сеть и подтверждённый статус. Выполняйте заказ только один раз.

Минимальная сумма API — 1, максимум шесть знаков после запятой. Примеры Node.js, Python, PHP, Go, Java и C# по умолчанию используют USDT. Для USDC выберите разрешённую пару. Доступны OpenAPI и Postman.

## WooCommerce и тарифы

Отдельный плагин v0.6.1 предлагает выбор валюты и сети. Он проверяет платёж до обновления заказа; возврат в магазин не подтверждает оплату. Требуются WordPress 7.0+, PHP 7.4+, WooCommerce 11.1+, HTTPS и валюта магазина USD. Котировка или фиксация обменного курса не предоставляется. 12 октября 2026 года плагин отправлен в WordPress.org: автоматическая проверка пройдена, ручная проверка ожидается. До публикации используйте ZIP из GitHub Releases. Покупки в демонстрационном магазине используют реальные средства.

Есть ежедневная бесплатная квота и подписки без дневного ограничения заказов. Актуальные условия и цены опубликованы на сайте; сетевые комиссии оплачиваются отдельно. Неполные, поздние и неоднозначные платежи требуют проверки. BoltUtil не является биржей и не конвертирует средства автоматически в фиат.

Публичные документы и примеры лицензированы по MIT, производственная платформа закрытая. Плагин — GPLv2 или новее. Названия брендов не означают одобрение. Техническая основа — английское руководство и API. Не публикуйте секреты; уязвимости сообщайте по SECURITY.md.

[Руководство USDC](https://boltutil.com/ru/docs/usdc-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [Руководство Base](https://boltutil.com/ru/docs/base-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [Плагин WooCommerce](https://github.com/changye0413/boltutil-payments-for-woocommerce) · [Демонстрационный магазин](https://shop-test.boltutil.com/)

[Поддержка и примеры](examples/README.md) · [OpenAPI](openapi.yaml) · [Postman](postman/BoltUtil.postman_collection.json) · [Discussions](https://github.com/changye0413/BoltUtil/discussions) · [support@boltutil.com](mailto:support@boltutil.com) · [X: @heyharryzhang](https://x.com/heyharryzhang) · [English](README.md)
