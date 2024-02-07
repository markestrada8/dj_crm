from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm

def landing_page(request):
    return render(request, 'landing.html')


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        'leads': leads
    }

    return render(request, 'leads/lead_list.html', context)

def lead_detail(request, id):
    # print('ID: ', id)
    lead = Lead.objects.get(id=id)
    context = {
        'lead': lead
    }

    return render(request, 'leads/lead_detail.html', context)

def lead_create(request):
    if request.method == 'POST':
        form_data = LeadModelForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('/leads')
    else:
        form_data = LeadModelForm()

    context = {
        'form': form_data
    }

    return render(request, 'leads/lead_create.html', context)

def lead_update(request, id):
    lead_to_update = Lead.objects.get(id=id)
    # NEEDED LINE?
    form_data = LeadModelForm(instance=lead_to_update)
    #
    if request.method == 'POST':
        form_data = LeadModelForm(request.POST, instance=lead_to_update)
        if form_data.is_valid():
            form_data.save()

            return redirect('/leads')

    context = {
        'form': form_data,
        'lead': lead_to_update
    }

    return render(request, 'leads/lead_update.html', context)

def lead_delete(request, id):
    lead_to_delete = Lead.objects.get(id=id)

    lead_to_delete.delete()
    return redirect('/leads')

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