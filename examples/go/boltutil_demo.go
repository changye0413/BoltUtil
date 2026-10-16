// BoltUtil 商户接入示例 / Merchant demo (Go 1.22+).
// 使用 POST /api/v1/order/create，不调用 WordPress /payments。
// 流程：服务端建单 → 保存付款信息 → checkoutUrl → 验签回调 → 数据库事务入账。
// 本程序不连接数据库、不发货；生产改造点见 handleVerifiedEvent。密钥只存服务端环境变量。
package main

import (
	"bytes"
	"crypto/hmac"
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"regexp"
	"strconv"
	"strings"
	"time"
)

const maxBody = 64 * 1024 // Demo 接收上限，不是平台全局限额。
func env(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
func secret() string { return os.Getenv("BOLT_WEBHOOK_SECRET") }
func requireSecret() error {
	if secret() == "" || strings.HasPrefix(secret(), "YOUR_") || strings.HasPrefix(secret(), "whsec_xxx") {
		return errors.New("set BOLT_WEBHOOK_SECRET")
	}
	return nil
}

// 签名毫秒时间戳 + 点 + 原始 UTF-8 body；签名后发送同一份字节，不再序列化。
func signBody(body []byte, timestamp string) string {
	mac := hmac.New(sha256.New, []byte(secret()))
	mac.Write([]byte(timestamp + "."))
	mac.Write(body)
	return hex.EncodeToString(mac.Sum(nil))
}
func verifyWebhook(body []byte, timestamp, signature string) bool {
	if !regexp.MustCompile(`^[0-9]{13}$`).MatchString(timestamp) || !regexp.MustCompile(`^[a-fA-F0-9]{64}$`).MatchString(signature) {
		return false
	}
	ts, err := strconv.ParseInt(timestamp, 10, 64)
	if err != nil {
		return false
	}
	now := time.Now().UnixMilli()
	if ts < now-300000 || ts > now+300000 {
		return false
	}
	received, _ := hex.DecodeString(signature)
	expected, _ := hex.DecodeString(signBody(body, timestamp))
	return hmac.Equal(expected, received)
}
func createOrder(network, currency, amount string) error {
	if err := requireSecret(); err != nil {
		return err
	}
	key := os.Getenv("BOLT_API_KEY")
	if key == "" || strings.HasPrefix(key, "YOUR_") || strings.HasPrefix(key, "bt_live_xxx") {
		return errors.New("set BOLT_API_KEY")
	}
	network = strings.ToUpper(network)
	currency = strings.ToUpper(currency)
	valid := map[string]bool{"TRC20": true, "ERC20": true, "BEP20": true, "POLYGON": true, "SOLANA": true, "BASE": true}
	if !valid[network] || (currency != "USDT" && currency != "USDC") || (network == "TRC20" && currency == "USDC") {
		return errors.New("unsupported network/currency pair")
	}
	// 金额使用十进制文本和 json.Number，避免 float64；最少 1，最多 18 位整数、6 位小数。
	if !regexp.MustCompile(`^[1-9][0-9]{0,17}(\.[0-9]{1,6})?$`).MatchString(amount) {
		return errors.New("amount must be >= 1, max 6 decimals")
	}
	random := make([]byte, 16)
	if _, err := rand.Read(random); err != nil {
		return err
	}
	externalID := env("BOLT_EXTERNAL_ORDER_ID", "INV-"+hex.EncodeToString(random))
	if !regexp.MustCompile(`^[A-Za-z0-9_-]{6,64}$`).MatchString(externalID) {
		return errors.New("invalid externalOrderId")
	}
	notify := os.Getenv("BOLT_NOTIFY_URL")
	if !strings.HasPrefix(notify, "https://") {
		return errors.New("set a public HTTPS BOLT_NOTIFY_URL")
	}
	returnURL, err := url.Parse(env("BOLT_RETURN_URL", "https://merchant.example.com/orders/return"))
	if err != nil {
		return err
	}
	query := returnURL.Query()
	query.Set("order", externalID)
	returnURL.RawQuery = query.Encode() // 保留 query/fragment。
	payload := map[string]any{"amount": json.Number(amount), "externalOrderId": externalID, "network": network, "currency": currency,
		"notifyUrl": notify, "returnUrl": returnURL.String(), "expiredMinutes": 30, "orderDesc": "BoltUtil demo order", "metadata": map[string]string{"source": "go-demo"}}
	body, err := json.Marshal(payload)
	if err != nil {
		return err
	}
	timestamp := strconv.FormatInt(time.Now().UnixMilli(), 10)
	req, err := http.NewRequest(http.MethodPost, strings.TrimRight(env("BOLT_API_BASE", "https://api.boltutil.com"), "/")+"/api/v1/order/create", bytes.NewReader(body))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-Bolt-Key", key)
	req.Header.Set("X-Bolt-Timestamp", timestamp)
	req.Header.Set("X-Bolt-Signature", signBody(body, timestamp))
	// 禁止转发认证头到重定向目标；超时后查询同一个订单号，不盲目创建新单。
	client := &http.Client{Timeout: 20 * time.Second, CheckRedirect: func(_ *http.Request, _ []*http.Request) error { return http.ErrUseLastResponse }}
	fmt.Println("externalOrderId:", externalID)
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	responseBody, err := io.ReadAll(io.LimitReader(resp.Body, 1024*1024))
	if err != nil {
		return err
	}
	var result struct {
		Code int `json:"code"`
	}
	if err = json.Unmarshal(responseBody, &result); err != nil {
		return err
	}
	if resp.StatusCode < 200 || resp.StatusCode >= 300 || result.Code != 200 {
		return fmt.Errorf("create failed: HTTP %d: %s", resp.StatusCode, responseBody)
	}
	// 保存 data.payment.amount/network/currency/address。展示返回精确金额，不能重用请求的原金额。
	fmt.Println(string(responseBody))
	return nil
}
func handleVerifiedEvent(event map[string]any) int {
	if _, ok := event["externalOrderId"].(string); !ok {
		return 400
	}
	if _, ok := event["status"].(string); !ok {
		return 400
	}
	// TODO：当前商户 + externalOrderId 查本地订单；核对网络、币种、地址、返回付款金额。
	// amount/paidAmount 用十进制比较，不使用 float64；少付人工接受要有单独业务授权。
	// 仅 CONFIRMED/COMPLETED 可处理付款，分别代表链上确认/回调送达，不是两笔付款。
	// eventId 在重试时稳定（旧事件可能没有），用数据库唯一约束 + 事务/持久队列保证每单只履约一次。
	// returnUrl 和 metadata 不能作为付款凭证。持久化后返回 2xx，失败返回 5xx，邮件交给异步任务。
	// 本例默认 503 防止未入账就 ACK；BOLT_DEMO_ACK=1 仅用于联调，不可直接用于生产履约。
	fmt.Println("Verified webhook received (no fulfillment performed)")
	if os.Getenv("BOLT_DEMO_ACK") == "1" {
		return 204
	}
	return 503
}
func webhookHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" || r.URL.RequestURI() != "/webhooks/boltutil" {
		w.WriteHeader(404)
		return
	}
	r.Body = http.MaxBytesReader(w, r.Body, maxBody)
	body, err := io.ReadAll(r.Body)
	if err != nil {
		var tooLarge *http.MaxBytesError
		if errors.As(err, &tooLarge) {
			w.WriteHeader(413)
		} else {
			w.WriteHeader(400)
		}
		return
	}
	if !verifyWebhook(body, r.Header.Get("X-Bolt-Webhook-Timestamp"), r.Header.Get("X-Bolt-Webhook-Signature")) {
		w.WriteHeader(401)
		return
	}
	var event map[string]any
	// UseNumber 保留金额精度；拒绝多份 JSON，验签前不解析、不更新任何业务数据。
	decoder := json.NewDecoder(bytes.NewReader(body))
	decoder.UseNumber()
	if err = decoder.Decode(&event); err != nil || event == nil {
		w.WriteHeader(400)
		return
	}
	var extra any
	if decoder.Decode(&extra) != io.EOF {
		w.WriteHeader(400)
		return
	}
	w.WriteHeader(handleVerifiedEvent(event))
}
func main() {
	args := os.Args[1:]
	var err error
	if len(args) > 0 && args[0] == "create" {
		values := []string{"TRC20", "USDT", "1.00"}
		for i := 1; i < len(args) && i <= 3; i++ {
			values[i-1] = args[i]
		}
		err = createOrder(values[0], values[1], values[2])
	} else if len(args) > 0 && args[0] == "webhook" {
		err = requireSecret()
		if err == nil {
			server := &http.Server{Addr: env("BOLT_LISTEN_HOST", "127.0.0.1") + ":" + env("PORT", "3000"), Handler: http.HandlerFunc(webhookHandler), ReadHeaderTimeout: 10 * time.Second, ReadTimeout: 15 * time.Second, WriteTimeout: 15 * time.Second}
			fmt.Println("Webhook listener ready; use HTTPS reverse proxy")
			err = server.ListenAndServe()
		}
	} else {
		fmt.Println("go run boltutil_demo.go create POLYGON USDC 1.09 | webhook")
	}
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
