import json

import flask
from flask import redirect, url_for, render_template, request, Blueprint
from loguru import logger
from database import db
from repository.sql import DbQueries
from munch import DefaultMunch

as_class = DefaultMunch.fromDict
products_page = Blueprint('products_page', __name__)


class Products:
    def __init__(self):
        pass

    @staticmethod
    def check_login(session):
        logger.debug(session)
        if 'username' not in session:
            return redirect(url_for('admin_page.login'))

    def get(self, session):
        self.check_login(session)
        dollar = db.exec(
            DbQueries.dollar.Select.get(),
            'fetchone'
        )
        products_list = db.exec(
            DbQueries.products.Select.all_by_name(),
            'fetchall'
        )
        categories_list = db.exec(
            DbQueries.categories.Select.all_by_id(),
            'fetchall'
        )
        return render_template('products.html',
                               categories=categories_list,
                               products=products_list,
                               dollar=dollar)

    def post(self, session):
        self.check_login(session)
        form = as_class(request.form.to_dict())
        logger.debug('Меняем что-то в продуктах')
        logger.debug(json.dumps(form, indent=2, ensure_ascii=False))
        db.exec(DbQueries.products.Update.by_id(form))
        self.get(session)



    def delete(self, session, category_id):
        self.check_login(session)

        logger.debug(f"Удаляю категорию с id: {category_id}")
        try:
            db.exec(
                DbQueries.categories.Delete.by_id(category_id)
            )
            return flask.Response(status=200)
        except Exception as ex_:
            logger.error(ex_)
            return flask.Response(status=500)
