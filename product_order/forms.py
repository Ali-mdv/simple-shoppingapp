from django import forms



class NewOrderFrom(forms.Form):
    product_id = forms.IntegerField(
        widget=forms.HiddenInput(),
    )
    count = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class':'span6'}),
        initial=1
    )