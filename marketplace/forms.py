from django import forms


class Auth(forms.Form):
    key = forms.CharField()
    secret = forms.CharField()
