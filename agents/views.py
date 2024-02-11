from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganizerAndLoginRequredMixin

class AgentListView(OrganizerAndLoginRequredMixin, generic.ListView):
    template_name = 'agents/agent_list.html'
    context_object_name = 'agents'

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization = organization)


class AgentDetailView(OrganizerAndLoginRequredMixin, generic.DetailView):
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization = organization)

class AgentCreateView(OrganizerAndLoginRequredMixin, generic.CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent-list')

    def form_valid(self, form):
        agent = form.save(commit=False)
        agent.organization = self.request.user.userprofile
        agent.save()
        return super(AgentCreateView, self).form_valid(form)

class AgentUpdateView(OrganizerAndLoginRequredMixin, generic.UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('agents:agent-list')

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization = organization)

class AgentDeleteView(OrganizerAndLoginRequredMixin, generic.DeleteView):
    template_name = 'agents/agent_delete.html'
    queryset = Agent.objects.all()
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('agents:agent-list')

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization = organization)
