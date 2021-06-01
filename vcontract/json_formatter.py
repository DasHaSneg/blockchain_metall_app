import json


def get_formatted_verification_info(file_json, verification_result):
    """
    Formatting a json file into the dictionary used for displaying on the page

    :param file_json:
    :param verification_result:
    :return: dict
    """
    info = json.loads(file_json)
    issued_on = info['signedOn'][8:10] + "." + info['signedOn'][5:7] + "."+ info['signedOn'][0:4]
    return {
        'buyer': info['buyer']['title'],
        'supplier': info['supplier']['title'],
        'specification': info['specification'],
        'responsible_name': info['responsible']['name'],
        'responsible_job': info['responsible']['job'],
        'signature_img':  info['responsible']['signature_image'],
        'issued_on': issued_on,
        'verification_result': verification_result,
    }




