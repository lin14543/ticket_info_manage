from django import forms

class UserForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)
    confirmpassword = forms.CharField(max_length=50)