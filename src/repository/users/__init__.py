import flask
from flask import redirect, url_for, render_template, Blueprint
from loguru import logger
from database import db
from repository.sql import DbQueries
from munch import DefaultMunch

as_class = DefaultMunch.fromDict
users_page = Blueprint('users_page', __name__)


class Users:
    def __init__(self):
        pass

    @staticmethod
    def check_login(session):
        logger.debug(session)
        if 'username' not in session:
            return redirect(url_for('admin_page.login'))

    def get(self, session):
        self.check_login(session)
        logger.debug("THIS IS MOCK YET!")
        return render_template('not-ready.html')

    def post(self, session):
        self.check_login(session)
        logger.debug("THIS IS MOCK YET!")
        return render_template('not-ready.html')

    def delete(self, session, user_id):
        self.check_login(session)
        logger.debug(f"Removing user with id: {user_id}")
        try:
            db.exec(DbQueries.users.Delete.by_user_id(user_id))
            return flask.Response(status=200)
        except Exception as ex_:
            logger.error(ex_)
            return flask.Response(status=500)
