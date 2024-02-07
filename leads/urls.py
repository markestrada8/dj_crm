from django.urls import path, include
from .views import lead_list, lead_detail, lead_create, lead_update, lead_delete

app_name = 'leads'

urlpatterns = [
    path('', lead_list, name='lead-list'),
    # SPECIFY DATATYPE ON PARAMETERS OR THE CASCADE HALTS?
    path('<int:id>/', lead_detail, name='lead-detail'),
    path('create/', lead_create, name='lead-create'),
    path('<int:id>/update/', lead_update, name='lead-update'),
    path('<int:id>/delete/', lead_delete, name='lead-delete'),
]