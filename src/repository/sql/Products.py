class Products:
    class Select:

        @staticmethod
        def all_by_name():
            return ("Select * "
                    "from products "
                    "order by name asc")

    class Delete:

        @staticmethod
        def by_id(product_id):
            return (f"DELETE FROM products "
                    f"WHERE id={product_id};")

    class Update:

        @staticmethod
        def by_id(form):
            return (f"UPDATE products SET "
                    f"name='{form.pr_name}', "
                    f"by_price={form.pr_by_price}, "
                    f"price={form.pr_price}, "
                    f"amount={form.pr_amount}, "
                    f"brand='{form.pr_brand}', "
                    f"price_dependency={bool(form.pr_price_dependency)}, "
                    f"category_id={int(form.categoryParentName)}, "
                    f"image_id=Null, "
                    f"description='{form.pr_description}', "
                    f"image_path='{form.categoryImagePath}' "
                    f"WHERE id={form.pr_id}; "
                    )

        @staticmethod
        def rests_by_id(amount, product_id):
            return (f"UPDATE products "
                    f"SET amount={amount} "
                    f"WHERE id={product_id};")

    class Insert:

        @staticmethod
        def new_product(name, by_price, sell_price, amount, brand, in_dollar, category_id, description, image):
            return ("INSERT INTO products "
                    "(name, by_price, price, amount, brand, price_dependency, category_id, "
                    "description, image_path) "
                    f"VALUES "
                    f"('{name}', {by_price}, {sell_price}, {amount}, '{brand}', {in_dollar}, {category_id}, "
                    f"'{description}', '{image}');")
