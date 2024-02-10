from django.urls import path, include
from .views import (
    # lead_list, lead_detail, lead_create, lead_update, lead_delete,
    LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView)

app_name = 'leads'

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'),
    # SPECIFY DATATYPE ON PARAMETERS OR THE CASCADE HALTS?
    path('<int:id>/', LeadDetailView.as_view(), name='lead-detail'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),
    path('<int:id>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:id>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
]