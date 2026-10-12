# BoltUtil v2.1

[English](README.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [Tiếng Việt](README.vi.md) · [Türkçe](README.tr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md)

## مدفوعات USDT وUSDC تصل مباشرة إلى محفظتك.

[ابدأ مجانًا](https://boltutil.com/ar/auth/register?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=start) · [وثائق API](https://boltutil.com/ar/developer-docs?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=docs) · [الأسعار](https://boltutil.com/ar/pricing?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=pricing)

BoltUtil v2.1 هو واجهة API لمدفوعات العملات المستقرة وصفحة دفع مستضافة دون حفظ الأموال لدى المنصة، للمواقع وخدمات SaaS ومتاجر WooCommerce. ينشئ خادم التاجر الطلب، ويدفع العميل إلى عنوان التاجر. يتحقق BoltUtil من التحويل وتأكيدات الشبكة ثم يرسل Webhook موقّعًا. لا يطلب المفاتيح الخاصة أو عبارات الاسترداد.

## الشبكات والأصول

تكامل واحد لست شبكات وإحدى عشرة تركيبة أصل/شبكة. تدعم TRON عملة USDT. تدعم Ethereum وPolygon PoS وSolana عملتي USDT وUSDC الأصلي. تدعم BNB Smart Chain عملتي USDT وBinance-Peg USDC. تدعم Base عملتي Bridged USDT وUSDC الأصلي. تظهر المسارات التي فعّلها النظام ولها عنوان استقبال نشط للتاجر فقط. النسخ الأصلية والمجسّرة والمربوطة ليست قابلة للاستبدال؛ استخدم العقد أو mint المحدد في الطلب. تأكيد Base يتبع سياسة نهائية L1 المهيأة، ولا يُضمن وقت ثابت.

## الدفع بالمحفظة أو التحويل اليدوي

تُملأ الشبكة والعنوان والمبلغ الدقيق تلقائيًا، ويقوم العميل بالمراجعة والتأكيد داخل محفظته. يبقى التحويل اليدوي ورمز QR ونسخ العنوان متاحًا. تشمل الخيارات MetaMask وOKX Wallet وTrust Wallet وPhantom وTronLink وBitget Wallet وBinance Wallet وTokenPocket وSafePal وBase app بحسب الشبكة والجهاز. تفتح بعض الخيارات الطلب في متصفح التطبيق؛ لا تدعم جميع المحافظ اقتران الهاتف بسطح المكتب عبر QR. الاتصال لا يرسل أموالًا. قد يتطلب الاستخدام الأول فتح المحفظة أو السماح بالاتصال أو تغيير الشبكة، وتحتاج الرسوم إلى العملة الأصلية للشبكة.

## بدء التكامل

1. أنشئ حسابًا وفعّل عناوين الاستقبال وأنشئ API Key من نوع LIVE.
2. اضبط Webhook عبر HTTPS في حساب التاجر نفسه، واحتفظ بالسر على الخادم.
3. أنشئ الطلب وافتح `checkoutUrl` الذي يعيده النظام.
4. اعرض `payment.amount` كاملًا دون تقريب؛ قد يختلف قليلًا لتمييز الطلبات المتزامنة.
5. تحقّق من التوقيع والطابع الزمني والطلب والأصل والشبكة والحالة المؤكدة، ونفّذ الطلب مرة واحدة فقط.

الحد الأدنى لمبلغ API هو 1، وبحد أقصى ست منازل عشرية. أمثلة Node.js وPython وPHP وGo وJava وC# تستخدم USDT افتراضيًا؛ عدّل التركيبة المسموح بها عند استخدام USDC. تتوفر OpenAPI وPostman.

## WooCommerce والخطط

الإضافة المنفصلة v0.6.1 تتيح اختيار العملة والشبكة، وتتحقق من الدفع قبل تحديث الطلب. العودة إلى المتجر ليست إثباتًا للدفع. تتطلب WordPress 7.0+ وPHP 7.4+ وWooCommerce 11.1+ وHTTPS وعملة متجر USD؛ لا توفر سعر صرف مباشرًا أو تثبيتًا له. قُدّمت إلى WordPress.org في 12 أكتوبر 2026، واجتازت الفحص التلقائي وتنتظر المراجعة اليدوية. استخدم ZIP من GitHub Releases قبل نشرها في الدليل. مشتريات المتجر التجريبي تستخدم أموالًا حقيقية.

توجد حصة مجانية يومية واشتراكات دون حد يومي للطلبات. راجع الحصص والمزايا والأسعار الحالية في الموقع الرسمي؛ رسوم الشبكة منفصلة. الدفعات الناقصة أو المتأخرة أو غير محددة الطلب تحتاج إلى مراجعة. BoltUtil ليس منصة تداول ولا يحوّل الأموال تلقائيًا إلى العملات التقليدية.

المستودع يحتوي وثائق وأمثلة بترخيص MIT، وليس شيفرة المنصة الإنتاجية المغلقة. الإضافة بترخيص GPLv2 أو أحدث. أسماء العلامات لا تعني تأييدًا رسميًا. الدليل الإنجليزي ومرجع API هما الأساس التقني. لا تنشر أسرارًا، واتبع SECURITY.md للإبلاغ عن الثغرات.

[دليل USDC](https://boltutil.com/ar/docs/usdc-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [دليل Base](https://boltutil.com/ar/docs/base-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [إضافة WooCommerce](https://github.com/changye0413/boltutil-payments-for-woocommerce) · [المتجر التجريبي](https://shop-test.boltutil.com/)

[الدعم والأمثلة](examples/README.md) · [OpenAPI](openapi.yaml) · [Postman](postman/BoltUtil.postman_collection.json) · [Discussions](https://github.com/changye0413/BoltUtil/discussions) · [support@boltutil.com](mailto:support@boltutil.com) · [X: @heyharryzhang](https://x.com/heyharryzhang) · [English](README.md)
