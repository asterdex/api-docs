## Table of Contents

- [Query APIs](#query-apis)
  - [get all deposit assets](#get-all-deposit-assets)
  - [get all withdraw assets](#get-all-withdraw-assets)
  - [estimate withdraw fee](#estimate-withdraw-fee)
  - [get server time](#get-server-time)
  - [get user withdraw info](#get-user-withdraw-info)
  - [get deposit and withdraw history](#get-deposit-and-withdraw-history)
  - [get user withdraw info \[v3\]](#get-user-withdraw-infov3)
  - [get deposit and withdraw history \[v3\]](#get-deposit-and-withdraw-historyv3)
- [Signature](#signature)
  - [API-KEY Signature (V1)](#api-key-signature-v1)
  - [Pro API-KEY Signature (V3)](#pro-api-key-signature-v3)
  - [EVM Withdraw Signature](#evm-withdraw-signature)
  - [Solana Withdraw Signature (optional)](#solana-withdraw-signature-optional)
- [Deposit](#deposit)
  - [EVM](#evm)
    - [Mainnet contract addresses](#mainnet-contract-addresses)
    - [depositFor](#depositfor)
  - [Solana](#solana)
    - [Mainnet program address](#mainnet-program-address)
    - [depositSol](#depositsol)
    - [depositToken](#deposittoken)
  - [SUI](#sui)
    - [get user deposit address \[v3\]](#get-user-deposit-address-v3)
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

## get user withdraw info

> **Deprecated:** This V1 interface will be discontinued in the future. Please migrate to the [V3 version](#get-user-withdraw-infov3).

* Note: Follow the [API-KEY Signature (V1)](#api-key-signature-v1) instructions to generate the required request signature.

### request:

```shell
curl --location --request POST 'https://fapi.asterdex.com/fapi/aster/user-withdraw-info?timestamp=1742198400000&recvWindow=5000&signature=<signature>' \
  --header 'X-MBX-APIKEY: Your API KEY'
```

### params:

No additional parameters required beyond the standard V1 signature parameters (`timestamp`, `recvWindow`, `signature`).

### response:

```json
{
    "userDailyLimit": "10000",
    "userRemainingDailyLimit": "9000",
    "totalDailyLimit": "1000000",
    "totalRemainingDailyLimit": "980000",
    "balances": {
        "USDT": {
            "currency": "USDT",
            "spotTotalWithdrawAmount": "500",
            "perpTotalWithdrawAmount": "300",
            "dailyLimit": "9000",
            "chainBalances": {
                "56": {
                    "chainId": 56,
                    "spotMaxWithdrawAmount": "500",
                    "perpMaxWithdrawAmount": "300",
                    "chainLimit": "800",
                    "withdrawFee": "0.5"
                }
            }
        }
    }
}
```

| field                    | desc                                                              |
|--------------------------|-------------------------------------------------------------------|
| userDailyLimit           | User's daily withdrawal limit, denominated in USD                |
| userRemainingDailyLimit  | User's remaining daily withdrawal limit, denominated in USD      |
| totalDailyLimit          | Global daily withdrawal limit, denominated in USD                |
| totalRemainingDailyLimit | Global remaining daily withdrawal limit, denominated in USD      |
| balances                 | Map of non-zero asset balances, keyed by asset name              |
| balances.currency        | Asset name                                                        |
| balances.spotTotalWithdrawAmount | Total spot balance available for withdrawal               |
| balances.perpTotalWithdrawAmount | Total futures balance available for withdrawal            |
| balances.dailyLimit      | Remaining daily withdrawal limit for this asset, denominated in USD |
| balances.chainBalances   | Per-chain balance info, keyed by chain ID                        |
| balances.chainBalances.chainId           | Chain ID                                          |
| balances.chainBalances.spotMaxWithdrawAmount | Max withdrawable spot amount on this chain        |
| balances.chainBalances.perpMaxWithdrawAmount | Max withdrawable futures amount on this chain     |
| balances.chainBalances.chainLimit        | Max withdrawable amount on this chain             |
| balances.chainBalances.withdrawFee       | Withdrawal fee on this chain                      |

## get deposit and withdraw history

> **Deprecated:** This V1 interface will be discontinued in the future. Please migrate to the [V3 version](#get-deposit-and-withdraw-historyv3).

* Note: Follow the [API-KEY Signature (V1)](#api-key-signature-v1) instructions to generate the required request signature.

### request:

```shell
curl --location --request POST 'https://fapi.asterdex.com/fapi/aster/deposit-withdraw-history?timestamp=1742198400000&recvWindow=5000&signature=<signature>' \
  --header 'X-MBX-APIKEY: Your API KEY'
```

### params:

No additional parameters required beyond the standard V1 signature parameters (`timestamp`, `recvWindow`, `signature`).

### response:

```json
[
    {
        "id": "1234567",
        "type": "DEPOSIT",
        "asset": "USDT",
        "amount": "100",
        "state": "SUCCESS",
        "txHash": "0x9a40f0119b670fb6b155744b51981f91c4c4c8a20c333441a63853fe7d055c90",
        "time": 1742198400000,
        "chainId": 56,
        "accountType": "spot"
    }
]
```

| field       | desc                                                                 |
|-------------|----------------------------------------------------------------------|
| id          | Record ID                                                            |
| type        | Record type: `DEPOSIT` or `WITHDRAW`                                 |
| asset       | Asset name, e.g., USDT                                               |
| amount      | Amount                                                               |
| state       | Status: `PROCESSING`, `SUCCESS`, or `FAILED`                         |
| txHash      | On-chain transaction hash                                            |
| time        | Record time in milliseconds (Unix)                                   |
| chainId     | Chain ID                                                             |
| accountType | Account type: `spot` or `perp`                                       |

## get user withdraw info\[v3\]

* Note: Follow the [Pro API-KEY Signature (V3)](#pro-api-key-signature-v3) instructions to generate the required request signature. The example below includes only the parameters specific to this endpoint.

### request:

```shell
curl --location --request POST 'https://fapi.asterdex.com/fapi/v3/aster/user-withdraw-info' \
  --header 'Content-Type: application/json'
```

### params:

No additional parameters required beyond the standard V3 signature parameters.

### response:

```json
{
    "userDailyLimit": "10000",
    "userRemainingDailyLimit": "9000",
    "totalDailyLimit": "1000000",
    "totalRemainingDailyLimit": "980000",
    "balances": {
        "USDT": {
            "currency": "USDT",
            "spotTotalWithdrawAmount": "500",
            "perpTotalWithdrawAmount": "300",
            "dailyLimit": "9000",
            "chainBalances": {
                "56": {
                    "chainId": 56,
                    "spotMaxWithdrawAmount": "500",
                    "perpMaxWithdrawAmount": "300",
                    "chainLimit": "800",
                    "withdrawFee": "0.5"
                }
            }
        }
    }
}
```

| field                    | desc                                                              |
|--------------------------|-------------------------------------------------------------------|
| userDailyLimit           | User's daily withdrawal limit, denominated in USD                |
| userRemainingDailyLimit  | User's remaining daily withdrawal limit, denominated in USD      |
| totalDailyLimit          | Global daily withdrawal limit, denominated in USD                |
| totalRemainingDailyLimit | Global remaining daily withdrawal limit, denominated in USD      |
| balances                 | Map of non-zero asset balances, keyed by asset name              |
| balances.currency        | Asset name                                                        |
| balances.spotTotalWithdrawAmount | Total spot balance available for withdrawal               |
| balances.perpTotalWithdrawAmount | Total futures balance available for withdrawal            |
| balances.dailyLimit      | Remaining daily withdrawal limit for this asset, denominated in USD |
| balances.chainBalances   | Per-chain balance info, keyed by chain ID                        |
| balances.chainBalances.chainId           | Chain ID                                          |
| balances.chainBalances.spotMaxWithdrawAmount | Max withdrawable spot amount on this chain        |
| balances.chainBalances.perpMaxWithdrawAmount | Max withdrawable futures amount on this chain     |
| balances.chainBalances.chainLimit        | Max withdrawable amount on this chain             |
| balances.chainBalances.withdrawFee       | Withdrawal fee on this chain                      |

## get deposit and withdraw history\[v3\]

* Note: Follow the [Pro API-KEY Signature (V3)](#pro-api-key-signature-v3) instructions to generate the required request signature. The example below includes only the parameters specific to this endpoint.

### request:

```shell
curl --location --request POST 'https://fapi.asterdex.com/fapi/v3/aster/deposit-withdraw-history' \
  --header 'Content-Type: application/json'
```

### params:

No additional parameters required beyond the standard V3 signature parameters.

### response:

```json
[
    {
        "id": "1234567",
        "type": "DEPOSIT",
        "asset": "USDT",
        "amount": "100",
        "state": "SUCCESS",
        "txHash": "0x9a40f0119b670fb6b155744b51981f91c4c4c8a20c333441a63853fe7d055c90",
        "time": 1742198400000,
        "chainId": 56,
        "accountType": "spot"
    }
]
```

| field       | desc                                                                 |
|-------------|----------------------------------------------------------------------|
| id          | Record ID                                                            |
| type        | Record type: `DEPOSIT` or `WITHDRAW`                                 |
| asset       | Asset name, e.g., USDT                                               |
| amount      | Amount                                                               |
| state       | Status: `PROCESSING`, `SUCCESS`, or `FAILED`                         |
| txHash      | On-chain transaction hash                                            |
| time        | Record time in milliseconds (Unix)                                   |
| chainId     | Chain ID                                                             |
| accountType | Account type: `spot` or `perp`                                       |

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
| 131     | SUI       |

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

# Deposit

## EVM

Deposits are made by interacting directly with the vault contract on the source chain. There are two ways to deposit:

1. Call the `depositFor` method of the vault contract. Once the transaction is confirmed on-chain, the deposited asset is credited to the `forAddress` account.
2. Transfer the token directly to the vault contract address. The deposited asset is credited to the sending address.

* Use the [get all deposit assets](#get-all-deposit-assets) API to query the supported tokens and their contract addresses on each chain.

### Mainnet contract addresses

| chain    | chainId | contract address                             |
|----------|---------|----------------------------------------------|
| ETH      | 1       | `0x604DD02d620633Ae427888d41bfd15e38483736E` |
| BSC      | 56      | `0x128463A60784c4D3f46c23Af3f65Ed859Ba87974` |
| Arbitrum | 42161   | `0x9E36CB86a159d479cEd94Fa05036f235Ac40E1d5` |

### depositFor

```solidity
function depositFor(address currency, address forAddress, uint256 amount, uint256 broker) external payable
```

| param      | type    | description                                                                                                                                              |
|------------|---------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| currency   | address | Token contract address. For the native token (e.g., BNB, ETH), pass the fixed placeholder address `0xfdAE1bA7C826aBDc4c99903c8056f82a1A04a615`             |
| forAddress | address | The user's address that receives the deposited asset                                                                                                       |
| amount     | uint256 | Deposit amount in the token's smallest unit (wei). For the native token, it must equal `msg.value`                                                         |
| broker     | uint256 | Target account flag: pass `1000` to deposit to the **spot** account; any other value deposits to the **futures** account                                   |

> Notes:
> * For ERC20 deposits, `approve` the vault contract to spend the token before calling `depositFor`, and `msg.value` must be `0`.
> * For native token deposits, send the amount via `msg.value`; it must equal the `amount` parameter.
> * The token must be in the supported deposit asset list, otherwise the transaction reverts with `CurrencyNotSupport`.

**Example (ethers.js)**

```javascript
const vaultAbi = [
    'function depositFor(address currency, address forAddress, uint256 amount, uint256 broker) external payable',
];
const erc20Abi = [
    'function approve(address spender, uint256 amount) external returns (bool)',
    'function decimals() external view returns (uint8)',
];

const vaultAddress = '0x128463A60784c4D3f46c23Af3f65Ed859Ba87974'; // BSC mainnet
const usdtAddress = '0x55d398326f99059fF775485246999027B3197955'; // USDT on BSC

const wallet = new ethers.Wallet(PRIVATE_KEY, provider);
const vault = new ethers.Contract(vaultAddress, vaultAbi, wallet);
const usdt = new ethers.Contract(usdtAddress, erc20Abi, wallet);

// deposit 100 USDT to the user's futures account (pass broker = 1000 for the spot account)
const amount = ethers.parseUnits('100', await usdt.decimals());
await (await usdt.approve(vaultAddress, amount)).wait();
await (await vault.depositFor(usdtAddress, wallet.address, amount, 0)).wait();
```

## Solana

On Solana, deposits can **only** be made by calling the program methods below. Transferring SOL or tokens directly to the vault address will **not** be credited.

There are two deposit methods:

1. `depositSol`: deposit the native token (SOL).
2. `depositToken`: deposit an SPL token, e.g., USDT.

* Use the [get all deposit assets](#get-all-deposit-assets) API with `networks=SOLANA` to query the supported tokens and the account addresses (`admin`, `solVault`, `bank`, `tokenVaultAuthority`, `tokenVault`, `tokenMint`, etc.) required by the methods.
* Target account: for both methods, append the `programId` account (the program address) as the **last** account of the instruction to deposit to the **spot** account; omit it to deposit to the **futures** account.

### Mainnet program address

| network | program address                                |
|---------|------------------------------------------------|
| Solana  | `EhUtRgu9iEbZXXRpEvDj6n1wnQRjMi2SERDo3c6bmN2c` |

### depositSol

Deposit native SOL. The deposited asset is credited to the `signer` address.

**args:**

| arg    | type | description                |
|--------|------|-----------------------------|
| amount | u64  | Deposit amount in lamports |

**accounts:**

| account       | isSigner | isMut | description                                                        |
|---------------|----------|-------|---------------------------------------------------------------------|
| signer        | true     | true  | The depositor's wallet address                                     |
| admin         | false    | false | Admin account; from the get all deposit assets API (`admin`)       |
| solVault      | false    | true  | SOL vault account; from the get all deposit assets API (`solVault`) |
| systemProgram | false    | false | Fixed: `11111111111111111111111111111111`                          |
| programId     | false    | false | Optional; must be the **last** account. The program address `EhUtRgu9iEbZXXRpEvDj6n1wnQRjMi2SERDo3c6bmN2c`. Provide it to deposit to the **spot** account; omit it to deposit to the **futures** account |

**Example (Node.js / Anchor)**

```javascript
const tx = await program.methods.depositSol(amount)
    .accounts({
        signer: walletKeypair.publicKey,
        admin: admin,
        solVault: solVault,
        systemProgram: anchor.web3.SystemProgram.programId,
    })
    // deposit to the spot account; remove the following line to deposit to the futures account
    .remainingAccounts([{ pubkey: program.programId, isSigner: false, isWritable: false }])
    .signers([walletKeypair])
    .rpc();
```

### depositToken

Deposit an SPL token. The deposited asset is credited to the `signer` address.

**args:**

| arg    | type | description                                  |
|--------|------|-----------------------------------------------|
| amount | u64  | Deposit amount in the token's smallest unit |

**accounts:**

| account                | isSigner | isMut | description                                                                          |
|------------------------|----------|-------|---------------------------------------------------------------------------------------|
| signer                 | true     | false | The depositor's wallet address                                                       |
| admin                  | false    | false | Admin account; from the get all deposit assets API (`admin`)                         |
| bank                   | false    | false | Bank account of the token; from the get all deposit assets API (`bank`)              |
| tokenVaultAuthority    | false    | false | Token vault authority; from the get all deposit assets API (`tokenVaultAuthority`)   |
| tokenVault             | false    | true  | Token vault account; from the get all deposit assets API (`tokenVault`)              |
| depositor              | false    | true  | The depositor's associated token account of `tokenMint`                              |
| tokenMint              | false    | false | Token mint address; from the get all deposit assets API (`tokenMint`)                |
| tokenProgram           | false    | false | Fixed: `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`                                 |
| associatedTokenProgram | false    | false | Fixed: `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`                                |
| systemProgram          | false    | false | Fixed: `11111111111111111111111111111111`                                            |
| programId              | false    | false | Optional; must be the **last** account. The program address `EhUtRgu9iEbZXXRpEvDj6n1wnQRjMi2SERDo3c6bmN2c`. Provide it to deposit to the **spot** account; omit it to deposit to the **futures** account |

**Example (Node.js / Anchor)**

```javascript
const tx = await program.methods.depositToken(amount)
    .accounts({
        signer: walletKeypair.publicKey,
        admin: admin,
        bank: bank,
        tokenVaultAuthority: tokenVaultAuthority,
        tokenVault: tokenVault,
        depositor: userTokenAccount,
        tokenMint: tokenMint,
        tokenProgram: TOKEN_PROGRAM_ID,
        associatedTokenProgram: ASSOCIATED_TOKEN_PROGRAM_ID,
        systemProgram: anchor.web3.SystemProgram.programId,
    })
    // deposit to the spot account; remove the following line to deposit to the futures account
    .remainingAccounts([{ pubkey: program.programId, isSigner: false, isWritable: false }])
    .signers([walletKeypair])
    .rpc();
```

## SUI

> **Note:** On SUI, only the **spot** account is supported.

Deposits on SUI are made by transferring the asset directly to your dedicated deposit address — no contract call is required:

1. Call the [get user deposit address \[v3\]](#get-user-deposit-address-v3) API to get your deposit address on SUI.
2. Transfer the asset directly to that address; once the transaction is confirmed on-chain, it is credited to your spot account.

### get user deposit address \[v3\]

* Note: Follow the [Pro API-KEY Signature (V3)](#pro-api-key-signature-v3) instructions to generate the required request signature. The example below includes only the parameters specific to this endpoint.

#### request:

```shell
curl --location --request GET 'https://sapi.asterdex.com/api/v3/aster/user-deposit-address?network=SUI' \
  --header 'Content-Type: application/json'
```

#### params:

| param   | type   | required | description                   |
|---------|--------|----------|--------------------------------|
| network | string | false    | Network type. Default: `SUI` |

#### response:

```json
{
    "network": "SUI",
    "address": "0x9a40f0119b670fb6b155744b51981f91c4c4c8a20c333441a63853fe7d055c90"
}
```

| field   | desc                                              |
|---------|----------------------------------------------------|
| network | Network type                                      |
| address | The user's dedicated deposit address on the chain |

# Withdrawal APIs

## withdraw by fapi \[evm\] \[futures\]

> **Deprecated:** This V1 interface will be discontinued in the future. Please migrate to the [V3 version](#withdraw-by-fapiv3-evm-futures).

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

> **Deprecated:** This V1 interface will be discontinued in the future. Please migrate to the [V3 version](#withdraw-by-fapiv3-evm-spot).

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

> **Deprecated:** This V1 interface will be discontinued in the future. Please migrate to the [V3 version](#withdraw-by-fapiv3-solana-futures).

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

> **Deprecated:** This V1 interface will be discontinued in the future. Please migrate to the [V3 version](#withdraw-by-fapiv3-solana-spot).

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
| signatureType | string | false    | Signature type: `EOA` or `SafeWallet`. Default: `EOA`. Pass `SafeWallet` if the account is a Safe wallet           |
| userSignature | string | true     | EIP712 withdraw signature. When `signatureType=SafeWallet`, multiple signatures are supported, separated by commas |

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

| param            | type   | required | description                                                                                                        |
|------------------|--------|----------|--------------------------------------------------------------------------------------------------------------------|
| amount           | string | true     | Withdraw amount in token units                                                                                     |
| chainId          | int    | true     | Chain ID of the chain the asset belongs to                                                                        |
| signatureChainId | int    | false    | Chain ID of the chain used for signing (the `chainId` field of the EIP712 domain). Defaults to `chainId`           |
| asset            | string | true     | Currency name, e.g., ASTER                                                                                         |
| fee              | string | true     | Withdraw fee in token units                                                                                        |
| userNonce        | string | true     | Nanosecond timestamp for the EVM withdraw signature; separate from V3 API `nonce`, may differ by up to 1 hour      |
| receiver         | string | true     | Withdraw receipt address; should be the same as in signature                                                       |
| signatureType    | string | false    | Signature type: `EOA` or `SafeWallet`. Default: `EOA`. Pass `SafeWallet` if the account is a Safe wallet           |
| userSignature    | string | true     | EIP712 withdraw signature. When `signatureType=SafeWallet`, multiple signatures are supported, separated by commas |

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