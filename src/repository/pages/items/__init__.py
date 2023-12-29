import flask
from flask import redirect, url_for, render_template, request, Blueprint
from loguru import logger
from database import db
from repository.sql import DbQueries
from munch import DefaultMunch

as_class = DefaultMunch.fromDict
items_page = Blueprint('items_page', __name__)


class Items:
    def __init__(self):
        pass

    @staticmethod
    def get_dollar_price():
        dollar = db.exec(
            DbQueries.dollar.Select.get(),
            'fetchone'
        )
        logger.debug(f'dollar: {dollar.price}')
        return dollar.price

    @staticmethod
    def check_login(session):
        logger.debug(session)
        if 'username' not in session:
            return redirect(url_for('admin_page.login'))

    def get(self, session):
        self.check_login(session)
        categories_list = db.exec(
            DbQueries.categories.Select.all_by_id(),
            'fetchall'
        )
        return render_template('add_items.html',
                               categories=categories_list,
                               dollar=self.get_dollar_price())

    def post(self, session):
        self.check_login(session)
        form = as_class(request.form.to_dict())
        logger.debug(form)

        if 'productName' in form:
            return self.add_new_product(session, form)
        elif 'categoryName' in form:
            return self.add_new_category(session, form)
        else:
            return flask.Response(status=404)

    def add_new_product(self, session, form):
        logger.debug('Добавляем новый продукт')
        name = form.productName
        category_id = int(form.productCategory)
        brand = form.productBrand
        description = form.productDescription
        by_price = float(form.productByPrice)
        if form.productDollar:
            in_dollar = True
            sell_price = round(by_price * self.get_dollar_price() * 1.5, 0)
        else:
            in_dollar = False
            sell_price = round(by_price * 1.5, 0)

        amount = form.productAmount
        image = form.productImagePath

        db.exec(
            DbQueries.products.Insert.new_product(
                name, by_price, sell_price, amount, brand, in_dollar, category_id, description, image
            )
        )

        return self.get(session)

    def add_new_category(self, session, form):
        logger.debug('Добавляем новую категорию')
        db.exec(
            DbQueries.categories.Insert.new_category(form)
        )
        return self.get(session)
