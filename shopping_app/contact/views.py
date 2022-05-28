from django.shortcuts import render
from .forms import ContactForm
from .models import ContactUs
# Create your views here.


def contact_us(request):
    contact_form = ContactForm(request.POST or None)

    if contact_form.is_valid():
        name = contact_form.cleaned_data.get('name_input')
        email = contact_form.cleaned_data.get('email_input')
        subject = contact_form.cleaned_data.get('subject_input')
        text = contact_form.cleaned_data.get('text_input')

        ContactUs.objects.create(name=name,email=email,subject=subject,text=text)
        contact_form = ContactForm()

    context = {
        'contact_form':contact_form
    }

    return render(request,'product/contact.html', context)