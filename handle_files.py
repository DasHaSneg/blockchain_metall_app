import json
import os
import zipfile
from datetime import datetime
from django.core.files.storage import FileSystemStorage


def upload_file_image(f, user_id):
    dest = './blockchain_web_app/files/image/' + str(user_id) + f.name
    if os.path.exists(dest):
        os.remove(dest)
    with open(dest, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return dest


def upload_file_json(data):
    name = 'test.json'
    dest = 'media/' + name
    with open(dest, 'w') as destination:
         destination.write(json.dumps(data))
    return name


def upload_csv_file(f, user_id, itr=0):
    dest = 'media/' + str(user_id) + str(itr) + '.csv'
    if os.path.exists(dest):
        os.remove(dest)
    with open(dest, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return dest


def handle_file_json(diplom_json, diplom_id, rec_name):
    dest_json = './chdi/files/json/' + str(diplom_id) + '_' + str(rec_name) + '.json'
    name = str(diplom_id) + '_' + str(rec_name) + '.json'
    with open(dest_json, 'w') as destination:
        json.dump(diplom_json, destination)
    return dest_json, name


def upload_file_zip(user_id, destinations_json):
    dest_zip = './chdi/files/zip/filezip' + str(user_id) + '.zip'
    z = zipfile.ZipFile(dest_zip, 'w')
    for d in destinations_json:
        z.write(d)
    z.close()
    return dest_zip


def handle_upload_json(f):
    diplom_json = f.read()
    return json.loads(diplom_json)


def load_json(filename):
    path = 'media/'
    with open(path + filename) as f:
        return f.read()
