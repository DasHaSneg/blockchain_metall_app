from blockchain_web_app.models import ContractTemplate
from handle_files import upload_file_json
from tcontract.create_template import TemplateJson


def create_and_save_template_to_bd(form, request):
    user = request.user
    buyer = form.cleaned_data.get("buyer")
    supplier = form.cleaned_data.get("supplier")
    template = TemplateJson(buyer, supplier, user)
    contract_template = template.create_template()
    json_data = upload_file_json(contract_template)
    bd_temp = ContractTemplate(user_id=request.user, buyer=buyer, supplier=supplier, json_file=json_data)
    bd_temp.save()