import json

import flask
from flask import redirect, url_for, render_template, Blueprint
from loguru import logger
from database import db
from repository.sql import DbQueries
from munch import DefaultMunch

as_class = DefaultMunch.fromDict
orders_page = Blueprint('orders_page', __name__)


class Orders:
    def __init__(self):
        pass

    @staticmethod
    def check_login(session):
        logger.debug(session)
        if 'username' not in session:
            return redirect(url_for('admin_page.login'))

    def get(self, session):
        # переделать, чтобы быстрее грузилось, убрать лишнюю информацию в селекте
        self.check_login(session)
        orders_list = db.exec(
            DbQueries.orders.Select.user_info(),
            'fetchall'
        )

        if orders_list is None:
            return render_template('orders.html',
                                   orders=None)

        orders = db.exec(
            DbQueries.orders.Select.list_all(),
            'fetchall'
        )

        logger.debug(json.dumps(orders, ensure_ascii=False, indent=2))
        return render_template('orders.html',
                               orders=orders)

    def delete(self, session, order_id):
        """Delete order from database"""
        self.check_login(session)
        logger.debug(f"Removing order with id: {order_id}")

        try:
            db.exec(DbQueries.orders.Update.to_cancel_status_by_order_id(order_id))
            item_list = db.exec(
                DbQueries.orders.Select.product_rests_by_order_id(order_id),
                'fetchall'
            )
            logger.debug(f"Взял из бд [products] данные о товарах по заказу {order_id}")
            for item in item_list:
                total_amount = item.oam + item.pam
                db.exec(
                    DbQueries.products.Update.rests_by_id(total_amount, item.opid)
                )
            logger.debug(f"вернул товары из заказа {order_id} на полки")
            return flask.Response(status=200)
        except Exception as ex_:
            logger.error(ex_)
            return flask.Response(status=500)
