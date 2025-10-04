from django import forms
from .models import SCOPE_CHOICES, MODE_CHOICES

class ProjectForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    phone = forms.CharField(max_length=32, required=False)
    type  = forms.ChoiceField(choices=[("web","وب"),("mobile","موبایل"),("both","هر دو")])
    scope = forms.MultipleChoiceField(choices=SCOPE_CHOICES, required=False, widget=forms.CheckboxSelectMultiple)
    deadline = forms.DateField(required=False, widget=forms.DateInput(attrs={"type":"date"}))
    budget = forms.CharField(max_length=60, required=False)
    message = forms.CharField(widget=forms.Textarea, required=False)
    nda = forms.BooleanField(required=False)

    # honeypot
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean(self):
        data = super().clean()
        if data.get("website"):  # بات‌ها معمولا اینو پر می‌کنن
            raise forms.ValidationError("Invalid submission.")
        return data

class HireForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    role = forms.CharField(max_length=120, required=False)
    mode = forms.ChoiceField(choices=MODE_CHOICES, required=False)
    skills = forms.CharField(max_length=255, required=False)
    message = forms.CharField(widget=forms.Textarea, required=False)

    website = forms.CharField(required=False, widget=forms.HiddenInput)  # honeypot

    def clean(self):
        data = super().clean()
        if data.get("website"):
            raise forms.ValidationError("Invalid submission.")
        return data
