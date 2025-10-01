package main

import (
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"math/big"
	"net/http"
	"net/url"
	"sort"
	"strconv"
	"strings"
	"time"

	"github.com/ethereum/go-ethereum/accounts/abi"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/crypto"
)

//go version go1.24.1 darwin/arm64
var (
	//your main wallet address (eoa)
	//你的登陆钱包地址(erc20)
	user = "*****"
	//please get these parameters from  https://www.asterdex.com/en/api-wallet
	//下面这些参数在这里生成配置  https://www.asterdex.com/zh-CN/api-wallet
	signer    = "*******"
	priKeyHex = "********"

	//请求的域名
	host = "https://fapi.asterdex.com"
	cli  = &http.Client{
		Timeout: 15 * time.Second,
	}
)

var placeOrder = map[string]interface{}{
	"url":    "/fapi/v3/order",
	"method": "POST",
	"params": map[string]interface{}{
		"symbol":       "BTCUSDT",
		"positionSide": "BOTH",
		"type":         "LIMIT",
		"side":         "BUY",
		"timeInForce":  "GTC",
		"quantity":     "0.01",
		"price":        "110000.2",
	},
}

var getOrder = map[string]interface{}{
	"url":    "/fapi/v3/order",
	"method": "GET",
	"params": map[string]interface{}{
		"symbol":  "SANDUSDT",
		"orderId": "2194215",
		"side":    "BUY",
		"type":    "LIMIT",
	},
}

func main() {
	//get an order
	if err := call(getOrder); err != nil {
		fmt.Println("call failed:", err)
	}
	//place an order
	if err := call(placeOrder); err != nil {
		fmt.Println("call failed:", err)
	}
}

func call(api map[string]interface{}) error {
	nonce := genNonce()
	fmt.Println("nonce:", nonce)
	// 复制一份 params，以免修改全局模板
	params := cloneInterface(api["params"])
	paramsMap, ok := params.(map[string]interface{})
	if !ok {
		return errors.New("params must be map[string]interface{}")
	}

	// sign 会修改 paramsMap（加入 user, signer, signature, timestamp, recvWindow）
	if err := sign(paramsMap, nonce); err != nil {
		return err
	}

	// 发送请求
	urlPath, _ := api["url"].(string)
	method, _ := api["method"].(string)
	fullUrl := strings.TrimRight(host, "/") + urlPath
	respBody, statusCode, err := send(fullUrl, method, paramsMap)
	if err != nil {
		return err
	}
	fmt.Printf("HTTP %d response: %s\n", statusCode, respBody)
	return nil
}

// sign 将在 params 中添加 timestamp, recvWindow, user, signer, signature
func sign(params map[string]interface{}, nonce uint64) error {
	// 添加 recvWindow 和 timestamp (毫秒)
	params["recvWindow"] = "50000"
	timestamp := strconv.FormatInt(time.Now().UnixNano()/int64(time.Millisecond), 10)
	//params["timestamp"] = "1759212310710"
	params["timestamp"] = timestamp

	// 先做确定性的序列化（递归按 key 排序）
	trimmed, err := normalizeAndStringify(params)
	if err != nil {
		return err
	}
	// trimmed 是 string，作为第一个 ABI 参数
	// 构造 ABI: (string, address, address, uint256)
	argString := trimmed
	fmt.Println(argString)
	addrUser := common.HexToAddress(user)
	addrSigner := common.HexToAddress(signer)
	nonceBig := new(big.Int).SetUint64(nonce)

	// 定义 abi types
	tString, err := abi.NewType("string", "", nil)
	if err != nil {
		return err
	}
	tAddress, err := abi.NewType("address", "", nil)
	if err != nil {
		return err
	}
	tUint256, err := abi.NewType("uint256", "", nil)
	if err != nil {
		return err
	}
	arguments := abi.Arguments{
		{Type: tString},
		{Type: tAddress},
		{Type: tAddress},
		{Type: tUint256},
	}

	// Pack
	packed, err := arguments.Pack(argString, addrUser, addrSigner, nonceBig)
	if err != nil {
		return fmt.Errorf("abi pack error: %w", err)
	}

	fmt.Println(hex.EncodeToString(packed))

	// keccak256
	hash := crypto.Keccak256(packed)

	fmt.Println(hex.EncodeToString(hash))

	prefixedMsg := fmt.Sprintf("\x19Ethereum Signed Message:\n%d%s", len(hash), hash)

	// 2. keccak256 哈希
	msgHash := crypto.Keccak256Hash([]byte(prefixedMsg))
	// Load private key
	privKey, err := crypto.HexToECDSA(strings.TrimPrefix(priKeyHex, "0x"))
	if err != nil {
		return fmt.Errorf("invalid private key: %w", err)
	}

	// Sign the hash (returns 65 bytes: R(32)|S(32)|V(1))
	sig, err := crypto.Sign(msgHash.Bytes(), privKey)
	if err != nil {
		return fmt.Errorf("sign error: %w", err)
	}

	// crypto.Sign returns v as 0/1 in last byte — convert to 27/28
	if len(sig) != 65 {
		return fmt.Errorf("unexpected signature length: %d", len(sig))
	}
	sig[64] += 27

	// hex-encode with 0x prefix
	sigHex := "0x" + hex.EncodeToString(sig)

	// 将 user、signer、signature 插入 params
	params["user"] = user
	params["signer"] = signer
	params["signature"] = sigHex

	//把 nonce 也放回 params
	params["nonce"] = nonce

	fmt.Println("signature:", hex.EncodeToString(sig))

	return nil
}

