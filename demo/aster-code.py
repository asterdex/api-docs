import time

import requests
from eth_account import Account
from eth_account.messages import  encode_structured_data
from copy import deepcopy
import json

host = 'https://fapi.asterdex.com'
aster_chain = 'Mainnet'
chain_id = 1666

# aster_chain = 'Testnet'
# chain_id = 714

user = '0x014c85ffb0fF2F2972237AA950B452f92C69Ae1D'
main_private_key = '*'


signer = '0xC98Fd64eBc39E28b92849d9cCef9495663439014'
priKey =  '*'

builder = '0x014c85ffb0fF2F2972237AA950B452f92C69Ae1D'
approveAgent = {'url': '/fapi/v3/approveAgent', 'method': 'POST',
              'params':{'agentName': 'ivanbuilder','agentAddress':signer,
                      'ipWhitelist':'', 'expired':1967945395040,'canSpotTrade':True,
                        'canPerpTrade':False,  'canWithdraw':False}
    ,'main':True,"primary_type":"ApproveAgent"}

updateAgent = {'url': '/fapi/v3/updateAgent', 'method': 'POST',
              'params':{'agentAddress':signer,'ipWhitelist':'101.198.86.182,192.168.1.100,192.168.1.101',
                        'canSpotTrade':False, 'canPerpTrade':True,  'canWithdraw':False},'main':True,"primary_type":"UpdateAgent"}

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



# 模板只包含 EIP712Domain
eip712_template = {
    "types": {
        "EIP712Domain": [
            {"name": "name", "type": "string"},
            {"name": "version", "type": "string"},
            {"name": "chainId", "type": "uint256"},
            {"name": "verifyingContract", "type": "address"}
        ]
    },
    "primaryType": "",
    "domain": {
        "name": "AsterSignTransaction",
        "version": "1",
        "chainId": 56,
        "verifyingContract": "0x0000000000000000000000000000000000000000"
    },
    "message": {}
}

def infer_eip712_type(value):
    """根据 Python 值推断 EIP-712 类型"""
    if isinstance(value, bool):
        return "bool"
    elif isinstance(value, int):
        # 这里假设所有整数都是 uint256
        return "uint256"
    else:
        return "string"

def build_dynamic_eip712_with_infer(template: dict, primary_type: str, values: dict) -> dict:
    eip712_data = deepcopy(template)
    eip712_data["primaryType"] = primary_type

    # 自动生成主类型 fields
    type_fields = []
    for name, val in values.items():
        type_fields.append({"name": name, "type": infer_eip712_type(val)})

    eip712_data["types"][primary_type] = type_fields

    # 填充 message
    eip712_data["message"] = values
    return eip712_data

def sign_v3_eip712(private_key, message, primary_type) -> str:
    new_dict = {k[:1].upper() + k[1:]: v for k, v in message.items()}

    sign_data = build_dynamic_eip712_with_infer(
        template=eip712_template,
        primary_type=primary_type,
        values=new_dict
    )
    # sign_data['message'] = new_dict

    data = json.dumps(sign_data, indent=2)
    print(data)

    print(sign_data)
    msg = encode_structured_data(sign_data)
    signed = Account.sign_message(msg, private_key=private_key)
    return signed.signature.hex()

def get_url(my_dict) -> str:
    if my_dict is None:
        return ''
    if len(my_dict) == 0:
        return ''
    return '&'.join(f'{key}={str(value)}'for key, value in my_dict.items())

def sign_v3(private_key, message) -> str:
  typed_data_sign = {
      "types": {
          "EIP712Domain": [
              {"name": "name", "type": "string"},
              {"name": "version", "type": "string"},
              {"name": "chainId", "type": "uint256"},
              {"name": "verifyingContract", "type": "address"}
          ],
          "Message": [
              {"name": "msg", "type": "string"}
          ]
      },
      "primaryType": "Message",
      "domain": {
          "name": "AsterSignTransaction",
          "version": "1",
          "chainId": chain_id,
          "verifyingContract": "0x0000000000000000000000000000000000000000"
      },
      "message": {
          "msg": message
      }
  }
  # print(typed_data_sign)
  # print(message)

  msg = encode_structured_data(typed_data_sign)
  signed = Account.sign_message(msg, private_key=private_key)
  print(signed.signature.hex())

  return signed.signature.hex()

_last_ms = 0
_i = 0

def get_nonce():
    global _last_ms, _i
    now_ms = int(time.time())

    if now_ms == _last_ms:
        _i += 1
    else:
        _last_ms = now_ms
        _i = 0

    return now_ms * 1_000_000 + _i

def send_by_url(method_config):
    param = method_config['params']
    config_url = method_config['url']
    method = method_config['method']
    primary_type = method_config.get('primary_type')
    sign_private_key = main_private_key
    main = method_config.get('main') is not None

    param['asterChain'] = aster_chain
    param['user'] = user
    if not main:
        sign_private_key = priKey
        param['signer'] = signer

    nonce = get_nonce()
    param['nonce'] = nonce

    url = ''
    signature =''
    if main:
        signature =  sign_v3_eip712(sign_private_key, param, primary_type)
        param['signature'] = signature
        param['signatureChainId'] = 56

        # url = host + config_url + '?' + get_url(param)
        url = host + config_url

    else:
        url_param = get_url(param)
        url = host + config_url + '?' + url_param
        signature = sign_v3(sign_private_key, url_param)
        url = url + '&signature=' + signature


    print(signature)
    print(url)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'PythonApp/1.0'
    }

    if method == 'POST':
        res = requests.post(url, headers=headers,data=param)
        print(res.text)
    if method == 'GET':
        res = requests.get(url, headers=headers)
        print(res.text)
    if method == 'DELETE':
        # res = requests.delete(url, headers=headers)
        res = requests.delete(url, headers=headers,data=param)

        print(res.text)


if __name__ == '__main__':
    send_by_url(approveAgent)
    # send_by_url(updateAgent)
    # send_by_url(getAgents)
    # send_by_url(delAgent)

    # send_by_url(approveBuilder)
    # send_by_url(getBuilders)
    # send_by_url(updateBuilder)
    # send_by_url(delBuilder)
    # send_by_url(placeOrder)



