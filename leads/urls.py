from django.urls import path, include
from .views import (
    LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView, AssignAgentView,
    CategoryListView, CategoryDetailView, LeadCategoryUpdateView
    )

app_name = 'leads'

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'),
    # SPECIFY DATATYPE ON PARAMETERS OR THE CASCADE HALTS?
    path('<int:id>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<int:id>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),
    path('<int:id>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:id>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:id>/', CategoryDetailView.as_view(), name='category-detail'),
    path('<int:id>/category', LeadCategoryUpdateView.as_view(), name='lead-category-update'),
]