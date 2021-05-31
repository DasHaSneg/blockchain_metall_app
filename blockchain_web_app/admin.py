from django.contrib import admin
from .models import Profile, Company, ContractTemplate

admin.site.register(Profile)
admin.site.register(Company)
admin.site.register(ContractTemplate)