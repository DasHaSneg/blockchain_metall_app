"""
Creates a template
"""
import uuid

from tcontract.helper import URN_UUID_PREFIX, encode_image


class TemplateJson (object):

    def __init__(self, buyer, supplier, user):
        self.buyer = {
            'title': buyer.title,
            'phone': buyer.phone,
            'name': buyer.name,
            'inn': buyer.inn,
            'ogrn': buyer.ogrn,
            'address': buyer.address,
            'mail_address': buyer.mail_address,
            'email': buyer.email,
        }
        self.supplier = {
            'title': supplier.title,
            'phone': supplier.phone,
            'name': supplier.name,
            'inn': supplier.inn,
            'ogrn': supplier.ogrn,
            'address': supplier.address,
            'mail_address': supplier.mail_address,
            'email': supplier.email,
        }
        self.user = {
            'name': user.last_name + user.profile.patronymic + user.first_name,
            'job': user.profile.job,
            'signature_image': encode_image(user.profile.signature_image.path)
        }

    def create_template(self):
        assertion = create_assertion_section()
        assertion['responsible'] = self.user
        assertion['buyer'] = self.buyer
        assertion['supplier'] = self.supplier
        return assertion


def create_assertion_section():
    return {
        'issuedOn': '*|DATE|*',
        'id': URN_UUID_PREFIX + str(uuid.uuid4()),
        'specification': '*|List|*',
        'signedOn': '*|Data|*',
    }







