import json
import requests
from pdiplom.issuer_diplom import hash_byte_array
import base64
from pdiplom.issuer_diplom import val_url
from tcontract.helper import URN_UUID_PREFIX


def check_tx(di_id):
    message = di_id
    message_bytes = message.encode('utf-8')
    mes ='0X' + message_bytes.hex().upper()
    response = requests.get(
        'http://'+val_url+':26657/abci_query?data=' + mes).json()
    try:
        response["error"]
    except KeyError:
        log_response = response["result"]["response"]["log"]
        value_response = response["result"]["response"]["value"]
        value_response = base64.b64decode(value_response).decode('utf-8')
        return log_response, value_response


def verify(json_file):
    info = json.loads(json_file)
    target_hash = info['targetHash']
    del info['targetHash']
    info_no_sign_byte = json.dumps(info).encode()
    hashed = hash_byte_array(info_no_sign_byte)
    info_id = info['id'].replace(URN_UUID_PREFIX, "")
    log_response, value_response = check_tx(info_id)
    if log_response == 'exists':
        message1 = 'exist'
    elif log_response == 'recalled':
        message1 = 'recalled'
    else:
        message1 = 'not exist'
    if hashed == value_response == target_hash:
        message2 = 'same'
    else:
        message2 = 'not same'
    return message1, message2


