from django import forms
from Register_Login.models import RegisterationModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Email exists")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())




class CompleteProfile(forms.ModelForm):
    class Meta:
        model = RegisterationModel
        fields = ('FirstName', 'LastName', 'Age', 'PhoneNumber', 'ProfilePic',)
