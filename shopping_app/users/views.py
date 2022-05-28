from django.shortcuts import render, redirect
from django.contrib.auth import authenticate , login, get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .models import User
from .forms import ProfileForm, SignupForm
from django.urls import reverse_lazy, reverse

from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
# Create your views here.



# def register(request):
# 	User = get_user_model()

# 	form_class = RegisterForm(request.POST or None)

# 	if form_class.is_valid():
# 		username = form_class.cleaned_data.get('username')
# 		email = form_class.cleaned_data.get('email')
# 		password = form_class.cleaned_data.get('password1')
# 		print(form_class.cleaned_data)
# 		user = User.objects.create_user(username=username,email=email,password=password)

# 	context = {
# 		'form' : form_class,
# 	}

# 	return render(request, 'users/register.html',context)

#===========================================================================================

class Login(LoginView):
	def get_success_url(self):
		user = self.request.user
		if user.is_authenticated:
			return reverse('product:home')
		else:
			return reverse('login')


def navbar_login(request, *args, **kwargs):
	form_class = AuthenticationForm(request,request.POST or None)
	
	if form_class.is_valid():
		print(form_class.cleaned_data)
		username = form_class.cleaned_data.get('username')
		password = form_class.cleaned_data.get('password')
		user = authenticate(request,username=username,password=password)

		if not user is None:
			login(request,user)
			form_class = AuthenticationForm()
			
	context = {
		'form':form_class,
	}

	return render(request, 'product/navbar.html',context)




class Profile(LoginRequiredMixin,UpdateView):
    form_class = ProfileForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)


    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({'user':self.request.user})
        return kwargs






def signup(request):
    if request.user.is_authenticated:
        return redirect('product:home')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})




def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('<p>Thank you for your email confirmation. Now you can login your account.</p>\n<p><a href="/login">login</a></p>')
    else:
        return HttpResponse('Activation link is invalid!')