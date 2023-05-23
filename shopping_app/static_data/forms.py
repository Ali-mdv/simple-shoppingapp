from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import SiteInfo


class SiteInfoForm(forms.ModelForm):
    phonenumber = PhoneNumberField(
        label="تلفن همراه",
        region="IR",
        help_text='الزامی. شماره تلفن باید در قالب «09121234567» وارد شود. حداکثر 15 رقم مجاز است.'
    )
    landline = PhoneNumberField(
        label="تلفن ثابت",
        region="IR",
        help_text='الزامی. شماره تلفن باید در قالب «02112345678» وارد شود. حداکثر 15 رقم مجاز است.',
        required=False
    )
    # cumtomize phonenumberfield error
    phonenumber.error_messages[
        'invalid'] = "یک شماره تلفن معتبر وارد کنید (به عنوان مثال «09121234567» یا «989121234567»)."

    landline.error_messages[
        'invalid'] = "یک شماره تلفن معتبر وارد کنید (به عنوان مثال «02112345678» یا «982112345678»)."

    class Meta:
        model = SiteInfo
        fields = "__all__"
