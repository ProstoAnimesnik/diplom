## форма создания юзера

from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import TextInput, PasswordInput, EmailInput, NumberInput, ModelForm, Form
from django.contrib.admin.widgets import FilteredSelectMultiple
from Main.models import *


class CreateUserForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        model = UserNew
        fields = ('first_name', "username", "password1", "password2", "email", "NumPhone")
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Имя'}),
            "username": TextInput(attrs={'placeholder': 'Логин'}),
            "password1": PasswordInput(attrs={'placeholder': 'Пароль'}),
            "password2": PasswordInput(attrs={'placeholder': 'Повтор пароля'}),
            "email": EmailInput(attrs={'placeholder': 'Почта'}),
            "NumPhone": NumberInput(attrs={'placeholder': 'Номер телефона'})
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Ваше имя ?"
        self.fields["username"].label = "Логин"
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Повторите пароль"
        self.fields["email"].label = "Ваша почта"
        self.fields["NumPhone"].label = "Ваш номер телефона"


## форма логина
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Логин', 'type': 'text', "autocomplete": "username"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Пароль', 'type': 'password'}))

class AddGoodsForm(ModelForm):
    class Meta:
        model = Goods
        fields = ("NameGoods","Price","GoodsStock","GoodsPhoto","GoodsType")
 #        widgets = {
 #              "NameGoods": forms.CharField(attrs={'placeholder': 'Имя товара'}),
 #              "Price": forms.DecimalField(attrs={'placeholder': 'Цена товара'}),
 #              "GoodsStock": forms.DecimalField(attrs={'placeholder': 'Кол-во товара'}),
 #              "GoodsPhoto": forms.ImageField(attrs={'placeholder': 'Изображение товара'}),
 #              "GoodsType": forms.CharField(max_length=300, choices=Goods, attrs={'placeholder': 'Изображение товара'}),
 # }

class AddGoodsInZakazForm(Form):
    equip_id = forms.ModelMultipleChoiceField(queryset=Zakaz.objects.all(), required=True, widget=FilteredSelectMultiple("zakaz_status", is_stacked=False))

class Media:
    css = {
        'all': ('/admin/css/widgets.css',),
    }
    # jsi18n is required by the widget
    js = ('/admin/jsi18n/',)