// send HTTP 请求：POST -> body JSON; GET/DELETE -> params放 querystring
func send(fullUrl string, method string, params map[string]interface{}) (string, int, error) {
	method = strings.ToUpper(method)
	switch method {
	case "POST":
		form := url.Values{}
		for k, v := range params {
			form.Set(k, fmt.Sprintf("%v", v)) // interface{} -> string
		}
		req, err := http.NewRequest("POST", fullUrl, strings.NewReader(form.Encode()))
		req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
		resp, err := cli.Do(req)
		if err != nil {
			return "", 0, err
		}
		defer resp.Body.Close()
		body, _ := io.ReadAll(resp.Body)
		return string(body), resp.StatusCode, nil
	case "GET", "DELETE":
		// 把 params 放到 querystring（递归转成 key=val 的方式；此处做最简单的 flat 化）
		q := url.Values{}
		flattenParams("", params, &q)
		u, _ := url.Parse(fullUrl)
		u.RawQuery = q.Encode()
		fmt.Println(u.String())
		req, _ := http.NewRequest(method, u.String(), nil)
		resp, err := cli.Do(req)
		if err != nil {
			return "", 0, err
		}
		defer resp.Body.Close()
		body, _ := io.ReadAll(resp.Body)
		return string(body), resp.StatusCode, nil
	default:
		return "", 0, fmt.Errorf("unsupported http method: %s", method)
	}
}

// flattenParams 将 map 递归展平成 query params
func flattenParams(prefix string, v interface{}, q *url.Values) {
	switch val := v.(type) {
	case map[string]interface{}:
		// 保持 key 排序，确定性
		keys := make([]string, 0, len(val))
		for k := range val {
			keys = append(keys, k)
		}
		sort.Strings(keys)
		for _, k := range keys {
			nk := k
			if prefix != "" {
				nk = prefix + "." + k
			}
			flattenParams(nk, val[k], q)
		}
	case []interface{}:
		for i, item := range val {
			nk := fmt.Sprintf("%s[%d]", prefix, i)
			flattenParams(nk, item, q)
		}
	case string:
		q.Add(prefix, val)
	case bool:
		q.Add(prefix, fmt.Sprintf("%v", val))
	case float64:
		// JSON decode 默认数值为 float64
		q.Add(prefix, fmt.Sprintf("%v", val))
	case nil:
		// skip nil
	default:
		// 尝试格式化为 string
		q.Add(prefix, fmt.Sprintf("%v", val))
	}
}

// normalizeAndStringify 对 map 做确定性序列化（按 key 排序），返回 string
func normalizeAndStringify(v interface{}) (string, error) {
	// 先把 v 变成一个 deterministic structure，然后 json.Marshal
	norm, err := normalize(v)
	if err != nil {
		return "", err
	}
	bs, err := json.Marshal(norm)
	if err != nil {
		return "", err
	}
	return string(bs), nil
}

// normalize 将 map/array 中的键按字母序排序并递归处理
func normalize(v interface{}) (interface{}, error) {
	switch val := v.(type) {
	case map[string]interface{}:
		keys := make([]string, 0, len(val))
		for k := range val {
			keys = append(keys, k)
		}
		sort.Strings(keys)
		//out := make([]interface{}, 0, len(keys))
		// 为了保证 JSON 有键名，我们重建为 map 并按顺序添加
		newMap := make(map[string]interface{}, len(keys))
		for _, k := range keys {
			nv, err := normalize(val[k])
			if err != nil {
				return nil, err
			}
			newMap[k] = nv
		}
		// 返回按 key 排序的 map（Marshal 时 map 的顺序并不保证，但我们已按 key 插入；若你需要绝对保证，请把结果改为 []kv 的形式）
		return newMap, nil
	case map[interface{}]interface{}:
		// unlikely in JSON-decoded, 但处理一下
		keys := make([]string, 0, len(val))
		for k := range val {
			keys = append(keys, fmt.Sprint(k))
		}
		sort.Strings(keys)
		newMap := make(map[string]interface{}, len(keys))
		for _, k := range keys {
			newMap[k] = val[k]
		}
		return normalize(newMap)
	case []interface{}:
		out := make([]interface{}, 0, len(val))
		for _, it := range val {
			nv, err := normalize(it)
			if err != nil {
				return nil, err
			}
			out = append(out, nv)
		}
		return out, nil
	default:
		// 基本类型直接返回
		return val, nil
	}
}

// cloneInterface 做浅拷贝（仅用于顶层 params）
func cloneInterface(v interface{}) interface{} {
	// 通过 json marshal/unmarshal 做深拷贝（简单可靠）
	bs, err := json.Marshal(v)
	if err != nil {
		return v
	}
	var out interface{}
	_ = json.Unmarshal(bs, &out)
	return out
}

func genNonce() uint64 {
	micro := time.Now().UnixMicro()
	return uint64(micro)
}
