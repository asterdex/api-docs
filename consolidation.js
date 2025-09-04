const ethers = require('ethers');
const crypto = require('crypto');
const http = require('http');
const axios = require('axios');
const { Wallet } = require('ethers');


//待归集的账户信息
const new_address_config = [
    {
        private_key: "*",
        address: '*',
        'asset': 'CDL',
        'amount': '1',
    },
    {
        private_key: "*",
        address: '*',
        'asset': 'CDL',
        'amount': '1',
    }
]

const host = 'https://sapi.asterdex.com'

//主账户私钥
const main_WALLET_PRIVATE_KEY = "*";
//主账户钱包
const main_wallet = new ethers.Wallet(main_WALLET_PRIVATE_KEY);
//主账户的地址 apikey api_secret
const main_address = '*'
const api_key = '*'
const api_secret = '*'


const withdraw_nonce = Date.now() + '000'
const withdraw_asset = 'CDL'
const withdraw_amount = '1'
const network = 'BSC'   //主网使用 BSC
const chainId = 56  //主网使用 56


//下面的参数无需修改
var new_address_apikey = ''
var new_address_apiSecret = ''
var use_new_apikey = false

const spot_get_nonce = { 'url': '/api/v1/getNonce', 'method': 'POST', 'params': {  'userOperationType': 'CREATE_API_KEY' } }
const spot_create_apikey = { 'url': '/api/v1/createApiKey', 'method': 'POST', 'params': { 'userOperationType': 'CREATE_API_KEY' } }
const spot_send_toAddress = { 'url': '/api/v1/asset/sendToAddress', 'method': 'POST', 'params': {} }

// #chainId: 1(ETH),56(BSC),42161(Arbi)
const spot_withdraw_estimateFee = { 'url': '/api/v1/aster/withdraw/estimateFee', 'method': 'GET', 'params': { 'asset': withdraw_asset, "chainId": chainId } }
const spot_withdraw = { 'url': '/api/v1/aster/user-withdraw', 'method': 'POST', 'params': { "chainId": chainId } }


const domain = {
    name: 'Aster',
    version: '1',
    chainId: chainId,
    verifyingContract: ethers.ZeroAddress
}

const types = {
    Action: [
        { name: "type", type: "string" },
        { name: "destination", type: "address" },
        { name: "destination Chain", type: "string" },
        { name: "token", type: "string" },
        { name: "amount", type: "string" },
        { name: "fee", type: "string" },
        { name: "nonce", type: "uint256" },
        { name: "aster chain", type: "string" },
    ],
}


var value = {
    'type': 'Withdraw',
    'destination': main_address,
    'destination Chain': network,
    'token': withdraw_asset,
    'amount': withdraw_amount,
    'fee': '',
    'nonce': withdraw_nonce,
    'aster chain': 'Mainnet',
}

async function getUrl(my_dict) {
    content = ''
    for (let key in my_dict) {
        content = content + key + '=' + my_dict[key] + '&'
    }
    content += 'recvWindow=5000&timestamp=' + Date.now()

    return content

}

async function sign_v1(secretKey, message) {
    const hmac = crypto.createHmac('sha256', secretKey)
        .update(message)
        .digest('hex');
    return hmac
}

async function sendRequest(url, method) {
    headers = {}
    key = api_key
    if (use_new_apikey == true) {
        key = new_address_apikey
    }
    if (method == 'POST') {
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-MBX-APIKEY': key,
            'User-Agent': 'Node.js HTTP Client'
        }
    }
    try {
        const response = await axios({
            method: method, 
            url: url,
            headers: headers

        });

        return response.data;
    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
    }

    return ''
}

async function send_v1(path, method, my_dict) {
    content = await getUrl(my_dict)
    secret = api_secret
    if (use_new_apikey == true) {
        secret = new_address_apiSecret
    }
    signature = await sign_v1(secret, content)
    path = path + '?' + content + '&signature=' + signature
    return await sendRequest(host + path, method)
}


async function generateSignature() {
    try {
        const signature = await main_wallet.signTypedData(domain, types, value);
        return signature;
    } catch (error) {
        console.error("签名生成失败:", error);
        throw error;
    }
}

async function send(config, addParams) {
    path = config['url']
    method = config['method']
    my_dict = { ...config['params'], ...addParams }
    return await send_v1(path, method, my_dict)
}

async function sign(private_key, message) {
    wallet = new ethers.Wallet(private_key);
    const signature = await wallet.signMessage(message);
    return signature
}

async function main() {
    //循环归集
    i = 0
    for (const config of new_address_config) {
        console.log('开始归集账户:', config.address);
        //获取创建apikey的nonce
        let nonce = await send(spot_get_nonce, {'address': config.address})

        //给新地址创建api_key api_secret
        message = 'You are signing into Astherus ${nonce}'.replace('${nonce}', nonce)
        userSignature = await sign(config.private_key,message)
        
        //创建apikey时的描述信息 注意同一账户的desc不能重复
        var key_desc = Date.now() +'_' + i
        i = i + 1
        let new_api = await send(spot_create_apikey, { 'userSignature': userSignature,'address': config.address,'desc': key_desc })
        new_address_apikey = new_api['apiKey']
        new_address_apiSecret = new_api['apiSecret']
     
        console.log('new_address_apikey:', new_address_apikey)
        console.log('new_address_apiSecret:', new_address_apiSecret)

        use_new_apikey = true
        //归集 使用新生成的apikey api_secret 将新地址的CDL转账到老地址账户
        sendToMainAddressRes = await send(spot_send_toAddress, { 'asset': config.asset, "amount": config.amount, "toAddress": main_address })
        console.log('sendToMainAddressRes:', sendToMainAddressRes)
        use_new_apikey = false
        if(sendToMainAddressRes['status'] = 'SUCCESS'){
            console.log('归集成功:', config.address);
        }else{
            console.log('归集失败:', config.address);
        }
    }


    estimateFee = await send(spot_withdraw_estimateFee, {})
    console.log('estimateFee:', estimateFee)


    //归集和提现的手续费 代币 数量配置
    fee = estimateFee['gasCost']
    value.fee = fee*1.5+''
    console.log('提现手续费:', value.fee)


    withdraw_ignature = await generateSignature()

    //使用老账户进行提现操作
    spotWithdraw = await send(spot_withdraw, {
        'fee':  value.fee, 'nonce': withdraw_nonce,
        'userSignature': withdraw_ignature, 'receiver': main_address, 'asset': withdraw_asset, 'amount': withdraw_amount
    })

    if(spotWithdraw['hash'] != ''){
        console.log('提现成功:', spotWithdraw['hash']);
    }else{
        console.log('提现失败:', spotWithdraw);
    }

}


main()

