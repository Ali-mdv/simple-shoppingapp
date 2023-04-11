from django import forms
from .models import Comment, Product


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if len(category) != 2:
            raise forms.ValidationError(
                'انتخاب دو دسته بندی (یک دسته بندی از نوع مدل و دیگری از نوع بافت) الزامیست.')

        model_exist = category.filter(category_type="M")
        if (not model_exist):
            raise forms.ValidationError(
                'انتخاب یک دسته بندی از نوع مدل الزامیست.')

        texture_exist = category.filter(category_type="T")
        if (not texture_exist):
            raise forms.ValidationError(
                'انتخاب یک دسته بندی از نوع بافت الزامیست.')
        return category


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
