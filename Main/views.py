import datetime

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalLoginView
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, FormView, TemplateView
from django.shortcuts import render, redirect

from Main.forms import *
from Main.models import *
from Main.utils import DataMixin


class Index(DataMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Главная!")
        return dict(list(context.items()) + list(c_def.items()))


class Testing(DataMixin, ListView):
    template_name = "Shop.html"
    queryset = Goods.objects.all()
    context_object_name = "goods_t"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Товары")
        return dict(list(context.items()) + list(c_def.items()))

    def get(self, request, *args, **kwargs):
        for key in request.GET.keys():
            if key.startswith('btn_'):
                btn_pk = key[4:]
                tovar = Goods.objects.get(id=btn_pk)  # ищем объект по id  нажатой кнопки

                item_to_cart = Cart(cart_user_id=request.user, cart_goods_id=tovar)  # создаем запись
                item_to_cart.save()  # добавляем

        return super(Testing, self).get(request, *args, **kwargs)


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


# fdsfasdasd

class CartView(DataMixin, ListView):
    template_name = "Cart.html"
    context_object_name = "user_cart"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Корзина")
        return dict(list(context.items()) + list(c_def.items()))

    # массив товаров с фильтрацией по пользователю, т.е. показываются все товары текущего пользователя
    def get_queryset(self):
        return Cart.objects.filter(cart_user_id=self.request.user)

    def get(self, request, *args, **kwargs):
        goods = Cart.objects.filter(cart_user_id=request.user)  # список товаров в корзине у этого пользователя
        print(goods)
        for key in request.GET.keys():
            if key.startswith('btn_'):  # делаем грязь только по нажатию кнопки
                for i in goods:  # цикл по товарам пользователя
                    print("Request User - ", request.user)
                    cart_to_zakaz = Zakaz(zakaz_user_id=request.user,
                                          zakaz_goods_id=i.cart_goods_id,
                                          zakaz_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                                          )  # Создаем объект в бд
                    cart_to_zakaz.save()  # сохраняем

            this_item_cart = Cart.objects.filter(
                cart_user_id=request.user)  # список товаров в корзине у этого пользователя
            for j in this_item_cart:
                j.delete()  # "очищаем" корзину

        return super(CartView, self).get(request, *args, **kwargs)


class add_goods(DataMixin, CreateView):
    template_name = "add_goods.html"
    form_class = AddGoodsForm
    success_url = reverse_lazy("add_goods")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_content(title="Добавить товар")
        return dict(list(context.items()) + list(c_def.items()))


class view_orders(DataMixin, ListView):
    template_name = "view_orders.html"
    context_object_name = "orders"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        userss = UserNew.objects.all()  # - список всех пользователей
        # поиск по всем заказам. Сначала фильтруем все записи по массиву с пользователями.
        # Крч ищем, какие пользователи заказали.
        # Потом, через values() вытаскиваем только время заказа и юзернейм чела.
        # distinct() отвечает за отсутствие дубликатов
        users_with_time = Zakaz.objects.filter(zakaz_user_id__in=userss).values('zakaz_time',
                                                                                'zakaz_user_id__username').distinct()
        print("users - ", users_with_time)

        c_def = self.get_user_content(title="Добавить товар",
                                      users=users_with_time
                                      )
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Zakaz.objects.all()


def logout_user(request):
    logout(request)
    return redirect('home')
