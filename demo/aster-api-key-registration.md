# 1. get nonce

### request:

```shell
curl --location 'https://www.asterdex.com/bapi/futures/v1/public/future/web3/get-nonce' \
--header 'Content-Type: application/json' \
--data '{
"sourceAddr" : "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266",
"type": "CREATE_API_KEY"
}
```

### response:
```json
{
    "code": "000000",
    "message": null,
    "messageDetail": null,
    "data": {
        "nonce": "501182"
    },
    "success": true
}
```

# 2. sign message

### message:

```text
You are signing into Astherus 501182
```

### result:

```text
0x<signature>
```

# 3. login

### request:
```shell
curl -XPOST 'https://www.asterdex.com/bapi/futures/v1/public/future/web3/ae/login' \
  -H 'clientType: broker' \
  -H 'content-type: application/json' \
  --data-raw '{
  "signature":"0xafb84ca3bd36131970636a298677be2e1de4ed81b11101e417272d23f0b7f9af174efdf954ae7a63e844c83d16a4ad391e801c6766a422e647832b5c0c8aa1591c",
  "sourceAddr":"0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266",
  "chainId":56,
  "agentCode": "56789"
  }'
```

### params:

| param       | type | required | description                            |
|-------------|------|----------|----------------------------------------|
| signature   | string | yes | signature from previous step           |
| sourceAddr  | string | yes | the address used to sign the message   |
| chainId     | int | yes | blockchain network id, e.g. 56 for BSC |
| agentCode | string | no  | referral code                          |

### response:

```json
{
  "code": "000000",
  "message": null,
  "messageDetail": null,
  "data": {
    "token": "<login-token>",
    "uid": 12345678
  },
  "success": true
}
```

# 4. create api-key

### request:

```shell
curl --location 'https://www.asterdex.com/bapi/futures/v1/public/future/web3/broker-create-api-key' \
--header 'clientType: broker' \
--header 'accept: */*' \
--header 'Content-Type: application/json' \
--data '{
"desc": "test description",
"ip": "",
"network": "56",
"signature": "0x<signature>",
"sourceAddr": "0x<your-wallet-address>",
"type": "CREATE_API_KEY",
"sourceCode": "broker"
}'
```

### params:

|param | type | required | description                               |
|------|------|----------|-------------------------------------------|
| desc | string | yes | api-key's description, should unique      |
| ip   | string | no  | whitelist ip addresses, separated by ','  |
| network | string | yes | blockchain network, e.g. '56' for BSC     |
| signature | string | yes | signature from previous step              |
| sourceAddr | string | yes | the address used to sign the message      |
| type | string | yes | fixed value "CREATE_API_KEY"              |
| sourceCode | string | no  | "ae" for aster and other value for broker |

### response:

```json
{
  "code": "000000",
  "message": null,
  "messageDetail": null,
  "data": {
    "apiKey": "<api-key>",
    "apiSecret": "<api-secret>",
    "keyId": 0,
    "apiName": null
  },
  "success": true
}
```

### note:

1. Please keep a record of the returned apiKey and apiSecret. If you lose them, you cannot retrieve them and can only create them again.
2. api-key can't be deleted by user now.