class Orders:
    class Select:

        @staticmethod
        def list_all():
            return ("select distinct(o.order_id), "
                    "o.status_id, o.address, "
                    "cast(cast(o.datetime as date) as text), "
                    "cast(cast(o.creation_time as date) as text), "
                    "ose.id as status_id, "
                    "ose.name, temp.total_sum as position_total_sum "
                    "from orders o inner join order_status ose on ose.id = o.status_id "
                    "inner join ( "
                    "select order_id, SUM(position_price * amount) as total_sum "
                    "from orders "
                    "group by order_id ) as temp on temp.order_id = o.order_id "
                    "order by o.order_id asc;")

        @staticmethod
        def user_info():
            return ("Select distinct(order_id), user_id, status_id, "
                    "address, cast(datetime as text), "
                    "ose.id as status_id, ose.name "
                    "from orders o "
                    "inner join order_status ose on ose.id = o.status_id "
                    "order by order_id asc")

        @staticmethod
        def user_info_by_order_id(order_id):
            return ("Select cast(cast(o.creation_time as date) as text), "
                    "o.status_id, "
                    "os.name as status_name "
                    "from orders o "
                    "inner join order_status os on os.id = o.status_id "
                    f"where order_id = {order_id} "
                    f"order by order_id desc "
                    f"limit 1")

        @staticmethod
        def positions_by_order_id(order_id):
            return ("select p.id as id, "
                    "p.name as name, "
                    "p.price as price, "
                    "o.amount as amount "
                    "from orders o "
                    "LEFT JOIN products p on p.id = o.position_id "
                    f"WHERE order_id = {order_id} "
                    f"order by order_id asc")

        @staticmethod
        def detailed_info(order_id):
            return ("Select distinct(order_id), "
                    "status_id, address, "
                    "cast(datetime as text), "
                    "ose.id as status_id, "
                    "ose.name as status_name, "
                    "u.fio, "
                    "u.phone, "
                    "u.email "
                    "from orders o "
                    "inner join order_status ose on ose.id = o.status_id "
                    "inner join users_new u on o.user_id = u.id "
                    f"where order_id = {order_id}")

        @staticmethod
        def product_info_by_order_id(order_id):
            return ("select p.id as id, "
                    "p.name as name, "
                    "p.price as price, "
                    "o.amount as amount, "
                    "p.amount as total_amount, "
                    "o.status_id "
                    "from orders o "
                    "LEFT JOIN products p on p.id = o.position_id "
                    f"WHERE order_id = {order_id} "
                    "order by p.id asc")

        @staticmethod
        def product_rests_by_order_id(order_id):
            return (f"SELECT o.position_id as opid, "
                    f"o.amount as oam, "
                    f"p.amount as pam "
                    "from orders o "
                    "inner join products p on p.id = o.position_id "
                    f"where order_id={order_id};")

        @staticmethod
        def product_rests_by_order_id_and_product_id(order_id, product_id):
            return (f"SELECT o.position_id as opid, "
                    f"o.amount as oam, "
                    f"p.amount as pam "
                    "from orders o "
                    "inner join products p on p.id = o.position_id "
                    f"where o.order_id={order_id} and o.position_id={product_id};")

        @staticmethod
        def unique_orders_by_order_id(order_id):
            return (f"select distinct(order_id), status_id, user_id "
                    f"from orders "
                    f"where order_id = {order_id}")

        @staticmethod
        def status_matrix_by_status(status):
            return (f"Select * from order_status "
                    f"where id in "
                    f"(SELECT out_state "
                    f"FROM public.order_status_matrix "
                    f"where in_state = {status}) "
                    f"order by id asc;")

        @staticmethod
        def status_matrix_ext_by_status(in_status, out_state):
            return ("SELECT in_state, out_state "
                    "FROM public.order_status_matrix "
                    f"WHERE in_state = {in_status} and "
                    f"out_state = {out_state};")

    class Update:

        @staticmethod
        def to_cancel_status_by_order_id(order_id):
            return (f"UPDATE orders "
                    f"SET status_id=5 "
                    f"WHERE order_id={order_id};")

        @staticmethod
        def status_by_order_id(status, order_id):
            return (f"UPDATE orders "
                    f"SET status_id={status} "
                    f"WHERE order_id={order_id};")

        @staticmethod
        def position_amount_by_product_id(amount, product_id):
            return (f"UPDATE public.orders "
                    f"SET amount={amount} "
                    f"WHERE position_id={product_id};")

    class Delete:

        @staticmethod
        def position_by_order_id_and_product_id(order_id, product_id):
            return (f"DELETE FROM orders "
                    f"WHERE order_id={order_id} and "
                    f"position_id={product_id};")
