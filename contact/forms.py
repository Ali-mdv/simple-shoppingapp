from django import forms
from django.core import validators


class ContactForm(forms.Form):
    name_input = forms.CharField(
        label='نام خانوادگی',
        widget=forms.TextInput(attrs={'placeholder':'نام و نام خانوادگی','class':'input-xlarge'}),
        validators = [validators.MaxLengthValidator(100,'ورودی بیش از ۱۰۰ کاراکتر امکان پذیر نیست')],
    )
    email_input = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'placeholder':'ایمیل','class':'input-xlarge'}),
        validators = [validators.MaxLengthValidator(100,'ورودی بیش از ۱۰۰ کاراکتر امکان پذیر نیست')],
    )
    subject_input = forms.CharField(
        label='موضوع',
        widget=forms.TextInput(attrs={'placeholder':'موضوع','class':'input-xlarge'}),
        validators = [validators.MaxLengthValidator(100,'ورودی بیش از ۱۰۰ کاراکتر امکان پذیر نیست')],
    )
    text_input = forms.CharField(
        label='متن',
        widget=forms.Textarea(attrs={'placeholder':'متن','class':'input-xlarge'}),
    )