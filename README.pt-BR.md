# BoltUtil v2.1

[English](README.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [Tiếng Việt](README.vi.md) · [Türkçe](README.tr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md)

## Pagamentos em USDT e USDC, direto para sua carteira.

[Começar grátis](https://boltutil.com/pt/auth/register?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=start) · [Documentação API](https://boltutil.com/pt/developer-docs?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=docs) · [Preços](https://boltutil.com/pt/pricing?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=pricing)

BoltUtil v2.1 é uma API de pagamentos em stablecoins com checkout hospedado e sem custódia para sites, SaaS e lojas WooCommerce. Seu servidor cria o pedido, e o cliente paga à carteira do comerciante. O serviço verifica a transferência e as confirmações antes de enviar um Webhook assinado. Não solicita chaves privadas ou frases de recuperação.

## Redes e novidades

Uma integração cobre seis redes e onze combinações de ativo/rede. TRON aceita USDT. Ethereum, Polygon PoS e Solana aceitam USDT e USDC nativo. BNB Smart Chain aceita USDT e Binance-Peg USDC. Base aceita Bridged USDT e USDC nativo. As rotas precisam estar ativadas pelo serviço e ter uma carteira receptora ativa. Tokens nativos, bridged e vinculados não são intercambiáveis; use o contrato ou mint do pedido. A confirmação em Base depende da política de finalidade L1 configurada, sem prazo fixo garantido.

## Carteira conectada ou transferência manual

O checkout preenche endereço, rede e valor exato. O cliente conecta a carteira, confere e confirma. Transferência manual, QR e cópia de endereço continuam disponíveis. As opções incluem MetaMask, OKX Wallet, Trust Wallet, Phantom, TronLink, Bitget Wallet, Binance Wallet, TokenPocket, SafePal e Base app, conforme rede e dispositivo. Algumas abrem o pedido no navegador do aplicativo; nem todas oferecem pareamento remoto por QR. Conectar não envia fundos. O primeiro uso pode exigir desbloqueio, autorização ou troca de rede, além de moeda nativa para taxas.

## Comece a integrar

1. Crie a conta, ative endereços de recebimento e gere uma API Key LIVE.
2. Configure um Webhook HTTPS na mesma conta; mantenha o segredo no servidor.
3. Crie o pedido e redirecione para o `checkoutUrl` retornado.
4. Exiba `payment.amount` sem arredondar. O valor pode mudar ligeiramente para distinguir pedidos simultâneos.
5. Valide assinatura, timestamp, pedido, token, rede e estado confirmado. A entrega deve ser idempotente.

A API aceita valores a partir de 1 com até seis casas decimais. Os exemplos em Node.js, Python, PHP, Go, Java e C# mantêm USDT como padrão; adapte a combinação autorizada. OpenAPI e Postman estão disponíveis.

## WooCommerce, planos e suporte

O plugin independente v0.6.1 permite alternar a moeda e escolher a rede. Só atualiza o pedido após verificar o pagamento; retornar à loja não prova pagamento. Requer WordPress 7.0+, PHP 7.4+, WooCommerce 11.1+, HTTPS e moeda USD. Não fornece cotação de câmbio em tempo real. Enviado ao WordPress.org em 12 de outubro de 2026: verificação automática aprovada, revisão manual pendente. Instale o ZIP versionado do GitHub Releases. Compras na loja de demonstração usam fundos reais.

Há uma cota gratuita diária e planos sem limite diário de pedidos. Consulte os limites, benefícios e preços atuais no site oficial; taxas de rede são separadas. Pagamentos insuficientes, tardios ou ambíguos precisam de análise. BoltUtil não é uma exchange nem converte automaticamente para moeda fiduciária.

Este repositório contém documentação e exemplos sob MIT; a plataforma de produção é proprietária. O plugin usa GPLv2 ou posterior. Marcas não representam endosso. A documentação inglesa e a referência API são a base técnica. Não publique credenciais; siga SECURITY.md para vulnerabilidades.

[Guia USDC](https://boltutil.com/pt/docs/usdc-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [Guia Base](https://boltutil.com/pt/docs/base-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [Plugin WooCommerce](https://github.com/changye0413/boltutil-payments-for-woocommerce) · [Demo ao vivo](https://shop-test.boltutil.com/)

[Suporte e exemplos](examples/README.md) · [OpenAPI](openapi.yaml) · [Postman](postman/BoltUtil.postman_collection.json) · [Discussions](https://github.com/changye0413/BoltUtil/discussions) · [support@boltutil.com](mailto:support@boltutil.com) · [X: @heyharryzhang](https://x.com/heyharryzhang) · [English](README.md)
