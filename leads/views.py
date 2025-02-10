from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from .models import Lead, Category
from django.views import generic
from .forms import LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryForm, CategoryModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorAndLoginRequiredMixin
from django.conf import settings

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

    # Assigned Leads to a specific agent
    def get_queryset(self):
        user = self.request.user
        # filter to show all leads the organisation have
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile, agent__isnull = False)
        else:
            # filter to first access the agents org and 
            # then check a specific leads assigned to that agent
            queryset = Lead.objects.filter(organisation = user.agent.organisation, agent__isnull = False)
            queryset = Lead.objects.filter(agent__user = user)
        return queryset
    
    # Unassigned Leads
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile, agent__isnull = True)
            context.update({
                'unassigned_leads': queryset
            })
        return context


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
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        if lead.agent and lead.agent.user and lead.agent.user.email:
            send_mail(
                subject = "You've been assigned to the new lead.",
                message = "Visit the site to know more",
                from_email =settings.DEFAULT_FROM_EMAIL,
                recipient_list = [lead.agent.user.email]
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

class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        if lead.agent and lead.agent.user and lead.agent.user.email:
            send_mail(
                subject = "You've been assigned to the new lead.",
                message = "Visit the site to know more",
                from_email =settings.DEFAULT_FROM_EMAIL,
                recipient_list = [lead.agent.user.email]
            )
        return super(AssignAgentView, self).form_valid(form)  
    

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/category_list.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        # unassgined_leads count
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation)
        
        context.update({
                "fresh_lead_count": queryset.filter(category__isnull=True).count(),
                
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(organisation = user.userprofile)
        else:
            queryset = Category.objects.filter(organisation = user.agent.organisation)
        return queryset
    

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name= 'leads/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        leads = self.get_object().leads.all()

        context.update({
                "leads": leads
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(organisation = user.userprofile)
        else:
            queryset = Category.objects.filter(organisation = user.agent.organisation)
        return queryset
    
class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_category_update.html'
    form_class = LeadCategoryForm

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})
    
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

class CategoryCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = 'leads/category_create.html'
    context_object_name = 'category'
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")
    
    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)
    
class CategoryUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/category_update.html'
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")
         
    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(organisation = user.userprofile)
        else:
            queryset = Category.objects.filter(organisation = user.agent.organisation)
        return queryset
    
class CategoryDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/category_delete.html'

    def get_success_url(self):
        return reverse("leads:category-list")
    
    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(organisation = user.userprofile)
        else:
            queryset = Category.objects.filter(organisation = user.agent.organisation)
        return queryset
    
