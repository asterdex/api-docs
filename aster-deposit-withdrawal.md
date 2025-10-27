# 1. get all deposit assets

### request:

```shell
curl 'https://www.asterdex.com/bapi/futures/v1/public/future/aster/deposit/assets?chainIds=56&networks=EVM&accountType=spot'
```

### params:
|param      | type   | required | description                                                            |
|-----------|--------|----------|------------------------------------------------------------------------|
| chainIds  | string | true     | Chain ID, multiple IDs separated by commas                             |
| networks  | string | false    | Network type, e.g., EVM, SOLANA, multiple networks separated by commas |
| accountType | string | true   | Account type, e.g., spot, perp                                         |

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

# 2. get all withdraw assets

### request:

```shell
curl 'https://www.asterdex.com/bapi/futures/v1/public/future/aster/withdraw/assets?chainIds=56&networks=EVM&accountType=spot'
```

### params:
|param      | type   | required | description                                                            |
|-----------|--------|----------|------------------------------------------------------------------------|
| chainIds  | string | true     | Chain ID, multiple IDs separated by commas                             |
| networks  | string | false    | Network type, e.g., EVM, SOLANA, multiple networks separated by commas |
| accountType | string | true   | Account type, e.g., spot, perp                                         |

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

# 3. estimate withdraw fee

### request:

```shell
curl 'https://www.asterdex.com/bapi/futures/v1/public/future/aster/estimate-withdraw-fee?chainId=56&network=EVM&currency=ASTER&accountType=spot'
```

### params:

|param       | type   | required | description                  |
|------------|--------|----------|------------------------------|
| chainId    | int    | true     | Chain ID                     |
| network    | string | true     | Network type, e.g., EVM, SOL |
| currency   | string | true     | Currency name, e.g., ASTER   |
| accountType | string | true    | Account type, e.g., spot, perp |

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

- gasCost: Estimated withdrawal fee in token units

# 4. withdraw signature

* when you withdraw, you should supply a EIP712 signature. You can get the signature by signing the following message with your wallet.

### EIP712 Domain

```json
{
  "name": "Aster",
  "version": "1",
  "chainId": 56,
  "verifyingContract": "0x0000000000000000000000000000000000000000"
}
```

|field|desc|
|---|---|
|name|fix string 'Aster'|
|version|fix string '1'|
|chainId|the chainId of withdraw chain|
|verifyingContract|fix address: zero address|

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

|field          | desc                                                                                                  |
|---------------|-------------------------------------------------------------------------------------------------------|
|type           | fix string 'Withdraw'                                                                                 |
|destination    | the receipt address, should be user's register address                                                |
|destination Chain | the chain name of receipt address, you can see the defination of chainName below                      |
|token| the name of the currency user withdraw, e.g. ASTER, you can get the name from withdraw/asset API      |
|amount | the amount user withdraw in token unit, eg. '1.23'                                                    |
|fee| the fee user will pay in token unit, eg. '0.01' (you can get the fee from withdraw/estimate-withdraw-fee API) |
|nonce| a unique number, use the current timestamp in milliseconds and multiply '1000'                        |
|aster chain| fix string 'Mainnet'                                                                                  |

### chainName definition

|chainId| chainName |
|---|-----------|
|56| BSC       |
|42161| Arbitrum  |
|1| ETH       |

# 5. withdraw

### request:

```shell
curl -X POST "https://www.asterdex.com/bapi/futures/v1/private/future/aster/user-withdraw" -H "accept: */*" -H "x-gray-env: normal" -H "x-trace-id: fa2a5961b4a346e083f2bb0bffe39e2f" -H "Content-Type: application/json" \
-d "{ \"accountType\": \"spot\", \"amount\": \"10.2\", \"chainId\": 97, \"currency\": \"USDT\", \"fee\": \"0.01\", \"nonce\": \"1761029928213000\", \"receiver\": \"0x4C5EdB66CC7626a1C92d5178c3E5c45409BcE6D7\", \"userSignature\": \"0xc0299efe235ec194d070163b1f92ebf5d01bd820c1c08fa9730929c7a36172a9001b99203b2f9997aa7d41b7658348704e0515f4c40e76f1892f7a5b0af31daa1c\"}"
```

