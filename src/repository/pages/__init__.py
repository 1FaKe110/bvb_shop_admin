import repository.pages.login
import repository.pages.logout
import repository.pages.categories
import repository.pages.products
import repository.pages.orders
import repository.pages.orders.order_detailed
import repository.pages.users
import repository.pages.items


class PageInstance:

    def __init__(self, handler, page):
        self.handler = handler
        self.page = page


class Pages:

    def __init__(self):
        self.login = PageInstance(
            repository.pages.login.Login(),
            repository.pages.login.login_page,
        )
        self.logout = PageInstance(
            repository.pages.logout.Logout(),
            repository.pages.logout.logout_page,
        )
        self.category = PageInstance(
            repository.pages.categories.Categories(),
            repository.pages.categories.categories_page,
        )
        self.product = PageInstance(
            repository.pages.products.Products(),
            repository.pages.products.products_page,
        )
        self.order = PageInstance(
            repository.pages.orders.Orders(),
            repository.pages.orders.orders_page,
        )
        self.order_detailed = PageInstance(
            repository.pages.orders.order_detailed.OrdersDetailed,
            repository.pages.orders.order_detailed.orders_detailed_page,
        )
        self.user = PageInstance(
            repository.pages.users.Users(),
            repository.pages.users.users_page,
        )
        self.item = PageInstance(
            repository.pages.items.Items(),
            repository.pages.items.items_page,
        )
