from django import forms
from product.models import Color


class NewOrderFrom(forms.Form):
    product_id = forms.IntegerField(
        widget=forms.HiddenInput(),
    )
    count = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=1
    )
    color = forms.ChoiceField(
        label="رنگ",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super(NewOrderFrom, self).__init__(*args, **kwargs)
        select_option = [(color.id, color.title)
                         for color in Color.objects.all()]
        self.fields['color'].choices = [
            ('', " --- لطفا انتخاب کنید --- ")] + select_option
