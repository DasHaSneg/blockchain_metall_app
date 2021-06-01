import json

from django.http import HttpResponse

from blockchain_web_app.models import ContractTemplate
from handle_files import upload_csv_file, load_json
from pdiplom.issuer_diplom import sign_contract


def process_file_signature(request):
    user_id = request.user.id
    template = request.POST['user_template']
    template = ContractTemplate.objects.get(pk=template)
    csv_file_path = upload_csv_file(request.FILES['roster'], user_id)
    json_data = load_json(template.json_file.name)
    signed_template, message = sign_contract(csv_file_path, json_data)
    response = HttpResponse(json.dumps(signed_template), content_type='application/json"')
    filename = 'signed_contract.json'
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response