from django import forms

class BromoCodeForm(forms.Form):
    code = forms.CharField(max_length=20)

    def clean(self):
        cleaned_data = super(BromoCodeForm, self).clean()
        return cleaned_data