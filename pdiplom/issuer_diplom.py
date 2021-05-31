import requests
from pdiplom.create_unsigned_diploms import create_unsigned_diploms_from_file
import hashlib
import base64
import json
import logging
import csv
import os

from tcontract.helper import create_iso8601_tz, URN_UUID_PREFIX

val_url = 'localhost'


def connection_on():
    """Pings Google to see if the internet is on. If online, returns true. If offline, returns false."""
    try:
        requests.get('http://google.com')
        return True
    except requests.exceptions.RequestException:
        return False


def connection_rpc_on():
    """
     Pings Tendermint node
    :return: boolean
    """
    url = "http://"+ val_url+":26657/status"
    try:
        requests.post(url).json()
    except requests.exceptions.ConnectionError:
        return False
    return True


def hash_byte_array(data):
    return hashlib.sha256(data).hexdigest()


def broadcast_tx(uid, hashed):
    """
    Broadcasting a transaction containing a hash to a Tendermint node
    :param uid:
    :param hashed:
    :return:
    """
    url = "http://"+ val_url+":26657"
    message = uid + '=' + hashed
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    payload = {
        "id": -1,
        "jsonrpc": "2.0",
        "method": "broadcast_tx_sync",
        "params": [base64_message]
    }
    response = requests.post(url, json=payload).json()
    try:
        response["error"]
    except KeyError:
        return response["result"]["hash"], False
    else:
        return response["error"]["data"], True


def sign_contract(roster, template_file):
    template = get_template(template_file)
    template['specification'] = get_items_from_roster(roster)
    template['issuedOn'] = create_iso8601_tz()

    template_json_byte = template.encode()
    hashed_template = hash_byte_array(template_json_byte)
    result, err = broadcast_tx(template['id'].replace(URN_UUID_PREFIX, ""), hashed_template)
    if err:
        message = result
    else:
        message = 'Диплом успешно добавлен'
        template['targetHash'] = hashed_template

    return template, message


class Item:
    def __init__(self, fields):
        self.id = fields.pop('id')
        self.name = fields.pop('name')
        self.unit_price = fields.pop('unit_price')
        self.unit_of_measurement = fields.pop('unit_of_measurement')
        self.amount = fields.pop('amount')
        self.country = fields.pop('country')


def get_items_from_roster(roster):
    if os.path.exists(roster):
        with open(roster, 'r') as theFile:
            reader = csv.DictReader(theFile)
            items = map(lambda x: Item(x), reader)
            return list(items)
    else:
        logging.info('Error csv file is not exist')


def get_template(template_file):
    return json.loads(template_file)
