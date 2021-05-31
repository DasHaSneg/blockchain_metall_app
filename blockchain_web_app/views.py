from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, DeleteView, CreateView

from blockchain_web_app.forms import ContractTemplateCreateForm, ContractTemplateSignForm, TemplateRecallForm
from blockchain_web_app.models import ContractTemplate, Company
from blockchain_web_app.utils.create_and_save_template_to_bd import create_and_save_template_to_bd
from handle_files import handle_upload_json
from blockchain_web_app.utils.process_file_signature import process_file_signature
from pdiplom.issuer_diplom import connection_rpc_on, broadcast_tx
from vcontract.json_formatter import get_formatted_verification_info
from vcontract.verifier import verify


def index(request):
    if request.method == 'POST':
        if not connection_rpc_on():
            error = 'Нет связи с сервером'
            return render(
                request,
                'info_page.html',
                {'message': error}
            )
        file = request.FILES['filesjson']
        json_byte_file = file.read()
        json_file = json_byte_file.decode()

        m1, m2 = verify(json_file)
        if m1 == 'exist' and m2 == 'same':
            verification_result = 1
        elif m1 == 'recalled':
            verification_result = 2
        else:
            verification_result = 0

        info = get_formatted_verification_info(json_file, verification_result)
        return render(
            request,
            'award.html',
            info
        )
    return render(
        request,
        'index.html'
    )


@login_required
def create_template(request):
    if request.method == 'POST':
        form = ContractTemplateCreateForm(request.POST, request.FILES)
        if form.is_valid():
            create_and_save_template_to_bd(form, request)
            return HttpResponseRedirect(reverse('templates'))
    else:
        form = ContractTemplateCreateForm()
    return render(
        request,
        'create_template.html',
        {'form': form}
    )


@login_required
def sign_template(request):
    if request.method == 'POST':
        form = ContractTemplateSignForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            if not connection_rpc_on():
                error = 'Нет связи с сервером'
                return render(
                    request,
                    'info_page.html',
                    {'message': error}
                )
            return process_file_signature(request)
    else:
        form = ContractTemplateSignForm(request.user)
    return render(
        request,
        'sign_template.html',
        {'form': form}
    )


@login_required
def recall_contract(request):
    if request.method == 'POST':
        form = TemplateRecallForm(request.POST, request.FILES)
        if form.is_valid():
            if not connection_rpc_on():
                error = 'Нет связи с сервером'
                return render(
                    request,
                    'info_page.html',
                    {'message': error}
                )
            contract = handle_upload_json(request.FILES['diplom_file'])
            contract_id = contract['id'].replace(PREFIX_UID, "")
            result, error = broadcast_tx(contract_id, 'deleted')
            if error:
                printed_res = result
            else:
                printed_res = 'Крнтракт успешно отозван'
            return render(
                request,
                'info_page.html',
                {'message': printed_res}
            )
    else:
        form = TemplateRecallForm()
    return render(
        request,
        'recall_diplom.html',
        {'form': form}
    )


@login_required
def watch_profile(request):
    user = request.user
    return render(
        request,
        'profile.html',
        {'user': user}
    )


class TemplateListView(LoginRequiredMixin, ListView):
    """Generic class-based view for a list of templates."""
    model = ContractTemplate

    def get_queryset(self):
        return ContractTemplate.objects.filter(user_id=self.request.user)


class TemplateDetailView(LoginRequiredMixin, DetailView):
    """Generic class-based detail view for a template."""
    model = ContractTemplate


class TemplateDelete(LoginRequiredMixin, DeleteView):
    model = ContractTemplate
    success_url = reverse_lazy('templates')


class CompanyCreateView(LoginRequiredMixin, CreateView):
    """Generic class-based view for a list of templates."""
    model = Company
    fields = '__all__'
    success_url = reverse_lazy('companies')



class CompanyListView(LoginRequiredMixin, ListView):
    """Generic class-based view for a list of templates."""
    model = Company


class CompanyDetailView(LoginRequiredMixin, DetailView):
    """Generic class-based detail view for a template."""
    model = Company


class CompanyDelete(LoginRequiredMixin, DeleteView):
    model = Company
    success_url = reverse_lazy('companies')
