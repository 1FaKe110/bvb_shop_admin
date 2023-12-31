class Categories:
    class Select:
        @staticmethod
        def all_by_id():
            return ("Select * "
                    "from categories "
                    "order by id asc")

    class Insert:

        @staticmethod
        def new_category(form):
            return ("INSERT INTO categories "
                    "(parent_id, name, image_path) "
                    f"VALUES"
                    f"({form.categoryParentId}, '{form.categoryName}', '{form.productImagePath}');")

    class Update:

        @staticmethod
        def name_and_image_by_id(category_name, category_image_path, category_id):
            return (f"UPDATE categories SET "
                    f"name='{category_name}', image_path='{category_image_path}' "
                    f"WHERE id={category_id};")

    class Delete:

        @staticmethod
        def by_id(category_id):
            return (f"DELETE FROM categories "
                    f"WHERE id={category_id};")
