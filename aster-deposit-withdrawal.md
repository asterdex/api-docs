## Table of Contents

- [Query APIs](#query-apis)
  - [get all deposit assets](#get-all-deposit-assets)
  - [get all withdraw assets](#get-all-withdraw-assets)
  - [estimate withdraw fee](#estimate-withdraw-fee)
  - [get server time](#get-server-time)
- [Signature](#signature)
  - [API-KEY Signature (V1)](#api-key-signature-v1)
  - [Pro API-KEY Signature (V3)](#pro-api-key-signature-v3)
  - [EVM Withdraw Signature](#evm-withdraw-signature)
  - [Solana Withdraw Signature (optional)](#solana-withdraw-signature-optional)
- [Withdrawal APIs](#withdrawal-apis)
  - [withdraw by fapi \[evm\] \[futures\]](#withdraw-by-fapi-evm-futures)
  - [withdraw by fapi \[solana\] \[futures\]](#withdraw-by-fapi-solana-futures)
  - [withdraw by API \[evm\] \[spot\]](#withdraw-by-api-evm-spot)
  - [withdraw by API \[solana\] \[spot\]](#withdraw-by-api-solana-spot)
  - [withdraw by fapi\[v3\] \[evm\] \[futures\]](#withdraw-by-fapiv3-evm-futures)
  - [withdraw by fapi\[v3\] \[solana\] \[futures\]](#withdraw-by-fapiv3-solana-futures)
  - [withdraw by fapi\[v3\] \[evm\] \[spot\]](#withdraw-by-fapiv3-evm-spot)
  - [withdraw by fapi\[v3\] \[solana\] \[spot\]](#withdraw-by-fapiv3-solana-spot)

---

# Query APIs

## get all deposit assets

### request:

```shell
curl 'https://www.asterdex.com/bapi/futures/v1/public/future/aster/deposit/assets?chainIds=56&networks=EVM&accountType=spot'
```

### params:

| param       | type   | required | description                                                            |
|-------------|--------|----------|------------------------------------------------------------------------|
| chainIds    | string | true     | Chain ID, multiple IDs separated by commas                             |
| networks    | string | false    | Network type, e.g., EVM, SOLANA, multiple networks separated by commas |
| accountType | string | true     | Account type, e.g., spot, perp                                         |

### response:

```json
{
    "code": "000000",
    "message": null,
    "messageDetail": null,
    "data": [
        {
            "name": "ASTER",
            "displayName": "ASTER",
            "contractAddress": "0x000ae314e2a2172a039b26378814c252734f556a",
            "decimals": 18,
            "network": "EVM",
            "chainId": 56,
            "depositType": "normal",
            "rank": 10,
            "isNative": false,
            "admin": null,
            "bank": null,
            "tokenVaultAuthority": null,
            "tokenVault": null,
            "tokenMint": null,
            "associatedTokenProgram": null,
            "tokenProgram": null,
            "systemProgram": null,
            "ixSysvar": null,
            "priceFeed": null,
            "priceFeedProgram": null,
            "solVault": null
        }
    ],
    "success": true
}
```

## get all withdraw assets

### request:

```shell
curl 'https://www.asterdex.com/bapi/futures/v1/public/future/aster/withdraw/assets?chainIds=56&networks=EVM&accountType=spot'
```

### params:

| param       | type   | required | description                                                            |
|-------------|--------|----------|------------------------------------------------------------------------|
| chainIds    | string | true     | Chain ID, multiple IDs separated by commas                             |
| networks    | string | false    | Network type, e.g., EVM, SOLANA, multiple networks separated by commas |
| accountType | string | true     | Account type, e.g., spot, perp                                         |

### response:

```json
{
    "code": "000000",
    "message": null,
    "messageDetail": null,
    "data": [
        {
            "name": "ASTER",
            "displayName": "ASTER",
            "contractAddress": "0x000ae314e2a2172a039b26378814c252734f556a",
            "decimals": 18,
            "network": "EVM",
            "chainId": 56,
            "withdrawType": "autoWithdraw",
            "rank": 10,
            "isNative": false,
            "isProfit": true,
            "admin": null,
            "bank": null,
            "tokenVaultAuthority": null,
            "tokenVault": null,
            "tokenMint": null,
            "associatedTokenProgram": null,
            "tokenProgram": null,
            "systemProgram": null,
            "ixSysvar": null,
            "priceFeed": null,
            "priceFeedProgram": null,
            "solVault": null
        }
    ],
    "success": true
}
```

## estimate withdraw fee

### request:

```shell
curl 'https://www.asterdex.com/bapi/futures/v1/public/future/aster/estimate-withdraw-fee?chainId=56&network=EVM&currency=ASTER&accountType=spot'
```

### params:

| param       | type   | required | description                    |
|-------------|--------|----------|--------------------------------|
| chainId     | int    | true     | Chain ID                       |
| network     | string | true     | Network type, e.g., EVM, SOL   |
| currency    | string | true     | Currency name, e.g., ASTER     |
| accountType | string | true     | Account type, e.g., spot, perp |

### response:

```json
{
    "code": "000000",
    "message": null,
    "messageDetail": null,
    "data": {
        "gasPrice": null,
        "gasLimit": 200000,
        "nativePrice": null,
        "tokenPrice": 1.12357820,
        "gasCost": 0.0891,
        "gasUsdValue": 0.1
    },
    "success": true
}
```

| field   | desc                                    |
|---------|-----------------------------------------|
| gasCost | Estimated withdrawal fee in token units |

## get server time

### request:

```shell
curl 'https://fapi5.asterdex.com/fapi/v3/time'
```

### response:

```json
{
    "serverTime": 1742198400000
}
```

| field      | desc                                        |
|------------|---------------------------------------------|
| serverTime | Current server time in milliseconds (Unix)  |

---

# Signature

## API-KEY Signature (V1)

With a V1 API key, you generate your own `API_KEY` and `API_SECRET`. Every request must include the following three parameters:

| parameter  | description                                                                                     |
|------------|-------------------------------------------------------------------------------------------------|
| timestamp  | Current time in milliseconds (Unix timestamp)                                                   |
| recvWindow | Maximum number of milliseconds the request remains valid after `timestamp` (default: `5000`)    |
| signature  | HMAC SHA256 signature of the full request query string or body, signed with your `API_SECRET`   |

In addition, include your `API_KEY` in the request header:

```
X-MBX-APIKEY: <your API_KEY>
```

### How to generate the signature

Concatenate all query parameters into a single string, then sign it with your `API_SECRET` using HMAC SHA256. Append the result as the `signature` parameter.

```javascript
const queryString = 'asset=USDT&amount=10&timestamp=1742198400000&recvWindow=5000';
const signature = CryptoJS.HmacSHA256(queryString, API_SECRET).toString();
const finalUrl = `${baseUrl}?${queryString}&signature=${signature}`;
```

> The `signature` parameter must always be the **last** parameter in the query string.

## Pro API-KEY Signature (V3)

With a Pro API key (V3), you will be issued a dedicated EOA wallet address and its corresponding private key. Every V3 request must include the following parameters:

| parameter | description                                                                                                          |
|-----------|----------------------------------------------------------------------------------------------------------------------|
| nonce     | Nanosecond timestamp, valid within 30 seconds. Use the [get server time](#get-server-time) API to obtain the current server time. |
| user      | The user's own wallet address                                                                                        |
| signer    | The issued EOA wallet address                                                                                        |
| signature | Signature of all request parameters, signed with the issued EOA wallet private key                                  |

### How to generate the signature

The V3 signature is an EIP712 typed data signature. Concatenate all query parameters into a single string as the message payload, then sign it with your issued EOA private key using `signTypedData`.

**EIP712 Domain**

```json
{
  "name": "AsterSignTransaction",
  "version": "1",
  "chainId": "<API_CHAINID>",
  "verifyingContract": "0x0000000000000000000000000000000000000000"
}
```

**EIP712 Types**

```json
{
  "Message": [
    { "name": "msg", "type": "string" }
  ]
}
```

**Value**

```json
{
  "msg": "<query string of all request parameters>"
}
```

**Example (JavaScript / ethers.js)**

```javascript
const domain = {
    name: 'AsterSignTransaction',
    version: '1',
    chainId: 1666,
    verifyingContract: ethers.ZeroAddress,
};

const types = {
    Message: [
        { name: 'msg', type: 'string' },
    ],
};

const queryString = 'nonce=1742198400000000000&user=0xYourAddress&signer=0xSignerAddress';
const value = { msg: queryString };

const wallet = new ethers.Wallet(API_PRIVATEKEY);
const signature = await wallet.signTypedData(domain, types, value);
const finalUrl = `${baseUrl}?${queryString}&signature=${signature}`;
```

> The `signature` parameter must always be the **last** parameter in the query string.

## EVM Withdraw Signature

* When you withdraw, you should supply an EIP712 signature. You can get the signature by signing the following message with your wallet.

### EIP712 Domain

```json
{
  "name": "Aster",
  "version": "1",
  "chainId": 56,
  "verifyingContract": "0x0000000000000000000000000000000000000000"
}
```

| field             | desc                                |
|-------------------|-------------------------------------|
| name              | Fixed string: `Aster`               |
| version           | Fixed string: `1`                   |
| chainId           | The chainId of the withdraw chain   |
| verifyingContract | Fixed address: zero address         |

### EIP712 Types

```json
{
  "Action": [
    {"name": "type", "type": "string"},
    {"name": "destination", "type": "address"},
    {"name": "destination Chain", "type": "string"},
    {"name": "token", "type": "string"},
    {"name": "amount", "type": "string"},
    {"name": "fee", "type": "string"},
    {"name": "nonce", "type": "uint256"},
    {"name": "aster chain", "type": "string"}
  ]
}
```

| field             | desc                                                                                                  |
|-------------------|-------------------------------------------------------------------------------------------------------|
| type              | Fixed string: `Withdraw`                                                                              |
| destination       | The receipt address; should be the user's registered address                                          |
| destination Chain | The chain name of the receipt address; see chainName definition below                                 |
| token             | The name of the currency the user withdraws, e.g., `ASTER`; get the name from the withdraw/asset API |
| amount            | The amount the user withdraws in token units, e.g., `1.23`                                            |
| fee               | The fee the user will pay in token units, e.g., `0.01`; get the fee from estimate-withdraw-fee API    |
| nonce             | A unique number; use the current timestamp in milliseconds multiplied by `1000`                       |
| aster chain       | Fixed string: `Mainnet`                                                                               |

### chainName definition

| chainId | chainName |
|---------|-----------|
| 1       | ETH       |
| 56      | BSC       |
| 42161   | Arbitrum  |

## Solana Withdraw Signature (optional)

When submitting a Solana withdrawal, you may optionally provide a valid signature. While the signature is not currently required, it will be enforced in a future release. It is strongly recommended to include one — only withdrawal requests carrying a valid signature will be recorded on the L1 chain.

### How to generate the signature

The Solana withdrawal signature is an **Ed25519 signature** over a structured message string, encoded in **Base58**.

**Message format**

Construct the message by joining the following fields with commas, in this exact order:

```
PrimaryType=Withdraw,AsterChain=Mainnet,Destination={destination},DestinationChain={destinationChain},Token={token},Amount={amount},Fee={fee},Nonce={nonce}
```

| field            | description                                                         |
|------------------|---------------------------------------------------------------------|
| Destination      | The recipient's Solana wallet address                               |
| DestinationChain | Fixed string: `Solana`                                              |
| Token            | Currency name, e.g., `USDT`                                         |
| Amount           | Withdraw amount with trailing zeros stripped, e.g., `1.2` not `1.20` |
| Fee              | Fee amount with trailing zeros stripped, e.g., `0.1` not `0.10`    |
| Nonce            | Nanosecond timestamp, e.g., `1773741793787000`                      |

**Example message**

```
PrimaryType=Withdraw,AsterChain=Mainnet,Destination=H7LqU4p4f8LDddADXDH9oFeoh3r7vhfJFf3XCEot8pkd,DestinationChain=Solana,Token=USDT,Amount=1.2,Fee=0.1,Nonce=1773741793787000
```

**Example (Node.js)**

```javascript
import { Keypair } from '@solana/web3.js';
import nacl from 'tweetnacl';
import bs58 from 'bs58';

const destination = 'H7LqU4p4f8LDddADXDH9oFeoh3r7vhfJFf3XCEot8pkd';
const destinationChain = 'Solana';
const token = 'USDT';
const amount = '1.2';
const fee = '0.1';
const nonce = Date.now() * 1000; // nanosecond-level timestamp

const message = `PrimaryType=Withdraw,AsterChain=Mainnet,Destination=${destination},DestinationChain=${destinationChain},Token=${token},Amount=${amount},Fee=${fee},Nonce=${nonce}`;

const messageBytes = Buffer.from(message, 'utf8');
const keypair = Keypair.fromSecretKey(bs58.decode(YOUR_PRIVATE_KEY));
const signatureBytes = nacl.sign.detached(messageBytes, keypair.secretKey);
const userSignature = bs58.encode(signatureBytes);
```

> Trailing zeros in `Amount` and `Fee` must be stripped (e.g., `1.20` → `1.2`). A mismatch will cause signature verification to fail.

# Withdrawal APIs

## withdraw by fapi \[evm\] \[futures\]

* Note: Follow the [API-KEY Signature (V1)](#api-key-signature-v1) instructions to generate the required request signature. The example below includes only the parameters specific to this endpoint.

### request:

```shell
curl --location --request POST 'https://fapi.asterdex.com/fapi/aster/user-withdraw?chainId=56&asset=USDT&amount=31&fee=0.3&receiver=0x000ae314e2a2172a039b26378814c252734f556a&nonce=1761210000000000&userSignature=0xde4ca529eef20db136eed1daf1d072083431d5279e6d6e219600cf57161c5e6d1232af3c8a8ef37ba8b5963f439ef9cc2b475fe18dcc3732dda9fb93c94a3abd1c' \
  --header 'Content-Type: application/json' \
  --header 'X-MBX-APIKEY: Your API KEY'
```

### params:

| param         | type   | required | description                                                         |
|---------------|--------|----------|---------------------------------------------------------------------|
| amount        | string | true     | Withdraw amount in token units                                      |
| chainId       | int    | true     | Chain ID                                                            |
| asset         | string | true     | Currency name, e.g., ASTER                                          |
| fee           | string | true     | Withdraw fee in token units                                         |
| nonce         | string | true     | Unique number; should be the same value used in signature           |
| receiver      | string | true     | Withdraw receipt address; should be the same as in signature        |
| userSignature | string | true     | EIP712 signature                                                    |

### response:

```json
{
    "withdrawId": "1234567",
    "hash": "0x9a40f0119b670fb6b155744b51981f91c4c4c8a20c333441a63853fe7d055c90"
}
```

| field      | desc                                 |
|------------|--------------------------------------|
| withdrawId | The withdraw request ID, a unique ID |
| hash       | The digest of the user's signature   |

## withdraw by API \[evm\] \[spot\]

### request:

```shell
curl --location --request POST 'https://sapi.asterdex.com/api/v1/aster/user-withdraw?chainId=56&asset=ASTER&amount=1&fee=0.095&receiver=0x000ae314e2a2172a039b26378814c252734f556a&nonce=1761222960000000&userSignature=0x39051cc68de0fefb8e823259d3f7014fc787a8008b65d2a89d70defc48c3f91b35a4a819718c22ffcaeb143c8e1735621a0768d7c69e45ad8fbcf9bd315988423b' \
  --header 'Content-Type: application/json' \
  --header 'X-MBX-APIKEY: Your API KEY'
```

### params:

| param         | type   | required | description                                                         |
|---------------|--------|----------|---------------------------------------------------------------------|
| amount        | string | true     | Withdraw amount in token units                                      |
| chainId       | int    | true     | Chain ID                                                            |
| asset         | string | true     | Currency name, e.g., ASTER                                          |
| fee           | string | true     | Withdraw fee in token units                                         |
| nonce         | string | true     | Unique number; should be the same value used in signature           |
| receiver      | string | true     | Withdraw receipt address; should be the same as in signature        |
| userSignature | string | true     | EIP712 signature                                                    |

### response:

```json
{
    "withdrawId": "1234567",
    "hash": "0x9a40f0119b670fb6b155744b51981f91c4c4c8a20c333441a63853fe7d055c90"
}
```

| field      | desc                                 |
|------------|--------------------------------------|
| withdrawId | The withdraw request ID, a unique ID |
| hash       | The digest of the user's signature   |

## withdraw by fapi \[solana\] \[futures\]

### request:

```shell
curl --location --request POST 'https://fapi.asterdex.com/fapi/aster/user-solana-withdraw?chainId=101&asset=USDT&amount=3&fee=0.6&receiver=4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf&userNonce=1773741793787000&userSignature=51pM5A46n5NzHYTtuzB7gh8FFfbkh4Aij1fceCZV2NtkiVvE7DADMnSvXFiUJvauKawdWaCfPhzCTVfXYcf1iteQ' \
  --header 'Content-Type: application/json' \
  --header 'X-MBX-APIKEY: Your API KEY'
```

### params:

| param         | type   | required | description                                                         |
|---------------|--------|----------|---------------------------------------------------------------------|
| amount        | string | true     | Withdraw amount in token units                                      |
| chainId       | int    | true     | Fixed value: `101`                                                  |
| asset         | string | true     | Currency name, e.g., USDT                                           |
| fee           | string | true     | Withdraw fee in token units                                         |
| receiver      | string | true     | Withdraw receipt address                                            |
| userNonce     | string | false    | Nanosecond timestamp; should be the same value used in signature. Not currently required but strongly recommended |
| userSignature | string | false    | Ed25519 withdraw signature encoded in Base58. Not currently required but strongly recommended                     |

### response:

```json
{
    "withdrawId": "1234567",
    "hash": "0x9a40f0119b670fb6b155744b51981f91c4c4c8a20c333441a63853fe7d055c90"
}
```

> Note: `hash` is not the transaction hash; it is just a unique identifier.

## withdraw by API \[solana\] \[spot\]

### request:

```shell
curl --location --request POST 'https://sapi.asterdex.com/api/v1/aster/user-solana-withdraw?chainId=101&asset=USDT&amount=0.97&fee=0.5&receiver=BzsJhmtg2UtQWNw6764DkK5Y4GPjc1XMzRqAGqSziymK&userNonce=1773741793787000&userSignature=51pM5A46n5NzHYTtuzB7gh8FFfbkh4Aij1fceCZV2NtkiVvE7DADMnSvXFiUJvauKawdWaCfPhzCTVfXYcf1iteQ' \
  --header 'Content-Type: application/json' \
  --header 'X-MBX-APIKEY: Your API KEY'
```

### params:

| param         | type   | required | description                                                                                                       |
|---------------|--------|----------|-------------------------------------------------------------------------------------------------------------------|
| amount        | string | true     | Withdraw amount in token units                                                                                    |
| chainId       | int    | true     | Fixed value: `101`                                                                                                |
| asset         | string | true     | Currency name, e.g., USDT                                                                                         |
| fee           | string | true     | Withdraw fee in token units                                                                                       |
| receiver      | string | true     | Withdraw receipt address                                                                                          |
| userNonce     | string | false    | Nanosecond timestamp; should be the same value used in signature. Not currently required but strongly recommended |
| userSignature | string | false    | Ed25519 withdraw signature encoded in Base58. Not currently required but strongly recommended                     |

### response:

```json
{
    "withdrawId": "1234567",
    "hash": "0x9a40f0119b670fb6b155744b51981f91c4c4c8a20c333441a63853fe7d055c90"
}
```

> Note: `hash` is not the transaction hash; it is just a unique identifier.

## withdraw by fapi\[v3\] \[evm\] \[futures\]

* Note: Follow the [Pro API-KEY Signature (V3)](#pro-api-key-signature-v3) instructions to generate the required request signature. The example below includes only the parameters specific to this endpoint.

### request:

```shell
curl --location --request POST 'https://fapi.asterdex.com/fapi/v3/aster/user-withdraw?chainId=56&asset=USDT&amount=31&fee=0.3&receiver=0x000ae314e2a2172a039b26378814c252734f556a&userNonce=1761210000000000&userSignature=0xde4ca529eef20db136eed1daf1d072083431d5279e6d6e219600cf57161c5e6d1232af3c8a8ef37ba8b5963f439ef9cc2b475fe18dcc3732dda9fb93c94a3abd1c' \
  --header 'Content-Type: application/json'
```

### params:

| param         | type   | required | description                                                                                                        |
|---------------|--------|----------|--------------------------------------------------------------------------------------------------------------------|
| amount        | string | true     | Withdraw amount in token units                                                                                     |
| chainId       | int    | true     | Chain ID                                                                                                           |
| asset         | string | true     | Currency name, e.g., ASTER                                                                                         |
| fee           | string | true     | Withdraw fee in token units                                                                                        |
| userNonce     | string | true     | Nanosecond timestamp for the EVM withdraw signature; separate from V3 API `nonce`, may differ by up to 1 hour     |
| receiver      | string | true     | Withdraw receipt address; should be the same as in signature                                                       |
| userSignature | string | true     | EIP712 withdraw signature                                                                                          |

### response:

```json
{
    "withdrawId": "1234567",
    "hash": "0x9a40f0119b670fb6b155744b51981f91c4c4c8a20c333441a63853fe7d055c90"
}
```

| field      | desc                                 |
|------------|--------------------------------------|
| withdrawId | The withdraw request ID, a unique ID |
| hash       | The digest of the user's signature   |

## withdraw by fapi\[v3\] \[solana\] \[futures\]

* Note: Follow the [Pro API-KEY Signature (V3)](#pro-api-key-signature-v3) instructions to generate the required request signature. The example below includes only the parameters specific to this endpoint.

### request:

```shell
curl --location --request POST 'https://fapi.asterdex.com/fapi/v3/aster/user-solana-withdraw?chainId=101&asset=USDT&amount=3&fee=0.6&receiver=4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf&userNonce=1773741793787000&userSignature=51pM5A46n5NzHYTtuzB7gh8FFfbkh4Aij1fceCZV2NtkiVvE7DADMnSvXFiUJvauKawdWaCfPhzCTVfXYcf1iteQ' \
  --header 'Content-Type: application/json'
```

### params:

| param         | type   | required | description                                                                                                                           |
|---------------|--------|----------|---------------------------------------------------------------------------------------------------------------------------------------|
| amount        | string | true     | Withdraw amount in token units                                                                                                        |
| chainId       | int    | true     | Fixed value: `101`                                                                                                                    |
| asset         | string | true     | Currency name, e.g., USDT                                                                                                             |
| fee           | string | true     | Withdraw fee in token units                                                                                                           |
| receiver      | string | true     | Withdraw receipt address                                                                                                              |
| userNonce     | string | false    | Nanosecond timestamp for the Solana withdraw signature; separate from V3 API `nonce`. Not currently required but strongly recommended |
| userSignature | string | false    | Ed25519 withdraw signature encoded in Base58. Not currently required but strongly recommended                                         |

### response:

```json
{
    "withdrawId": "1234567",
    "hash": "0x9a40f0119b670fb6b155744b51981f91c4c4c8a20c333441a63853fe7d055c90"
}
```

> Note: `hash` is not the transaction hash; it is just a unique identifier.

## withdraw by fapi\[v3\] \[evm\] \[spot\]

* Note: Follow the [Pro API-KEY Signature (V3)](#pro-api-key-signature-v3) instructions to generate the required request signature. The example below includes only the parameters specific to this endpoint.

### request:

```shell
curl --location --request POST 'https://sapi.asterdex.com/api/v3/aster/user-withdraw?chainId=56&asset=USDT&amount=31&fee=0.3&receiver=0x000ae314e2a2172a039b26378814c252734f556a&userNonce=1761210000000000&userSignature=0xde4ca529eef20db136eed1daf1d072083431d5279e6d6e219600cf57161c5e6d1232af3c8a8ef37ba8b5963f439ef9cc2b475fe18dcc3732dda9fb93c94a3abd1c' \
  --header 'Content-Type: application/json'
```

### params:

| param         | type   | required | description                                                                                                        |
|---------------|--------|----------|--------------------------------------------------------------------------------------------------------------------|
| amount        | string | true     | Withdraw amount in token units                                                                                     |
| chainId       | int    | true     | Chain ID                                                                                                           |
| asset         | string | true     | Currency name, e.g., ASTER                                                                                         |
| fee           | string | true     | Withdraw fee in token units                                                                                        |
| userNonce     | string | true     | Nanosecond timestamp for the EVM withdraw signature; separate from V3 API `nonce`, may differ by up to 1 hour     |
| receiver      | string | true     | Withdraw receipt address; should be the same as in signature                                                       |
| userSignature | string | true     | EIP712 withdraw signature                                                                                          |

### response:

```json
{
    "withdrawId": "1234567",
    "hash": "0x9a40f0119b670fb6b155744b51981f91c4c4c8a20c333441a63853fe7d055c90"
}
```

| field      | desc                                 |
|------------|--------------------------------------|
| withdrawId | The withdraw request ID, a unique ID |
| hash       | The digest of the user's signature   |

## withdraw by fapi\[v3\] \[solana\] \[spot\]

* Note: Follow the [Pro API-KEY Signature (V3)](#pro-api-key-signature-v3) instructions to generate the required request signature. The example below includes only the parameters specific to this endpoint.

### request:

```shell
curl --location --request POST 'https://sapi.asterdex.com/api/v3/aster/user-solana-withdraw?chainId=101&asset=USDT&amount=0.97&fee=0.5&receiver=BzsJhmtg2UtQWNw6764DkK5Y4GPjc1XMzRqAGqSziymK&userNonce=1773741793787000&userSignature=51pM5A46n5NzHYTtuzB7gh8FFfbkh4Aij1fceCZV2NtkiVvE7DADMnSvXFiUJvauKawdWaCfPhzCTVfXYcf1iteQ' \
  --header 'Content-Type: application/json'
```

### params:

| param         | type   | required | description                                                                                                                           |
|---------------|--------|----------|---------------------------------------------------------------------------------------------------------------------------------------|
| amount        | string | true     | Withdraw amount in token units                                                                                                        |
| chainId       | int    | true     | Fixed value: `101`                                                                                                                    |
| asset         | string | true     | Currency name, e.g., USDT                                                                                                             |
| fee           | string | true     | Withdraw fee in token units                                                                                                           |
| receiver      | string | true     | Withdraw receipt address                                                                                                              |
| userNonce     | string | false    | Nanosecond timestamp for the Solana withdraw signature; separate from V3 API `nonce`. Not currently required but strongly recommended |
| userSignature | string | false    | Ed25519 withdraw signature encoded in Base58. Not currently required but strongly recommended                                         |

### response:

```json
{
    "withdrawId": "1234567",
    "hash": "0x9a40f0119b670fb6b155744b51981f91c4c4c8a20c333441a63853fe7d055c90"
}
```

> Note: `hash` is not the transaction hash; it is just a unique identifier.