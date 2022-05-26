from bootstrap_modal_forms.generic import BSModalCreateView, BSModalLoginView
from django.contrib.auth import login
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, FormView, TemplateView
from django.shortcuts import render, redirect

from Main.forms import CreateUserForm, LoginUserForm
from Main.models import *
from Main.utils import DataMixin


class Index(DataMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Главная!")
        return dict(list(context.items()) + list(c_def.items()))


##запушил не хероку а он не пушится ебаный бранч говна из-за него комит не получается
class Testing(DataMixin, ListView):
    template_name = "Shop.html"
    queryset = Goods.objects.all()
    context_object_name = "goods_t"
    print(UserNew.objects.all())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Товары")
        return dict(list(context.items()) + list(c_def.items()))


class About(DataMixin, TemplateView):
    template_name = "About.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="About")
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, BSModalCreateView):
    form_class = CreateUserForm
    template_name = 'create_user.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Регистрация!")
        return dict(list(context.items()) + list(c_def.items()))

    ## функция, вызывающаяся при валидности формы
    def form_valid(self, form):
        if not self.request.is_ajax():
            user = form.save()  ## сохранение формы
            login(self.request, user)  ## авто-логин пользователя при регистрации
        return redirect('home')


class LoginUser(DataMixin, BSModalLoginView):
    form_class = LoginUserForm
    template_name = 'login.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Авторизируйся!")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class Cart(DataMixin, TemplateView):
    template_name = "Cart.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Корзина")
        return dict(list(context.items()) + list(c_def.items()))


class add_goods(DataMixin, TemplateView):
    template_name = "add_goods.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Добавить товар")
        return dict(list(context.items()) + list(c_def.items()))


class view_orders(DataMixin, TemplateView):
    template_name = "view_orders.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Добавить товар")
        return dict(list(context.items()) + list(c_def.items()))
