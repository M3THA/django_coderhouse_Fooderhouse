from django import forms

class MessagesForm(forms.Form):
    title = forms.CharField(max_length=40)
    reciever = forms.CharField(max_length=60)
    content = forms.CharField(max_length=1000)
    