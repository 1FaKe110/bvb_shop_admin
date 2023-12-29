from flask import redirect, url_for, render_template, request, Blueprint, flash
from loguru import logger
from werkzeug.security import check_password_hash

from database import db
from repository.sql import DbQueries
from munch import DefaultMunch

as_class = DefaultMunch.fromDict
login_page = Blueprint('login_page', __name__)


class Login:
    def __init__(self):
        pass

    @staticmethod
    def check_login(session):
        logger.debug(session)
        if 'username' in session:
            return redirect(url_for('admin_page.categories'))

        logger.debug("Пользователь не авторизован, возвращаю страницу логина")
        return

    def get(self, session):
        self.check_login(session)
        return render_template('login.html')

    def post(self, session):
        self.check_login(session)

        _login = request.form['username']
        password = request.form["password"]

        user_info = db.exec(
            DbQueries.adminUsers.Select.by_login(_login),
            "fetchone"
        )

        if user_info is None:
            logger.info('Пользователь не найден')
            flash('Пользователь не найден', 'error')
            return render_template('login.html')

        if not check_password_hash(user_info.password, password):
            logger.info('Не верный пароль')
            flash('Не верный логин или пароль', 'error')
            return render_template('login.html')

        if not user_info.is_admin:
            logger.info("Пользователь не является администратором")
            flash('Пользователь не является администратором', 'error')
            return render_template('login.html')

        session['username'] = _login  # устанавливаем сессию
        return redirect(url_for('admin_page.orders'))
