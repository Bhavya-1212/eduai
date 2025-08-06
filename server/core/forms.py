from django import forms

class PromptForm(forms.Form):
    prompt = forms.CharField(label='Enter your prompt', max_length=200)

class ChatForm(forms.Form):
    message = forms.CharField(label='Ask something', max_length=200)
