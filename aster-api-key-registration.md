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
You are signing into Aster DEX 501182
```

### result:

```text
0xa4ee6b068060caeac447216b592a918b085642056248e6ff50ba22b50e8884875ead28f06cbcefcbb93d03997f807fd242354d878756f4690f791ae8dbfcde841c
```

# 3. create api-key

### request:

```shell
curl --location 'https://www.asterdex.com/bapi/futures/v1/public/future/web3/broker-create-api-key' \
--header 'accept: */*' \
--header 'Content-Type: application/json' \
--data '{
"desc": "test description",
"ip": "",
"network": "56",
"signature": "0xa4ee6b068060caeac447216b592a918b085642056248e6ff50ba22b50e8884875ead28f06cbcefcbb93d03997f807fd242354d878756f4690f791ae8dbfcde841c",
"sourceAddr": "0xE90F9596e3Bfd49e9f4c2E0eA48830DC47e6997b",
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
    "apiKey": "4a2e11b243b1ad75981edf359ae02e873bf88b699196170d998d8266f5eb9f32",
    "apiSecret": "72911505f67b24a8efe8f246d06c324b787d2f3f7cb8b5b80ef1698ee1486e25",
    "keyId": 0,
    "apiName": null
  },
  "success": true
}
```

### note:

1. Please keep a record of the returned apiKey and apiSecret. If you lose them, you cannot retrieve them and can only create them again.
2. api-key can't be deleted by user now.