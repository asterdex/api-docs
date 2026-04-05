const ethers = require('ethers');
const crypto = require('crypto');
const axios = require('axios');

const { Wallet } = require('ethers');

//下面的参数无需修改
const host = 'https://www.asterdex.com/bapi/futures/v1'
const get_nonce = { 'url': '/public/future/web3/get-nonce', 'method': 'POST', 'params': { } }
const create_apikey = { 'url': '/public/future/web3/broker-create-api-key', 'method': 'POST', 'params': { 'network': '56','type':'CREATE_API_KEY','sourceCode':'ae','ip':'' } }
const ae_login = { 'url': '/public/future/web3/ae/login', 'method': 'POST', 'params': { 'chainId': '56' } }

async function sendRequest(url, method,body) {
    headers = {}
    url = host+url
    if (method == 'POST') {
        headers = {
            'Content-Type': 'application/json',
            'clientType':'web'
        }
    }
    try {
        const response = await axios({
            method: method, 
            data: body,
            url: url,
            headers: headers

        });

        return response.data;
    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
    }

    return ''
}


async function send(config, addParams) {
    path = config['url']
    method = config['method']
    my_dict = { ...config['params'], ...addParams }
    return await sendRequest(path, method, my_dict)
}

async function sign(private_key, message) {
    wallet = new ethers.Wallet(private_key);
    const signature = await wallet.signMessage(message);
    return signature
}

async function main() {
    const wallet = Wallet.createRandom();

    console.log("Address:", wallet.address);
    console.log("Private Key:", wallet.privateKey);

    let login_nonce_res = await send(get_nonce, {'type':'LOGIN','sourceAddr':wallet.address})
    let nonce = login_nonce_res['data']['nonce']
    console.log(nonce)
    //地址登陆 header必传 'clientType':'web' 
    let message = 'You are signing into Astherus ${nonce}'.replace('${nonce}', nonce)
    let user_signature = await sign( wallet.privateKey,message)
    console.log(user_signature)
    let ae_login_res = await send(ae_login, {'signature':user_signature,'sourceAddr':wallet.address,'agentCode':'69Ae1D'})
    console.log(ae_login_res)

    let apikey_nonce_res = await send(get_nonce, {'type':'CREATE_API_KEY','sourceAddr':wallet.address})
    nonce = apikey_nonce_res['data']['nonce']
    console.log(nonce)
    //给新地址创建api_key api_secret
    message = 'You are signing into Astherus ${nonce}'.replace('${nonce}', nonce)
    user_signature = await sign( wallet.privateKey,message)
    console.log(user_signature)
    let create_api_key_res = await send(create_apikey, {'signature':user_signature,'desc':'12','sourceAddr':wallet.address})
    console.log(create_api_key_res)

}

main()



