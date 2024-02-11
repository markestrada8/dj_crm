from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganizerAndLoginRequredMixin
from django.http import HttpResponse
from django.views import generic
from .models import Lead, Agent, Category
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm

class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')

class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'


class LeadListView(LoginRequiredMixin, generic.ListView):
    # CONTEXT AS IMPLICIT ARGUMENT 'object_list', OVERLOAD AS context_object_name
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        # GET USER
        user = self.request.user

        # FILTER BY ORGANIZATION
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization, agent__isnull=False)
            # FILTER BY AGENT
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, *kwargs):
        context = super(LeadListView, self).get_context_data(*kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=True)
            context.update({
                'unassigned_leads': queryset
            })
        return context


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/lead_detail.html'
    queryset = Lead.objects.all()
    context_object_name = 'lead'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        # GET USER
        user = self.request.user

        # FILTER BY ORGANIZATION
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # FILTER BY AGENT
            queryset = queryset.filter(agent__user=user)
        return queryset



class LeadCreateView(OrganizerAndLoginRequredMixin, generic.CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        send_mail(
            subject="A lead has been created",
            message="Go to management page to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)

class LeadUpdateView(OrganizerAndLoginRequredMixin, generic.UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm
    pk_url_kwarg = 'id'

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse('leads:lead-list')

class LeadDeleteView(OrganizerAndLoginRequredMixin, generic.DeleteView):
    template_name = 'leads/lead_delete.html'
    queryset = Lead.objects.all()
    pk_url_kwarg = 'id'

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse('leads:lead-list')


class AssignAgentView(OrganizerAndLoginRequredMixin, generic.FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs['id'])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/category_list.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)

        context.update({
            'unassigned_lead_count': queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)
        return queryset

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/category_detail.html'
    context_object_name = 'category'
    pk_url_kwarg = 'id'

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)
    #     # MODEL RELATED NAME
    #     leads = self.get_object().leads.all()

    #     context.update({
    #         'leads': leads
    #     })
    #     return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm
    pk_url_kwarg = 'id'

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"id": self.get_object().id})

    # def form_valid(self, form):
    #     lead_before_update = self.get_object()
    #     instance = form.save(commit=False)
    #     converted_category = Category.objects.get(name="Converted")
    #     if form.cleaned_data["category"] == converted_category:
    #         # update the date at which this lead was converted
    #         if lead_before_update.category != converted_category:
    #             # this lead has now been converted
    #             instance.converted_date = datetime.datetime.now()
    #     instance.save()
    #     return super(LeadCategoryUpdateView, self).form_valid(form)








################################################################
# VIEW HANDLER FUNCTIONS (CONTROLLERS)

# def landing_page(request):
#     return render(request, 'landing.html')


# def lead_list(request):
#     leads = Lead.objects.all()
#     context = {
#         'leads': leads
#     }

#     return render(request, 'leads/lead_list.html', context)

# def lead_detail(request, id):
#     # print('ID: ', id)
#     lead = Lead.objects.get(id=id)
#     context = {
#         'lead': lead
#     }

#     return render(request, 'leads/lead_detail.html', context)

# def lead_create(request):
#     if request.method == 'POST':
#         form_data = LeadModelForm(request.POST)
#         if form_data.is_valid():
#             form_data.save()
#             return redirect('/leads')
#     else:
#         form_data = LeadModelForm()

#     context = {
#         'form': form_data
#     }

#     return render(request, 'leads/lead_create.html', context)

# def lead_update(request, id):
#     lead_to_update = Lead.objects.get(id=id)
#     # NEEDED LINE?
#     form_data = LeadModelForm(instance=lead_to_update)
#     #
#     if request.method == 'POST':
#         form_data = LeadModelForm(request.POST, instance=lead_to_update)
#         if form_data.is_valid():
#             form_data.save()

#             return redirect('/leads')

#     context = {
#         'form': form_data,
#         'lead': lead_to_update
#     }

#     return render(request, 'leads/lead_update.html', context)

# def lead_delete(request, id):
#     lead_to_delete = Lead.objects.get(id=id)

#     lead_to_delete.delete()
#     return redirect('/leads')

################################################################

# BASIC FORM VERSION
# def lead_create(request):
#     if request.method == 'POST':
#         form = LeadForm(request.POST)
#         if form.is_valid():

#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.first()
#             Lead.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 age=age,
#                 agent=agent
#             )

#             return redirect('/leads')
#     else:
#         form = LeadForm()

#     context = {
#         'form': form
#     }

#     return render(request, 'leads/lead_create.html', context)

################################################################
# def lead_update(request, id):
#     lead_to_update = Lead.objects.get(id=id)
#     if request.method == 'POST':
#         form_data = LeadForm(request.POST)
#         if form_data.is_valid():
#             lead_to_update.first_name = form_data.cleaned_data['first_name']
#             lead_to_update.last_name = form_data.cleaned_data['last_name']
#             lead_to_update.age = form_data.cleaned_data['age']
#             lead_to_update.save()

#             return redirect('/leads')
#     else:
#         form_data = LeadForm()

#     context = {
#         'form': form_data,
#         'lead': lead_to_update
#     }

#     return render(request, 'leads/lead_update.html', context)