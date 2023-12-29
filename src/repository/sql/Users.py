class Users:
    class Select:
        pass

    class Update:

        @staticmethod
        def username_by_user_id(user_data, user_id):
            return (f"UPDATE public.users "
                    f"SET username='{user_data.fio}', "
                    f"phone='{user_data.phone}', "
                    f"email='{user_data.email}' "
                    f"WHERE id={user_id};")

    class Delete:

        @staticmethod
        def by_user_id(user_id):
            return (f"DELETE FROM users_new "
                    f"WHERE user_id={user_id};")


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
