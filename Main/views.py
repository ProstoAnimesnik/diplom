import datetime

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalLoginView
from django.contrib.auth import login, logout
from django.http import *
from django.shortcuts import redirect , render
from django.template.smartif import key
from django.urls import reverse_lazy
from django.utils.timezone import make_aware
from django.views.generic import CreateView, ListView, TemplateView, FormView
from django.views.generic.base import View
from django.db.models import *
from Main.forms import *
from Main.models import *
from Main.utils import DataMixin
from django.utils.encoding import force_text

class Index(DataMixin, ListView):
    template_name = "index.html"
    queryset = Goods.objects.all()
    context_object_name = "Cab"

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


class SearchAllLessonAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = '_modal_Shop.html'

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('gg')  ## запрос строки

        if query:
            less = Goods.objects.all()
            return Response({'lesson': less})

        for key in request.GET.keys():
            if key.startswith('btn_'):
                btn_pk = key[4:]
                tovar = Goods.objects.get(id=btn_pk)  # ищем объект по id  нажатой кнопки
                cou = 0
                for i in Cart.objects.filter(cart_user_id=request.user):
                    if tovar == i.cart_goods_id:
                        towa = Cart.objects.get(cart_user_id=request.user, cart_goods_id=tovar)
                        towa.cart_goods_count += 1
                        towa.save()
                        cou = 1
                if cou == 0:
                    item_to_cart = Cart(cart_user_id=request.user, cart_goods_id=tovar,
                                        cart_goods_count=1)  # создаем запись
                    item_to_cart.save()  # добавляем
        return HttpResponseRedirect('/test_1')


# class About(DataMixin, FormView):
#     template_name = "About.html"
#     form_class = AddGoodsInZakazForm
#
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_content(title="About")
#         return dict(list(context.items()) + list(c_def.items()))


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
            if key.startswith('btn_'):  # делаем только по нажатию кнопки
                for i in goods:  # цикл по товарам пользователя
                    print("Request User - ", request.user)
                    cart_to_zakaz = Zakaz(zakaz_user_id=request.user,
                                          zakaz_goods_id=i.cart_goods_id,
                                          zakaz_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                          zakaz_goods_count=i.cart_goods_count)  # Создаем объект в бд
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

class view_orders(DataMixin, ListView ):
    template_name = "view_orders.html"
    context_object_name = "orders"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        userss = UserNew.objects.all()  # - список всех пользователей
        # поиск по всем заказам. Сначала фильтруем все записи по массиву с пользователями.
        # Крч ищем, какие пользователи заказали.
        # Потом, через values() вытаскиваем только время заказа и юзернейм чела.
        # distinct() отвечает за отсутствие дубликатов

        choices = dict(Zakaz._meta.get_field('zakaz_status').flatchoices)
        whens = [When(zakaz_status=k, then=Value(v)) for k, v in choices.items()]
        users_with_time = (
            Zakaz.objects.filter(zakaz_user_id__in=userss)
                .annotate(get_zakaz_status_display=Case(*whens, output_field=CharField())).order_by('zakaz_status')
                .values(
                'zakaz_time',
                'zakaz_user_id__username',
                'zakaz_user_id__NumPhone',
                "zakaz_status",
                "get_zakaz_status_display"
            ).distinct()
        )
        c_def = self.get_user_content(title="Добавить товар",
                                      users_zakaz=users_with_time,
                                      )
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Zakaz.objects.all()

    def post(self, request):
        if request.method == 'POST':
            if request.POST.get("submit"):
                request_content = request.POST.get('submit').split("_")
                filter_content = Zakaz.objects.filter(zakaz_time=request_content[0], zakaz_user_id__username=request_content[1])
                for i in filter_content:
                    i.zakaz_status = "3"
                    i.save()

            elif request.POST.get("decline"):
                request_content = request.POST.get('decline').split("_")
                filter_content = Zakaz.objects.filter(zakaz_time=request_content[0], zakaz_user_id__username=request_content[1])
                for i in filter_content:
                    i.zakaz_status = "2"
                    i.save()

            elif request.POST.get("delete"):
                request_content = request.POST.get('delete').split("_")
                filter_content =Zakaz.objects.filter(zakaz_goods_id=request_content[0], zakaz_user_id__username=request_content[1], zakaz_time=request_content[2])
                for i in filter_content:
                    i.delete()

            elif request.POST.get("return"):
                request_content = request.POST.get('return').split("_")
                filter_content = Zakaz.objects.filter(zakaz_time=request_content[0],
                                                      zakaz_user_id__username=request_content[1])
                for i in filter_content:
                    i.zakaz_status = "1"
                    i.save()
        return HttpResponseRedirect('/view_orders')





def logout_user(request):
    logout(request)
    return redirect('home')

# ToDo шоб задеплоить на кероку
# git add .
# git commit -am "Название комита"
# git push heroku master
# gi
