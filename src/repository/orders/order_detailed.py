import json

import flask
from flask import redirect, url_for, render_template, request, Blueprint, flash
from loguru import logger
from database import db
from repository.orders import Orders
from repository.sql import DbQueries
from munch import DefaultMunch

as_class = DefaultMunch.fromDict
orders_detailed_page = Blueprint('orders_detailed_page', __name__)


class OrdersDetailed:
    def __init__(self):
        pass

    @staticmethod
    def check_login(session):
        logger.debug(session)
        if 'username' not in session:
            return redirect(url_for('admin_page.login'))

    @logger.catch
    def get(self, session, order_id):
        self.check_login(session)

        order_obj = db.exec(
            DbQueries.orders.Select.detailed_info(order_id),
            'fetchone')

        if order_obj is None or not len(order_obj):
            logger.debug("переход на несуществующее заявление. Возвращаю на главную страницу")
            return redirect(url_for('admin_page.orders'))

        order_obj.datetime = order_obj.datetime[:10]
        order_obj.sum = 0
        order_obj.positions = db.exec(
            DbQueries.orders.Select.product_info_by_order_id(order_id),
            "fetchall"
        )
        for position in order_obj.positions:
            order_obj.sum += position.price * position.amount

        logger.debug(json.dumps(order_obj, indent=2, ensure_ascii=False))
        cur_order_status = db.exec(
            DbQueries.orders.Select.product_info_by_order_id(order_id),
            'fetchone').status_id
        logger.debug(f"Заявление в статусе: {cur_order_status}: {order_obj.status_name}")

        order_statuses = db.exec(
            DbQueries.orders.Select.status_matrix_by_status(cur_order_status),
            'fetchall'
        )
        return render_template('order_detailed.html',
                               order=order_obj,
                               order_statuses=order_statuses)

    def update(self, session, order_id):
        self.check_login(session)
        logger.debug(f"updating order with id: {order_id}")
        logger.debug(json.dumps(request.json, indent=2, ensure_ascii=False))
        data = as_class(request.json)

        order_mini_info = db.exec(
            DbQueries.orders.Select.unique_orders_by_order_id(order_id),
            'fetchone'
        )

        if str(order_mini_info.status_id) != data.status.id:
            switch = db.exec(
                DbQueries.orders.Select.status_matrix_ext_by_status(order_mini_info.status_id, data.status.id),
                'fetchone'
            )
            if switch is None:
                logger.error("Попытка смены статуса не разрешенного в матрице!")
            else:
                logger.debug(f"Обновляю статус заказа [{order_mini_info.status_id} -> {data.status.id}]")
                db.exec(
                    DbQueries.orders.Update.status_by_order_id(data.status.id, order_id)
                )
                if data.status.id == 5:
                    Orders().delete(session, order_id)
        else:
            logger.debug(f'Статус заказа не изменен: {order_mini_info.status_id} -> {data.status.id}')

        db.exec(
            DbQueries.users.Update.username_by_user_id(data.user, order_mini_info.user_id)
        )
        logger.debug(f"данные о клиенте [{data.user.phone}] обновлены!")

        for pos in data.positions:
            pr_reply = db.exec(
                DbQueries.orders.Select.product_rests_by_order_id_and_product_id(order_id, pos.Id),
                'fetchone'
            )

            o_delta = pr_reply.oam - int(pos.Amount)
            if not o_delta:
                logger.debug(f"Кол-во товара №{pr_reply.opid} в заказе №{order_id} не изменилось")
            elif o_delta < 0:
                logger.debug(f"В заказе {order_id} есть доп списания по товару №{pr_reply.opid}")
                new_pr_amount = pr_reply.pam - abs(o_delta)
                new_or_amount = pr_reply.oam + abs(o_delta)
                if new_pr_amount < 0:
                    message = (f"Попытка списания товара #{pr_reply.opid}, которого не хватит на {pr_reply.pam}\n "
                               f"Остатки товара #{pr_reply.opid} изменены не будут")
                    flash(message, 'error')
                    logger.warning(message)
                else:
                    logger.debug(
                        f"Дополнительно списываю товар #{pr_reply.opid} в кол-ве {o_delta} шт по заказу №{order_id}")
                    self.update_order_and_product_rests(new_or_amount, new_pr_amount, pr_reply)
            else:
                new_pr_amount = pr_reply.pam + abs(o_delta)
                new_or_amount = pr_reply.oam - abs(o_delta)

                if new_or_amount < 0:
                    logger.warning(f"Попытка возврата товара #{pr_reply.opid}, которого не хватит на {pr_reply.oam}")
                    logger.debug(f"Остатки товара #{pr_reply.opid} изменены не будут")
                else:
                    logger.debug(f"Возвращаю на полки товар #{pr_reply.opid} в кол-ве №{o_delta} шт.")
                    self.update_order_and_product_rests(new_or_amount, new_pr_amount, pr_reply)

        return flask.Response(status=200)

    def delete(self, session, order_id, item_id):
        self.check_login(session)
        logger.debug(f"Removing item #{item_id} from order_id #{order_id}")
        try:
            item_list = db.exec(
                DbQueries.orders.Select.product_rests_by_order_id_and_product_id(order_id, item_id),
                'fetchall'
            )
            db.exec(
                DbQueries.orders.Delete.position_by_order_id_and_product_id(order_id, item_id)
            )
            for item in item_list:
                total_amount = item.oam + item.pam
                db.exec(
                    DbQueries.products.Update.rests_by_id(total_amount, item.opid)
                )
            logger.debug(f"вернул товары, от которых отказались на полку из заказа {order_id}")
            return flask.Response(status=200)
        except Exception as ex_:
            logger.error(ex_)
            return flask.Response(status=500)

    @staticmethod
    def update_order_and_product_rests(new_or_amount, new_pr_amount, pr_reply):
        db.exec(
            DbQueries.products.Update.rests_by_id(new_pr_amount, pr_reply.opid)
        )
        db.exec(
            DbQueries.orders.Update.position_amount_by_product_id(new_or_amount, pr_reply.opid)
        )