### params:
|param         | type   | required | description                                               |
|--------------|--------|----------|-----------------------------------------------------------|
| accountType  | string | true     | Account type, e.g., spot, perp                            |
| amount       | string | true     | Withdraw amount in token unit                             |
| chainId      | int    | true     | Chain ID                                                  |
| currency     | string | true     | Currency name, e.g., ASTER                                |
| fee          | string | true     | Withdraw fee in token unit                                |
| nonce        | string | true     | Unique number, should be the save in signature            |
| receiver     | string | true     | Withdraw receipt address, should be the save in signature |
| userSignature | string | true    | EIP712 signature                                         |

### response:

```json
{
  "code": "200",
  "message": "success",
  "messageDetail": null,
  "data": {
    "withdrawId": "1234567",
    "hash": "0x9a40f0119b670fb6b155744b51981f91c4c4c8a20c333441a63853fe7d055c90"
  },
  "success": true
}
```

|field      | desc                                 |
|-----------|--------------------------------------|
|withdrawId | the withdraw request id, a unique id |
|hash       | the digest of user's signature       |

# 6. withdraw by API [futures]

### request:

```shell
curl --location --request POST 'https://fapi.asterdex.com/fapi/aster/user-withdraw?chainId=56&asset=USDT&amount=31&fee=0.3&receiver=0x000ae314e2a2172a039b26378814c252734f556a&nonce=1761210000000000&userSignature=0xde4ca529eef20db136eed1daf1d072083431d5279e6d6e219600cf57161c5e6d1232af3c8a8ef37ba8b5963f439ef9cc2b475fe18dcc3732dda9fb93c94a3abd1c&recvWindow=60000&timestamp=1761230958410&signature=f5fd60da19be213d58914dd6f46bc400ada610fb916998dfc01dd346bfdad512' \
--header 'Content-Type: application/json' \
--header 'X-MBX-APIKEY: Your API KEY'
```

### params:
| param         | type   | required | description                                               |
|---------------|--------|----------|-----------------------------------------------------------|
| amount        | string | true     | Withdraw amount in token unit                             |
| chainId       | int    | true     | Chain ID                                                  |
| asset         | string | true     | Currency name, e.g., ASTER                                |
| fee           | string | true     | Withdraw fee in token unit                                |
| nonce         | string | true     | Unique number, should be the save in signature            |
| receiver      | string | true     | Withdraw receipt address, should be the save in signature |
| userSignature | string | true    | EIP712 signature                                         |

### response:

```json
{
  "code": "200",
  "message": "success",
  "messageDetail": null,
  "data": {
    "withdrawId": "1234567",
    "hash": "0x9a40f0119b670fb6b155744b51981f91c4c4c8a20c333441a63853fe7d055c90"
  },
  "success": true
}
```

|field      | desc                                 |
|-----------|--------------------------------------|
|withdrawId | the withdraw request id, a unique id |
|hash       | the digest of user's signature       |

# 7. withdraw by API [spot]

### request:

```shell
curl --location --request POST 'https://sapi.asterdex.com/api/v1/aster/user-withdraw?chainId=56&asset=ASTER&amount=1&fee=0.095&receiver=0x000ae314e2a2172a039b26378814c252734f556a&nonce=1761222960000000&userSignature=0x39051cc68de0fefb8e823259d3f7014fc787a8008b65d2a89d70defc48c3f91b35a4a819718c22ffcaeb143c8e1735621a0768d7c69e45ad8fbcf9bd315988423b&recvWindow=60000&timestamp=1761230958410&signature=f5fd60da19be213d58914dd6f46bc400ada610fb916998dfc01dd346bfdad51' \
--header 'Content-Type: application/json' \
--header 'X-MBX-APIKEY: Your API KEY'
```

### params:
| param         | type   | required | description                                               |
|---------------|--------|----------|-----------------------------------------------------------|
| amount        | string | true     | Withdraw amount in token unit                             |
| chainId       | int    | true     | Chain ID                                                  |
| asset         | string | true     | Currency name, e.g., ASTER                                |
| fee           | string | true     | Withdraw fee in token unit                                |
| nonce         | string | true     | Unique number, should be the save in signature            |
| receiver      | string | true     | Withdraw receipt address, should be the save in signature |
| userSignature | string | true    | EIP712 signature                                         |

### response:

```json
{
  "code": "200",
  "message": "success",
  "messageDetail": null,
  "data": {
    "withdrawId": "1234567",
    "hash": "0x9a40f0119b670fb6b155744b51981f91c4c4c8a20c333441a63853fe7d055c90"
  },
  "success": true
}
```

|field      | desc                                 |
|-----------|--------------------------------------|
|withdrawId | the withdraw request id, a unique id |
|hash       | the digest of user's signature       |