from django import forms



class GithubUerForm(forms.Form):

    username = forms.CharField()
    username.widget.attrs.update({'class':"form-control"})


class CredentialForm(forms.Form):

    authtoken = forms.CharField()
    authtoken.widget.attrs.update({'class':"form-control"})