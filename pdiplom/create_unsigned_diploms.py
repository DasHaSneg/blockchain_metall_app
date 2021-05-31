import copy
import csv
import hashlib
import json
import os
import uuid
import logging
from tcontract.helper import URN_UUID_PREFIX, create_iso8601_tz


class Recipient:
    def __init__(self, fields):
        self.name = fields.pop('name')
        self.identity = fields.pop('identity')
        self.additional_fields = fields


def hash_and_salt_email_address(email, salt):
    str = email + salt
    return 'sha256$' + hashlib.sha256(str.encode('utf-8')).hexdigest()


def instantiate_assertion(cert, uid, issued_on):
    cert['issuedOn'] = issued_on
    cert['id'] = URN_UUID_PREFIX + uid
    return cert


def instantiate_recipient(cert, recipient):

    salt = uuid.uuid4().hex
    cert['recipient']['hashed'] = True
    cert['recipient']['salt'] = salt

    cert['recipient']['identity'] = hash_and_salt_email_address(recipient.identity, salt)

    profile_field = 'recipientProfile'

    cert[profile_field] = {}
    cert[profile_field]['type'] = ['RecipientProfile', 'Extension']
    cert[profile_field]['name'] = recipient.name

    if recipient.additional_fields:
        logging.info('Error in csv file, too much fields')

def create_unsigned_diploms_from_file(roster, template_file):
    recipients = get_recipients_from_roster(roster)
    template = get_template(template_file)
    issued_on = create_iso8601_tz()
    diploms = {}
    for recipient in recipients:
        uid = str(uuid.uuid4())
        cert = copy.deepcopy(template)
        instantiate_assertion(cert, uid, issued_on)
        instantiate_recipient(cert, recipient)
        diploms[uid] = cert
    return diploms

def get_template(template_file):
        return json.loads(template_file)


def get_recipients_from_roster(roster):
    if os.path.exists(roster):
        with open(roster, 'r') as theFile:
            reader = csv.DictReader(theFile)
            recipients = map(lambda x: Recipient(x), reader)
            return list(recipients)
    else:
        logging.info('Error csv file is not exist')
