from rest_framework.test import APITestCase

from store.models import (
    Category,
    Product,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
)


class TestModel(APITestCase):

    def tests_category_return_get_absolute_trl(self):
        response = Category(name='Name', slug='name')
        res = Category.get_absolute_url(response)
        self.assertEqual(res, '/shop/name/')

    def test_string_return_category_name(self):
        user = Category(name='Fashion')
        check = Category.__str__(user)
        self.assertEqual(check, 'Fashion')

    def test_string_return_product_type_name(self):
        user = ProductType(name='Clothes')
        check = ProductType.__str__(user)
        self.assertEqual(check, 'Clothes')

    def test_string_return_product_title(self):
        user = Product(title='Clothes')
        check = Product.__str__(user)
        self.assertEqual(check, 'Clothes')

    def tests_product_return_get_absolute_trl(self):
        response = Product(title='Product', slug='product')
        res = Product.get_absolute_url(response)
        self.assertEqual(res, '/product')

    def test_string_return_proguctspecification_value(self):
        user = ProductSpecificationValue(value='Valued')
        check = ProductSpecificationValue.__str__(user)
        self.assertEqual(check, 'Valued')

    def test_string_return_productspecification_name(self):
        user = ProductSpecification(name='Pages')
        check = ProductSpecification.__str__(user)
        self.assertEqual(check, 'Pages')
