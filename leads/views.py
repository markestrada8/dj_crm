from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm


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
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    else:
        form = LeadModelForm()

    context = {
        'form': form
    }

    return render(request, 'leads/lead_create.html', context)

def lead_update(request, id):
    lead_to_update = Lead.objects.get(id=id)
    context = {
        'lead': lead_to_update
    }

    return render(request, 'leads/lead_update.html', context)
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

