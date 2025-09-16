
#Python 3.9.6
# eth-account~=0.13.7
# eth-abi~=5.2.0
# web3~=7.11.0
# requests~=2.32.3
# pip install -r requirements.txt

import json
import math
import time
import requests

from eth_abi import encode
from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3

user = '0x63DD5aCC6b1aa0f563956C0e534DD30B6dcF7C4e'
signer='0x21cF8Ae13Bb72632562c6Fff438652Ba1a151bb0'
priKey = "0x4fd0a42218f3eae43a6ce26d22544e986139a01e5b34a62db53757ffca81bae1"

host = 'https://fapi.asterdex.com'

placeOrder = {'url': '/fapi/v3/order', 'method': 'POST',
              'params':{'symbol': 'SANDUSDT', 'positionSide': 'BOTH', 'type': 'LIMIT', 'side': 'BUY',
	         'timeInForce': 'GTC', 'quantity': "30", 'price': 0.325,'reduceOnly': True}}
getOrder = {'url':'/fapi/v3/order','method':'GET','params':{'symbol':'SANDUSDT','side':"BUY","type":'LIMIT','orderId':2194215}}

def call(api):
    nonce = math.trunc(time.time() * 1000000)
    my_dict = api['params']
    send(api['url'],api['method'],sign(my_dict,nonce))

def sign(my_dict,nonce):
    my_dict = {key: value for key, value in my_dict.items() if  value is not None}
    my_dict['recvWindow'] = 50000
    my_dict['timestamp'] = int(round(time.time()*1000))
    msg = trim_param(my_dict,nonce)
    signable_msg = encode_defunct(hexstr=msg)
    signed_message = Account.sign_message(signable_message=signable_msg, private_key=priKey)
    my_dict['nonce'] = nonce
    my_dict['user'] = user
    my_dict['signer'] = signer
    my_dict['signature'] = '0x'+signed_message.signature.hex()

    print(my_dict['signature'])
    return  my_dict

def trim_param(my_dict,nonce) -> str:
    _trim_dict(my_dict)
    json_str = json.dumps(my_dict, sort_keys=True).replace(' ', '').replace('\'','\"')
    print(json_str)
    encoded = encode(['string', 'address', 'address', 'uint256'], [json_str, user, signer, nonce])
    print(encoded.hex())
    keccak_hex =Web3.keccak(encoded).hex()
    print(keccak_hex)
    return keccak_hex

def _trim_dict(my_dict) :
    for key in my_dict:
        value = my_dict[key]
        if isinstance(value, list):
            new_value = []
            for item in value:
                if isinstance(item, dict):
                    new_value.append(json.dumps(_trim_dict(item)))
                else:
                    new_value.append(str(item))
            my_dict[key] = json.dumps(new_value)
            continue
        if isinstance(value, dict):
            my_dict[key] = json.dumps(_trim_dict(value))
            continue
        my_dict[key] = str(value)

    return my_dict

def send(url, method, my_dict):
    url = host + url
    print(url)
    print(my_dict)
    if method == 'POST':
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'PythonApp/1.0'
        }
        res = requests.post(url, data=my_dict, headers=headers)
        print(res.text)
    if method == 'GET':
        res = requests.get(url, params=my_dict)
        print(res.text)
    if method == 'DELETE':
        res = requests.delete(url, data=my_dict)
        print(res.text)

if __name__ == '__main__':
    # call(placeOrder)
    call(getOrder)
