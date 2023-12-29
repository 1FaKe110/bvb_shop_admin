import os

import flask
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, redirect, url_for, abort, session, Blueprint
from flask_cors import CORS
from loguru import logger
from munch import DefaultMunch

from background import Tasks
from repository.categories import Categories, categories_page
from repository.items import Items, items_page
from repository.login import Login, login_page
from repository.logout import Logout, logout_page
from repository.orders import Orders, orders_page
from repository.orders.order_detailed import OrdersDetailed, orders_detailed_page
from repository.products import Products, products_page
from repository.users import Users, users_page

Tasks.update_dollar_course()
as_class = DefaultMunch.fromDict
app = Flask(__name__)
app.secret_key = os.getenv('secret_key')  # секретный ключ для сессий
CORS(app)

# Создание Blueprint для страницы "admin"
admin_page = Blueprint('admin_page', __name__)
category_handler = Categories()
login_handler = Login()
logout_handler = Logout()
product_handler = Products()
orders_handler = Orders()
orders_detailed_handler = OrdersDetailed()
users_handler = Users()
items_handler = Items()


@admin_page.route('/')
def index():
    logger.debug(session)
    if 'username' not in session:
        return redirect(url_for('admin_page.login'))
    return redirect(url_for('admin_page.categories'))


@admin_page.route('/login', methods=['GET', 'POST'])
def login():
    match request.method:
        case 'GET':
            return login_handler.get(session)
        case 'POST':
            return login_handler.post(session)
        case _:
            return flask.Response(status=405)


@admin_page.route('/logout')
def logout():
    """Выход из личного кабинета"""
    match request.method:
        case 'GET':
            return logout_handler.get(session)
        case _:
            return flask.Response(status=405)


#### КАТЕГОРИИ ####

@logger.catch
@admin_page.route('/categories', methods=['GET', 'POST'])
def categories():
    match request.method:
        case 'GET':
            return category_handler.get(session)
        case 'POST':
            return category_handler.post(session)
        case _:
            return flask.Response(status=405)


@admin_page.route('/categories/<category_id>/delete', methods=['DELETE'])
def categories_delete(category_id):
    """Delete category from database"""
    match request.method:
        case 'DELETE':
            return category_handler.delete(session, category_id)
        case _:
            return flask.Response(status=405)


#### Продукты ####

@logger.catch
@admin_page.route('/products', methods=['GET', 'POST'])
def products():
    match request.method:
        case 'GET':
            return product_handler.get(session)
        case 'POST':
            return product_handler.post(session)
        case _:
            return flask.Response(status=405)


@admin_page.route('/products/<product_id>/delete', methods=['DELETE'])
def products_delete(product_id):
    match request.method:
        case 'GET':
            return product_handler.delete(session, product_id)
        case _:
            return flask.Response(status=405)


### ЗАКАЗЫ ###

@logger.catch
@admin_page.route('/orders', methods=['GET', 'POST'])
def orders():
    match request.method:
        case 'GET':
            return orders_handler.get(session)
        case _:
            return flask.Response(status=405)


### ЗАКАЗЫ ДЕТАЛЬНО ###

@logger.catch
@admin_page.route('/order/<int:order_id>', methods=['GET'])
def order(order_id):
    match request.method:
        case 'GET':
            return orders_detailed_handler.get(session, order_id)
        case _:
            return flask.Response(status=405)


@admin_page.route('/order/<order_id>/delete', methods=['DELETE'])
def order_delete(order_id):
    """Delete order from database"""
    match request.method:
        case 'GET':
            return orders_detailed_handler.get(session, order_id)
        case _:
            return flask.Response(status=405)


@admin_page.route('/order/<order_id>/update', methods=['POST'])
def order_update(order_id):
    """update order in database"""
    match request.method:
        case 'POST':
            return orders_detailed_handler.update(session, order_id)
        case _:
            return flask.Response(status=405)


@logger.catch
@admin_page.route('/order/<order_id>/delete/<item_id>', methods=['DELETE'])
def order_delete_item(order_id, item_id):
    """Delete order from database"""
    match request.method:
        case 'DELETE':
            return orders_detailed_handler.delete(session, order_id, item_id)
        case _:
            return flask.Response(status=405)


### ПОЛЬЗОВАТЕЛИ ###

@logger.catch
@admin_page.route('/users', methods=['GET', 'POST'])
def users():
    match request.method:
        case 'GET':
            return users_handler.get(session)
        case 'POST':
            return users_handler.post(session)
        case _:
            return flask.Response(status=405)


@admin_page.route('/users/delete/<user_id>', methods=['DELETE'])
def users_delete(user_id):
    """Delete user from database"""
    match request.method:
        case 'POST':
            return users_handler.delete(session, user_id)
        case _:
            return flask.Response(status=405)


### Добавление новых данных ####

@logger.catch
@admin_page.route('/add_items', methods=['GET', 'POST'])
def add_items():
    match request.method:
        case 'GET':
            return items_handler.get(session)
        case 'POST':
            return items_handler.post(session)
        case _:
            return flask.Response(status=405)


@admin_page.errorhandler(404)
def page_not_found(error):
    """Страница 'страница не найдена'"""
    return render_template('404.html'), 404


@admin_page.errorhandler(500)
def error_page(error):
    """Страница 'страница не найдена'"""
    return render_template('500.html'), 500


@admin_page.route('/error_500')
def nonexistent_page():
    """Пример эндпоинта, которого нет"""
    # Генерируем ошибку 404 "Страница не найдена"
    return abort(500)


def main():
    scheduler = BackgroundScheduler()
    scheduler.add_job(Tasks.update_dollar_course, 'interval', hours=24)
    scheduler.start()
    app.register_blueprint(admin_page, url_prefix='/')
    app.register_blueprint(login_page, url_prefix='/login')
    app.register_blueprint(logout_page, url_prefix='/logout')
    app.register_blueprint(categories_page, url_prefix='/categories')
    app.register_blueprint(products_page, url_prefix='/products')
    app.register_blueprint(orders_page, url_prefix='/orders')
    app.register_blueprint(orders_detailed_page, url_prefix='/order')
    app.register_blueprint(users_page, url_prefix='/users')
    app.register_blueprint(items_page, url_prefix='/add_items')
    app.run(host='0.0.0.0', port=1112, debug=True)


if __name__ == '__main__':
    main()
