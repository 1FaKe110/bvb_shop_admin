import flask
from flask import redirect, url_for, render_template, request, Blueprint
from loguru import logger
from database import db
from repository.sql import DbQueries
from munch import DefaultMunch

as_class = DefaultMunch.fromDict
categories_page = Blueprint('categories_page', __name__)


class Categories:
    def __init__(self):
        pass

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

        return render_template('categories.html',
                               categories=categories_list)

    def post(self, session):
        self.check_login(session)

        form = as_class(request.form.to_dict())
        logger.debug(form)

        logger.debug('Меняем что-то в категориях')
        ct_id = form.ct_id.replace('.', '')
        ct_name = form.ct_name
        ct_image_path = form.categoryImagePath
        db.exec(
            DbQueries.categories.Update.name_and_image_by_id(ct_name, ct_image_path, ct_id)
        )

        return self.get(session)

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
