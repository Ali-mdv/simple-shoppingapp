from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
	username = forms.CharField(
		label='نام کاربری',
		widget=forms.TextInput(attrs={'class':'input'})
		)
	password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput())
	email = forms.EmailField(widget=forms.EmailInput())
	password1 = forms.CharField(label='password',widget=forms.PasswordInput())
	password2 = forms.CharField(label='confirm password',widget=forms.PasswordInput())


	def clean_username(self):
		username = self.cleaned_data.get('username')
		user = User.objects.filter(username=username)

		if user:
			raise forms.ValidationError('کاربری با این ایمیل قبلا ثبت نام کرده است.')

		return username

	def clean_email(self):
		email = self.cleaned_data.get('email')
		user = User.objects.filter(email=email)

		if user:
			raise forms.ValidationError('کاربری با این ایمیل قبلا ثبت نام کرده است.')

		return email


	def clean(self):
		data = self.cleaned_data
		password1 = data.get('password1')
		password2 = data.get('password2')

		if not password1 == password2:
			raise forms.ValidationError('رمز عبور مطابقت ندارد')

		return data



class ProfileForm(forms.ModelForm):
	def __init__(self,*args,**kwargs):
		user = kwargs.pop('user')
		super(ProfileForm,self).__init__(*args,**kwargs)

		if not user.is_superuser:
			self.fields['username'].disabled = True
			# self.fields['username'].help_text = None
			self.fields['email'].disabled = True
			self.fields['phonenumber'].disabled = True
			self.fields['email'].disabled = True

	class Meta:
		model = User
		fields = ['first_name','last_name','email','username','phonenumber']




class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email','phonenumber', 'password1', 'password2')