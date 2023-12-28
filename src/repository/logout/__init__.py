from flask import redirect, url_for, Blueprint
from loguru import logger
from munch import DefaultMunch

as_class = DefaultMunch.fromDict
logout_page = Blueprint('logout_page', __name__)


class Logout:
    def __init__(self):
        pass

    @staticmethod
    def check_login(session):
        logger.debug(session)
        if 'username' not in session:
            return redirect(url_for('admin_page.index'))

    def get(self, session):
        self.check_login(session)
        session.pop('username', None)
        return redirect(url_for('admin_page.login'))
