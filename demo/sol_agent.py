import threading
import urllib

import base58
from eth_account import Account
from eth_account.messages import encode_structured_data
from nacl.signing import SigningKey
import time
import requests

# ⚠️  WARNING: Replace these with your own addresses and keys before use.
user = 'YOUR_SOLANA_PUBLIC_KEY'
base58_private_key = 'YOUR_SOLANA_PRIVATE_KEY'
signer = '0xYOUR_AGENT_WALLET_ADDRESS'
signer_pri_key =  '0xYOUR_AGENT_PRIVATE_KEY'

builder = '0xYOUR_BUILDER_ADDRESS'
host = 'https://fapi3.asterdex.com'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'PythonApp/1.0'
}

typed_data = {
  "types": {
    "EIP712Domain": [
      {"name": "name", "type": "string"},
      {"name": "version", "type": "string"},
      {"name": "chainId", "type": "uint256"},
      {"name": "verifyingContract", "type": "address"}
    ],
    "Message": [
      { "name": "msg", "type": "string" }
    ]
  },
  "primaryType": "Message",
  "domain": {
    "name": "AsterSignTransaction",
    "version": "1",
    "chainId": 1666,
    "verifyingContract": "0x0000000000000000000000000000000000000000"
  },
  "message": {
    "msg": "$msg"
  }
}

approveAgent = {'url': '/fapi/v3/approveAgent', 'method': 'POST',
              'params':{'agentName':'acc' ,'agentAddress':signer,
                      'ipWhitelist':'', 'expired':1967945395040,'canSpotTrade':True,
                        'canPerpTrade':False,  'canWithdraw':False}
    ,'main':True,"primary_type":"ApproveAgent"}

updateAgent = {'url': '/fapi/v3/updateAgent', 'method': 'POST',
              'params':{'agentAddress':signer,'ipWhitelist':'',
                        'canSpotTrade':True, 'canPerpTrade':True,  'canWithdraw':False},'main':True,"primary_type":"UpdateAgent"}

delAgent = {'url': '/fapi/v3/agent', 'method': 'DELETE',
              'params':{'agentAddress':signer},'main':True,"primary_type":"DelAgent"}

getAgents = {'url': '/fapi/v3/agent', 'method': 'GET',
              'params':{}}

approveBuilder = {'url': '/fapi/v3/approveBuilder', 'method': 'POST',
                  'params': {'builder': builder,
                             'maxFeeRate': '0.00001','builderName':'ivan3' }, 'main': True,"primary_type":"ApproveBuilder"}

updateBuilder = {'url': '/fapi/v3/updateBuilder', 'method': 'POST',
              'params':{'builder': builder,'maxFeeRate': '0.00002'},'main':True,"primary_type":"UpdateBuilder"}

delBuilder = {'url': '/fapi/v3/builder', 'method': 'DELETE',
              'params':{'builder':builder},'main':True,"primary_type":"DelBuilder"}
getBuilders = {'url': '/fapi/v3/builder', 'method': 'GET', 'params':{}}

placeOrder = {'url': '/fapi/v3/order', 'method': 'POST',
              'params':{'symbol': 'BTCUSDT', 'type': 'MARKET','builder':builder,'feeRate':0.00001, 'side': 'BUY','quantity': "0.03"}}

def sign(message, all_bytes=None) :
    # 要签名的数据
    # 创建 signing key
    if len(all_bytes) == 64:
        all_bytes = all_bytes[:32]

    signing_key = SigningKey(all_bytes)
    # 签名
    signed = signing_key.sign(message.encode())
    # signature
    signature = signed.signature

    print("message:", message)
    print("signature base58:", base58.b58encode(signature).decode())
    print("signature hex:", signature.hex())
    return base58.b58encode(signature).decode()

_last_ms = 0
_i = 0
_nonce_lock = threading.Lock()

def get_nonce():
    global _last_ms, _i
    with _nonce_lock:
        now_ms = int(time.time())

        if now_ms == _last_ms:
            _i += 1
        else:
            _last_ms = now_ms
            _i = 0

        return now_ms * 1_000_000 + _i

def send_by_url(api) :
    my_dict = api['params']
    url = host + api['url']
    method = api['method']
    main = api.get('main') is not None

    my_dict['nonce'] = str(get_nonce())
    my_dict['user'] = user
    print(str(get_nonce()))

    signature = ''
    param = ''
    if main:
        param = urllib.parse.urlencode(my_dict)
        print(param)
        signature = sign(param,base58.b58decode(base58_private_key))
    else:
        my_dict['signer'] = signer
        param = urllib.parse.urlencode(my_dict)
        print(param)
        typed_data['message']['msg'] = param
        message = encode_structured_data(typed_data)
        signature = Account.sign_message(message, private_key=signer_pri_key).signature.hex()

    url = url + '?' + param + '&signature=' + signature
    print(url)
    if method == 'POST':
        print(signature)
        res = requests.post(url, headers=headers)
        print(res.text)
    if method == 'GET':
        print(signature)
        res = requests.get(url, headers=headers)
        print(res.text)
    if method == 'DELETE':
        res = requests.delete(url, headers=headers)
        print(res.text)

if __name__ == '__main__':
   send_by_url(approveAgent)
   # send_by_url(updateAgent)
   # send_by_url(delAgent)
   # send_by_url(getAgents)
   # send_by_url(approveBuilder)
   # send_by_url(updateBuilder)
   # send_by_url(delBuilder)
   # send_by_url(getBuilders)
   # send_by_url(placeOrder)
