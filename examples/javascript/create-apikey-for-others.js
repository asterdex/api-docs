const ethers = require('ethers');
const crypto = require('crypto');
const axios = require('axios');


//需要生成apikey的账户信息
const new_address_config = [
    {
        private_key: "*",
        address: '*',
    },
    {
        private_key: "*",
        address: '*',
    }
]

//主账户的地址 apikey api_secret
const api_key = '*'
const api_secret = '*'


//下面的参数无需修改
const host = 'https://sapi.asterdex.com'

var new_address_apikey = ''
var new_address_apiSecret = ''
var use_new_apikey = false

const spot_get_nonce = { 'url': '/api/v1/getNonce', 'method': 'POST', 'params': {  'userOperationType': 'CREATE_API_KEY' } }
const spot_create_apikey = { 'url': '/api/v1/createApiKey', 'method': 'POST', 'params': { 'userOperationType': 'CREATE_API_KEY' } }

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
    i = 0
    for (const config of new_address_config) {
        console.log('开始为账户创建apikey:', config.address);
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
     
        console.log('new address: ',config.address)
        console.log('new_address_apikey:', new_address_apikey)
        console.log('new_address_apiSecret:', new_address_apiSecret)
    }
}


main()

