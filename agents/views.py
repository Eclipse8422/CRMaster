from django.core.mail import send_mail
from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentLeadForm
from .mixins import OrganisorAndLoginRequiredMixin
import random


class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = 'agents/agent_list.html'
    context_object_name = 'agents'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)
    
class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentLeadForm

    def get_success_url(self):
        return reverse('agents:agent-list')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(str("random.randint(1,10000000)"))
        user.save()
        Agent.objects.create(
            user = user,
            organisation = self.request.user.userprofile
        )
        send_mail(
            subject="Agent invite",
            message="You were added as an agent on CRMaster. Please Login and start working!",
            from_email="admin@test.com",
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)
    
class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agent_detail.html'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)
    
    def get_success_url(self):
        return reverse('agents:agent-list')
    

class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentLeadForm
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)
    
    def get_success_url(self):
        return reverse('agents:agent-list')

class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent_delete.html'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)
    
    def get_success_url(self):
        return reverse('agents:agent-list')

     