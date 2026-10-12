# BoltUtil v2.1

[English](README.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [Tiếng Việt](README.vi.md) · [Türkçe](README.tr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md)

## Paiements USDT et USDC, directement dans votre portefeuille.

[Commencer gratuitement](https://boltutil.com/fr/auth/register?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=start) · [Documentation API](https://boltutil.com/fr/developer-docs?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=docs) · [Tarifs](https://boltutil.com/fr/pricing?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=pricing)

BoltUtil v2.1 est une API de paiement en stablecoins et une page de paiement hébergée, sans garde des fonds, pour les sites web, SaaS et boutiques WooCommerce. Votre serveur crée la commande ; le client paie à l’adresse du commerçant. BoltUtil vérifie le transfert et les confirmations avant d’envoyer un Webhook signé. Aucune clé privée ni phrase de récupération n’est demandée.

## Réseaux et actifs

Une intégration couvre six réseaux et onze combinaisons actif/réseau. TRON accepte USDT. Ethereum, Polygon PoS et Solana acceptent USDT et USDC natif. BNB Smart Chain accepte USDT et Binance-Peg USDC. Base accepte Bridged USDT et USDC natif. Seules les routes activées par le service et disposant d’une adresse de réception active sont proposées. Les versions natives, bridgées et indexées ne sont pas interchangeables : utilisez le contrat ou mint indiqué dans la commande. La confirmation sur Base dépend de la politique de finalité L1 configurée ; aucun délai fixe n’est promis.

## Portefeuille connecté ou virement manuel

L’adresse, le réseau et le montant exact sont renseignés automatiquement. Le client connecte son portefeuille, vérifie puis confirme. Le transfert manuel, le QR et la copie d’adresse restent disponibles. Les options MetaMask, OKX Wallet, Trust Wallet, Phantom, TronLink, Bitget Wallet, Binance Wallet, TokenPocket, SafePal et Base app varient selon le réseau et l’appareil. Certaines ouvrent la commande dans le navigateur de l’application ; toutes ne proposent pas l’appairage téléphone/ordinateur par QR. Se connecter n’envoie pas de fonds. Le premier usage peut nécessiter un déverrouillage, une autorisation ou un changement de réseau. Les frais requièrent la monnaie native.

## Démarrer l’intégration

1. Créez un compte, activez les adresses de réception et générez une API Key LIVE.
2. Configurez un Webhook HTTPS dans le même compte ; gardez le secret sur le serveur.
3. Créez la commande et ouvrez le `checkoutUrl` retourné.
4. Affichez `payment.amount` sans arrondi. Il peut légèrement différer pour distinguer des commandes simultanées.
5. Vérifiez signature, timestamp, commande, actif, réseau et statut confirmé. Rendez l’exécution idempotente.

L’API accepte un montant minimum de 1 et jusqu’à six décimales. Les exemples Node.js, Python, PHP, Go, Java et C# utilisent USDT par défaut ; adaptez la paire autorisée pour USDC. OpenAPI et Postman sont disponibles.

## WooCommerce et offres

Le plugin distinct v0.6.1 permet de choisir monnaie et réseau, puis vérifie le paiement avant de modifier la commande. Revenir à la boutique ne prouve pas le paiement. Il nécessite WordPress 7.0+, PHP 7.4+, WooCommerce 11.1+, HTTPS et une boutique en USD ; aucune cotation ni fixation de taux de change en direct. Soumis à WordPress.org le 12 octobre 2026 : analyse automatique réussie, examen manuel en attente. Utilisez le ZIP de GitHub Releases avant sa publication dans l’annuaire. Les achats dans la boutique de démonstration utilisent des fonds réels.

Un quota gratuit quotidien est disponible, avec des abonnements sans plafond quotidien de commandes. Consultez les quotas, avantages et tarifs actuels sur le site officiel. Les frais de réseau sont distincts. Les paiements insuffisants, tardifs ou ambigus doivent être examinés. BoltUtil n’est pas une plateforme d’échange et ne convertit pas automatiquement en monnaie fiduciaire.

Ce dépôt contient des documents et exemples MIT, pas le code propriétaire de production. Le plugin utilise GPLv2 ou ultérieur. Les marques ne signifient pas une approbation officielle. Le guide anglais et la référence API sont la base technique. Ne publiez pas de secrets ; suivez SECURITY.md pour signaler une vulnérabilité.

[Guide USDC](https://boltutil.com/fr/docs/usdc-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [Guide Base](https://boltutil.com/fr/docs/base-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [Plugin WooCommerce](https://github.com/changye0413/boltutil-payments-for-woocommerce) · [Boutique démo](https://shop-test.boltutil.com/)

[Aide et exemples](examples/README.md) · [OpenAPI](openapi.yaml) · [Postman](postman/BoltUtil.postman_collection.json) · [Discussions](https://github.com/changye0413/BoltUtil/discussions) · [support@boltutil.com](mailto:support@boltutil.com) · [X: @heyharryzhang](https://x.com/heyharryzhang) · [English](README.md)
