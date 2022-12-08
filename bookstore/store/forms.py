from django import forms
import re
from django.contrib.auth.models import User
from .models import Customer
class RegistrationForm(forms.Form):
    username = forms.CharField(required=True,label='Tài khoản', max_length=30)
    password1 = forms.CharField(required=True,label='Mật khẩu', widget=forms.PasswordInput())
    password2 = forms.CharField(required=True,label='Nhập lại mật khẩu', widget=forms.PasswordInput())
    email = forms.EmailField(required=True,label='Email')
    cus_name = forms.CharField(required=True,label='Họ tên',max_length=50)
    cus_addr = forms.CharField(required=True,label='Địa chỉ',max_length=50)
    cus_phone = forms.CharField(required=True,label='Số điện thoại',max_length=12)

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2 and password1:
                return password2
        raise forms.ValidationError("Mật khẩu không hợp lệ")

    def clean_username(self):
        username = self.cleaned_data['username']
        if re.search(r'!@#$%^&*()_+=-', username):
            raise forms.ValidationError("Tên tài khoản có kí tự đặc biệt")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Tài khoản đã tồn tại")
    
    def save(self):
        User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password1'])
        cus_link = Customer.object.create(cus_name=cus_name, cus_addr=cus_addr, cus_phone=cus_phone)