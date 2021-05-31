from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('templates/', views.TemplateListView.as_view(), name='templates'),
    path('companies/', views.CompanyListView.as_view(), name='companies'),
    path('sign/', views.sign_template, name='template_sign'),
    path('recall/', views.recall_contract, name='template_recall'),
    path('profile/', views.watch_profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('template/<int:pk>', views.TemplateDetailView.as_view(), name='template-detail'),
    path('template/<int:pk>/delete/', views.TemplateDelete.as_view(), name='template_delete'),
    path('template/create/', views.create_template, name='template_create'),
    path('company/<int:pk>', views.CompanyDetailView.as_view(), name='company-detail'),
    path('company/<int:pk>/delete/', views.CompanyDelete.as_view(), name='company_delete'),
    path('company/create/', views.CompanyCreateView.as_view(), name='company_create'),
]