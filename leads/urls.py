from django.urls import path, include
from .views import lead_list, lead_detail, lead_create, lead_update

app_name = 'leads'

urlpatterns = [
    path('', lead_list),
    # SPECIFY DATATYPE ON PARAMETERS OR THE CASCADE HALTS?
    path('<int:id>/', lead_detail),
    path('create/', lead_create),
    path('update/<int:id>', lead_update),
]