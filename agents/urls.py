from django.urls import path
from .views import AgentListView, AgentCreateView, AgentDetailView, AgentUpdateView, AgentDeleteView

app_name = 'agents'

urlpatterns = [
    path('', AgentListView.as_view(), name='agent-list'),
    path('create/', AgentCreateView.as_view(), name='agent-create'),
    path('<int:id>/', AgentDetailView.as_view(), name='agent-detail'),
    path('<int:id>/update/', AgentUpdateView.as_view(), name='agent-update'),
    path('<int:id>/delete/', AgentDeleteView.as_view(), name='agent-delete')
]