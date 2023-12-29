from repository.sql.Orders import Orders
from repository.sql.Categories import Categories
from repository.sql.Users import Users, UsersAdmin
from repository.sql.Products import Products
from repository.sql.Dollar import Dollar


class DbQueries:

    categories = Categories
    users = Users
    adminUsers = UsersAdmin
    products = Products
    dollar = Dollar
    orders = Orders
