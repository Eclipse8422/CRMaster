from typing import Any
from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, reverse
from .models import Lead
from django.views import generic
from .forms import LeadModelForm, CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorAndLoginRequiredMixin

class RegisterView(generic.CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

class HomePageView(generic.TemplateView):
    template_name = 'homepage.html'


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        # filter to show all leads the organisation have
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile)
        else:
            # filter to first access the agents org and 
            # then check a specific leads assigned to that agent
            queryset = Lead.objects.filter(organisation = user.agent.organisation)
            queryset = Lead.objects.filter(agent__user = user)
        return queryset

class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/lead_detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        # filter to show all leads the organisation have
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile)
        else:
            # filter to first access the agents org and 
            # then check a specific leads assigned to that agent
            queryset = Lead.objects.filter(organisation = user.agent.organisation)
            queryset = Lead.objects.filter(agent__user = user)
        return queryset
    

class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        send_mail(
            subject = "A new lead has been created.",
            message = "Visit the site to know more",
            from_email = "test@test.com",
            recipient_list = ["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)                                                         

class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def get_queryset(self):
        user = self.request.user
        # filter to show all leads the organisation have      
        return Lead.objects.filter(organisation = user.userprofile)
        

class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/lead_delete.html'

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def get_queryset(self):
        user = self.request.user
        # filter to show all leads the organisation have      
        return Lead.objects.filter(organisation = user.userprofile)
