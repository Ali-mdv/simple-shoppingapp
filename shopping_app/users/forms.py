from django import forms
from .models import User, UserAddress
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from phonenumber_field.formfields import PhoneNumberField
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(attrs={'class': 'input'})
    )
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    password1 = forms.CharField(label='password', widget=forms.PasswordInput())
    password2 = forms.CharField(
        label='confirm password', widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username)

        if user:
            raise forms.ValidationError(
                'کاربری با این ایمیل قبلا ثبت نام کرده است.')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email)

        if user:
            raise forms.ValidationError(
                'کاربری با این ایمیل قبلا ثبت نام کرده است.')

        return email

    def clean(self):
        data = self.cleaned_data
        password1 = data.get('password1')
        password2 = data.get('password2')

        if not password1 == password2:
            raise forms.ValidationError('رمز عبور مطابقت ندارد')

        return data


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'آدرس ایمیل یا رمز عبور اشتباه است.\nلطفا ایمیل و رمز عبور معتبر وارد نمایید.',
    }


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(
        label="ایمیل",
        max_length=200,
    )
    phonenumber = PhoneNumberField(
        label="شماره همراه",
        region="IR",
        help_text='شماره تلفن باید در قالب «09121234567» وارد شود. حداکثر 15 رقم مجاز است.'
    )
    # cumtomize phonenumberfield error
    phonenumber.error_messages[
        'invalid'] = "یک شماره تلفن معتبر وارد کنید (به عنوان مثال «09121234567» یا «989121234567»)."

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)

        if not user.is_superuser:
            self.fields['username'].disabled = True
            # self.fields['username'].help_text = None
            self.fields['email'].disabled = True
            self.fields['phonenumber'].disabled = True
            self.fields['email'].disabled = True

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'username', 'phonenumber']


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        label="ایمیل",
        max_length=200,
        help_text='الزامی. یک آدرس ایمیل معتبر وارد کنید.'
    )
    phonenumber = PhoneNumberField(
        label="شماره همراه",
        region="IR",
        help_text='الزامی. شماره تلفن باید در قالب «09121234567» وارد شود. حداکثر 15 رقم مجاز است.'
    )
    # cumtomize phonenumberfield error
    phonenumber.error_messages[
        'invalid'] = "یک شماره تلفن معتبر وارد کنید (به عنوان مثال «09121234567» یا «989121234567»)."

    class Meta:
        model = User
        fields = ('username', 'email', 'phonenumber', 'password1', 'password2')


class UserAddressForm(forms.ModelForm):
    city = forms.CharField(
        label="شهر",
        max_length=50,
    )
    address = forms.CharField(
        label="آدرس",
        max_length=155,
        help_text='آدرس معتبر و کامل وارد نمایید.'
    )
    post_code = forms.CharField(
        label="کد پستی",
        max_length=20,
    )
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    class Meta:
        model = UserAddress
        fields = ("city", "address", "post_code", )

    def clean(self):
        if self.user.useraddress_set.count() >= 3:
            raise ValidationError("ثبت بیش از ۳ آدرس امکانپذیر نیست.")
