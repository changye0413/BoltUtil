# BoltUtil v2.1

[English](README.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [Tiếng Việt](README.vi.md) · [Türkçe](README.tr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md)

## Pagos USDT y USDC, directamente a tu cartera.

[Empezar gratis](https://boltutil.com/es/auth/register?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=start) · [Documentación API](https://boltutil.com/es/developer-docs?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=docs) · [Precios](https://boltutil.com/es/pricing?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=pricing)

BoltUtil v2.1 es una API de pagos con stablecoins y una página de pago alojada, sin custodia, para sitios web, SaaS y tiendas WooCommerce. Tu servidor crea el pedido; el cliente paga a la dirección del comerciante. BoltUtil verifica la transferencia y las confirmaciones antes de enviar un Webhook firmado. No solicita claves privadas ni frases de recuperación.

## Novedades y redes

Una integración cubre seis redes y once combinaciones de activo/red. TRON admite USDT. Ethereum, Polygon PoS y Solana admiten USDT y USDC nativo. BNB Smart Chain admite USDT y Binance-Peg USDC. Base admite Bridged USDT y USDC nativo. Solo se muestran las rutas activadas por el servicio con una dirección receptora activa. Los tokens nativos, puenteados y vinculados no son intercambiables: utiliza el contrato o mint indicado en el pedido. Base requiere la política configurada de finalidad L1; no se promete un tiempo fijo.

## Confirmación en la cartera o transferencia manual

La opción de pago con cartera rellena la dirección, red y cantidad exacta. El cliente conecta su cartera, revisa y confirma. La transferencia manual, el QR y la copia de dirección siguen disponibles. MetaMask, OKX Wallet, Trust Wallet, Phantom, TronLink, Bitget Wallet, Binance Wallet, TokenPocket, SafePal y Base app tienen entradas según la red y el dispositivo. Algunas abren el pedido dentro del navegador de la aplicación; no todas emparejan el teléfono con el escritorio mediante QR. Conectar no envía fondos. Puede ser necesario desbloquear, autorizar o cambiar de red, y disponer de moneda nativa para las comisiones.

## Integración

1. Crea una cuenta, activa las direcciones receptoras y genera una API Key LIVE.
2. Configura un Webhook HTTPS en la misma cuenta y conserva el secreto en tu servidor.
3. Crea el pedido y abre el `checkoutUrl` devuelto.
4. Muestra `payment.amount` completo, sin redondearlo. Puede diferir ligeramente del importe original para identificar pedidos simultáneos.
5. Verifica firma, fecha, identidad del pedido, token, red y estado confirmado; realiza la entrega una sola vez.

La API acepta importes desde 1 con hasta seis decimales. Los ejemplos de Node.js, Python, PHP, Go, Java y C# conservan USDT como valor inicial; adapta el token y la red autorizados. Hay OpenAPI y Postman.

## WooCommerce y planes

El plugin separado v0.6.1 permite elegir moneda y red y verifica el estado antes de marcar el pedido pagado. Requiere WordPress 7.0+, PHP 7.4+, WooCommerce 11.1+, HTTPS y moneda de tienda USD; no ofrece cotización de cambio en vivo. Fue enviado a WordPress.org el 12 de octubre de 2026: escaneo automático aprobado, revisión manual pendiente. Instálalo desde el ZIP de GitHub Releases. La tienda de demostración utiliza dinero real.

Hay una cuota gratuita diaria; los planes de suscripción no tienen límite diario de pedidos. Consulta las condiciones y tarifas actuales en el sitio oficial. Las comisiones de red son independientes. BoltUtil no es una bolsa ni convierte automáticamente a moneda fiduciaria. Los pagos incompletos, tardíos o ambiguos requieren revisión.

## Alcance y ayuda

Este repositorio publica documentación y ejemplos MIT, no el código de producción propietario. El plugin utiliza GPLv2 o posterior. Las marcas identifican integraciones, no avales. La guía inglesa y la referencia API son la base técnica. No publiques secretos en Issues; para seguridad utiliza SECURITY.md.

[Guía USDC](https://boltutil.com/es/docs/usdc-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [Guía Base](https://boltutil.com/es/docs/base-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [Plugin WooCommerce](https://github.com/changye0413/boltutil-payments-for-woocommerce) · [Demo en vivo](https://shop-test.boltutil.com/)

[Soporte y ejemplos](examples/README.md) · [OpenAPI](openapi.yaml) · [Postman](postman/BoltUtil.postman_collection.json) · [Discussions](https://github.com/changye0413/BoltUtil/discussions) · [support@boltutil.com](mailto:support@boltutil.com) · [X: @heyharryzhang](https://x.com/heyharryzhang) · [English](README.md)
