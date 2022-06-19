## Контекстное меню (которое сверху). title - заголовок. url_name - ссылка странички. path - та же url_name,
# только с '/' для проверки, на той ли мы страничке находимся
menu = [{'title': 'Главная', 'url_name': 'home', 'path': '/'},
        {'title': 'Каталог', 'url_name': 'test_1', 'path': '/test_1'},
        # {'title': 'О нас', 'url_name': 'About', 'path': 'About'},
        {'title': 'Корзина', 'url_name': 'Cart', 'path': 'Cart'},
        {'title': 'Добавить товар', 'url_name': 'add_goods', 'path': 'add_goods'},
        {'title': 'Просмотр заказов', 'url_name': 'view_orders', 'path': 'view_orders'},
        ]


class DataMixin:
    def get_user_content(self, **kwargs):
        context = kwargs
        context['error'] = ''
        context['menu'] = menu
        return context
