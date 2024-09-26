from django import forms
from .models import Lead, Agent
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'first_name','last_name', 'age', 'email','agent','description','phone_number',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 1, 'cols': 30}),  # Adjust rows and cols as needed
        }

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username'
        ]
        
class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organisation = request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents

class LeadCategoryForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'category',
        ]