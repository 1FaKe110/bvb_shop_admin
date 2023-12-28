class Products:
    class Select:

        @staticmethod
        def all_by_name():
            return ("Select * "
                    "from products "
                    "order by name asc")

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
