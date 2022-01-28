from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms

from .models import User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = '아이디'


class FindUsernameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['name'].required = True

    class Meta:
        model = User
        fields = ['name', 'email']


class UserEditForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['name'].required = True
        self.fields['username'].label = '아이디'
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['profile_img'].widget.attrs['accept'] = 'image/png, image/gif, image/jpeg'
        self.fields['password'].widget = forms.HiddenInput()

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['username', 'email', 'name', 'gender', 'profile_img']

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email).exclude(username=username)
            if qs.exists():
                raise forms.ValidationError("이미 등록된 이메일 주소입니다.")
        return email


class JoinForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['name'].required = True
        self.fields['username'].label = '아이디'
        self.fields['profile_img'].widget.attrs['accept'] = 'image/png, image/gif, image/jpeg'

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'name', 'gender', 'profile_img']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("이미 등록된 이메일 주소입니다.")
        return email
