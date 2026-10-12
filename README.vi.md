# BoltUtil v2.1

[English](README.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [Tiếng Việt](README.vi.md) · [Türkçe](README.tr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md)

## Nhận USDT và USDC trực tiếp vào ví của bạn.

[Bắt đầu miễn phí](https://boltutil.com/vi/auth/register?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=start) · [Tài liệu API](https://boltutil.com/vi/developer-docs?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=docs) · [Bảng giá](https://boltutil.com/vi/pricing?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=pricing)

BoltUtil v2.1 là API thanh toán stablecoin và trang thanh toán lưu trữ sẵn, không lưu ký, dành cho website, SaaS và cửa hàng WooCommerce. Máy chủ người bán tạo đơn; khách chuyển tiền đến ví người bán. BoltUtil kiểm tra giao dịch và xác nhận trên chuỗi rồi gửi Webhook có chữ ký. Dịch vụ không yêu cầu khóa riêng hay cụm từ khôi phục.

## Mạng và loại tài sản

Một quy trình tích hợp cho sáu mạng và mười một cặp tài sản/mạng. TRON hỗ trợ USDT. Ethereum, Polygon PoS và Solana hỗ trợ USDT cùng USDC gốc. BNB Smart Chain hỗ trợ USDT và Binance-Peg USDC. Base hỗ trợ Bridged USDT và USDC gốc. Chỉ hiển thị tuyến đã được dịch vụ bật và có địa chỉ nhận đang hoạt động. Token gốc, token qua cầu nối và token neo giá không thay thế cho nhau: dùng đúng hợp đồng hoặc mint của đơn. Xác nhận Base tuân theo chính sách tính cuối cùng L1 đã cấu hình; không cam kết thời gian cố định.

## Thanh toán qua ví hoặc chuyển thủ công

Địa chỉ, mạng và số tiền chính xác được điền tự động; khách kiểm tra rồi xác nhận trong ví. Vẫn có chuyển thủ công, mã QR và sao chép địa chỉ. Các lựa chọn gồm MetaMask, OKX Wallet, Trust Wallet, Phantom, TronLink, Bitget Wallet, Binance Wallet, TokenPocket, SafePal và Base app, tùy mạng và thiết bị. Một số mở đơn trong trình duyệt của ứng dụng, không phải tất cả đều ghép phiên điện thoại/máy tính bằng QR. Kết nối không tự chuyển tiền. Lần đầu có thể cần mở khóa, cấp quyền hoặc đổi mạng; cần đồng gốc để trả phí.

## Bắt đầu

1. Tạo tài khoản, bật địa chỉ nhận và tạo API Key LIVE.
2. Cấu hình Webhook HTTPS trong cùng tài khoản; giữ bí mật trên máy chủ.
3. Tạo đơn và mở `checkoutUrl` được trả về.
4. Hiển thị đủ `payment.amount`, không làm tròn; giá trị có thể lệch nhẹ để phân biệt các đơn đồng thời.
5. Kiểm tra chữ ký, timestamp, đơn, token, mạng và trạng thái xác nhận. Xử lý hoàn tất theo cơ chế idempotent.

API nhận số tiền từ 1, tối đa sáu chữ số thập phân. Ví dụ Node.js, Python, PHP, Go, Java và C# mặc định dùng USDT; đổi sang cặp được cho phép khi tích hợp USDC. Có OpenAPI và Postman.

## WooCommerce và gói dịch vụ

Plugin riêng v0.6.1 cho phép đổi token và chọn mạng, xác minh thanh toán trước khi cập nhật đơn. Quay lại cửa hàng không chứng minh đã trả tiền. Yêu cầu WordPress 7.0+, PHP 7.4+, WooCommerce 11.1+, HTTPS và tiền tệ USD; không có báo giá hay khóa tỷ giá trực tiếp. Đã gửi WordPress.org ngày 12/10/2026: quét tự động đạt, đang chờ đánh giá thủ công. Cài ZIP phiên bản trên GitHub Releases. Mua ở cửa hàng demo sử dụng tiền thật.

Có hạn mức miễn phí mỗi ngày và gói thuê bao không giới hạn số đơn mỗi ngày. Xem hạn mức, quyền lợi và giá hiện hành trên website; phí mạng riêng biệt. Thanh toán thiếu, muộn hoặc không rõ thuộc đơn nào cần kiểm tra. BoltUtil không phải sàn và không tự đổi sang tiền pháp định.

Tài liệu và ví dụ công khai dùng MIT; nền tảng sản xuất đóng mã nguồn. Plugin dùng GPLv2 trở lên. Tên thương hiệu không thể hiện sự bảo trợ. Tài liệu tiếng Anh và API là cơ sở kỹ thuật. Không đăng bí mật; xem SECURITY.md để báo lỗ hổng.

[Hướng dẫn USDC](https://boltutil.com/vi/docs/usdc-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [Hướng dẫn Base](https://boltutil.com/vi/docs/base-integration?utm_source=github&utm_medium=referral&utm_campaign=boltutil_v21&utm_content=readme) · [Plugin WooCommerce](https://github.com/changye0413/boltutil-payments-for-woocommerce) · [Cửa hàng demo](https://shop-test.boltutil.com/)

[Hỗ trợ và ví dụ](examples/README.md) · [OpenAPI](openapi.yaml) · [Postman](postman/BoltUtil.postman_collection.json) · [Discussions](https://github.com/changye0413/BoltUtil/discussions) · [support@boltutil.com](mailto:support@boltutil.com) · [X: @heyharryzhang](https://x.com/heyharryzhang) · [English](README.md)
