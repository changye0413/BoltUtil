package main

import (
	"bytes"
	"crypto/hmac"
	"crypto/sha256"
	"crypto/subtle"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"
)

var (
	apiBase       = env("BOLT_API_BASE", "https://api.boltutil.com")
	apiKey        = env("BOLT_API_KEY", "YOUR_API_KEY")
	webhookSecret = env("BOLT_WEBHOOK_SECRET", "YOUR_WEBHOOK_SECRET")
	notifyURL     = env("BOLT_NOTIFY_URL", "https://merchant.example.com/webhooks/boltutil")
	returnURL     = env("BOLT_RETURN_URL", "https://merchant.example.com/orders/return")
)

func env(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}

func hmacSHA256Hex(payload, secret string) string {
	mac := hmac.New(sha256.New, []byte(secret))
	mac.Write([]byte(payload))
	return hex.EncodeToString(mac.Sum(nil))
}

func signBody(rawBody, timestamp string) string {
	return hmacSHA256Hex(timestamp+"."+rawBody, webhookSecret)
}

func createOrder(network string) error {
	externalOrderID := fmt.Sprintf("INV-%d", time.Now().UnixMilli())
	payload := map[string]any{
		"amount":          25.0,
		"externalOrderId": externalOrderID,
		"network":         network,
		"currency":        "USDT",
		"orderDesc":       "BoltUtil demo order",
		"notifyUrl":       notifyURL,
		"returnUrl":       returnURL + "?order=" + externalOrderID,
		"expiredMinutes":  30,
		"metadata": map[string]any{
			"customerId": "CUS_1001",
			"source":     "go-demo",
		},
	}

	bodyBytes, err := json.Marshal(payload)
	if err != nil {
		return err
	}
	rawBody := string(bodyBytes)
	timestamp := strconv.FormatInt(time.Now().UnixMilli(), 10)
	signature := signBody(rawBody, timestamp)

	req, err := http.NewRequest("POST", apiBase+"/api/v1/order/create", bytes.NewBufferString(rawBody))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-Bolt-Key", apiKey)
	req.Header.Set("X-Bolt-Timestamp", timestamp)
	req.Header.Set("X-Bolt-Signature", signature)

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	responseBody, _ := io.ReadAll(resp.Body)
	fmt.Println("HTTP", resp.StatusCode)
	fmt.Println(string(responseBody))
	return nil
}

func verifyWebhook(rawBody, timestamp, signature string) bool {
	if timestamp == "" || signature == "" {
		return false
	}

	ts, err := strconv.ParseInt(timestamp, 10, 64)
	if err != nil {
		return false
	}
	if abs(time.Now().UnixMilli()-ts) > 5*60*1000 {
		return false
	}

	expected := signBody(rawBody, timestamp)
	left := []byte(strings.ToLower(expected))
	right := []byte(strings.ToLower(signature))
	return len(left) == len(right) && subtle.ConstantTimeCompare(left, right) == 1
}

func abs(value int64) int64 {
	if value < 0 {
		return -value
	}
	return value
}

func webhookHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.NotFound(w, r)
		return
	}

	bodyBytes, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, `{"error":"read_body_failed"}`, http.StatusBadRequest)
		return
	}
	rawBody := string(bodyBytes)
	timestamp := r.Header.Get("X-Bolt-Webhook-Timestamp")
	signature := r.Header.Get("X-Bolt-Webhook-Signature")

	w.Header().Set("Content-Type", "application/json")
	if !verifyWebhook(rawBody, timestamp, signature) {
		w.WriteHeader(http.StatusUnauthorized)
		w.Write([]byte(`{"error":"invalid_signature"}`))
		return
	}

	var event map[string]any
	if err := json.Unmarshal(bodyBytes, &event); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte(`{"error":"invalid_json"}`))
		return
	}

	fmt.Println("Verified BoltUtil webhook:", event)
	// TODO: update your local order by event["externalOrderId"].
	// Only fulfill when status is CONFIRMED or COMPLETED, according to your business rules.

	w.Write([]byte(`{"status":"SUCCESS"}`))
}

func startWebhookServer() error {
	port := env("PORT", "3000")
	http.HandleFunc("/webhooks/boltutil", webhookHandler)
	fmt.Println("BoltUtil webhook demo listening on http://localhost:" + port + "/webhooks/boltutil")
	return http.ListenAndServe(":"+port, nil)
}

func main() {
	command := ""
	if len(os.Args) > 1 {
		command = os.Args[1]
	}

	switch command {
	case "create":
		network := "TRC20"
		if len(os.Args) > 2 {
			network = os.Args[2]
		}
		if err := createOrder(network); err != nil {
			panic(err)
		}
	case "webhook":
		if err := startWebhookServer(); err != nil {
			panic(err)
		}
	default:
		fmt.Println("Usage:")
		fmt.Println("  go run boltutil_demo.go create TRC20")
		fmt.Println("  go run boltutil_demo.go create ERC20")
		fmt.Println("  go run boltutil_demo.go create BEP20")
		fmt.Println("  go run boltutil_demo.go create POLYGON")
		fmt.Println("  go run boltutil_demo.go create SOLANA")
		fmt.Println("  go run boltutil_demo.go webhook")
	}
}
