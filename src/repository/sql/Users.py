class Users:
    class Select:
        pass

    class Update:
        pass

    class Delete:
        pass


class UsersAdmin:
    class Select:

        @staticmethod
        def by_login(login):
            return (f"Select phone, password, is_admin "
                    f"from users "
                    f"where login = '{login}'")

    class Update:
        pass

    class Delete:
        pass
