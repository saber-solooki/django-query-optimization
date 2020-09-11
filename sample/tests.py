import sys

from django.db.models import Prefetch
from django.test import TestCase

# Create your tests here.
from sample.query_tools import query_reporter
from sample.models import User, Address, SalesDoc, SalesDocItem, Product


class BaseTestCase(TestCase):
    def setUp(self):
        from django.conf import settings
        settings.DEBUG = True


class UserCountAndExistTest(BaseTestCase):
    number_of_user_in_db = 1000

    user_data = {
        "password": "123",
        "first_name": "saber",
        "last_name": "solooki"
    }

    def setUp(self):
        super().setUp()
        self.user_bulk_create()

    def user_bulk_create(self):
        user_for_create = []
        for i in range(self.number_of_user_in_db):
            username = "ss" + str(i)
            user_for_create.append(User(username=username, **self.user_data))

        User.objects.bulk_create(user_for_create)

    def test_check_users_exist_and_do_business(self):
        users = User.objects.filter(first_name__startswith="sa")
        is_user_exist = users.exists()

        size_of_result = sys.getsizeof(users)
        print(f'size of user object to do business is {size_of_result}')

        size_of_result = sys.getsizeof(is_user_exist)
        print(f'size of user existance to do business is {size_of_result}')

        if users:
            print("User existance check with query set and do business")

        if is_user_exist:
            print("user existance check with exist query and do business")

    @query_reporter
    def test_check_users_count(self):
        users = User.objects.filter(first_name__startswith="sa")
        user_count = users.count()

        print(f'size of user {len(users)}')
        print(f'size of user count query {user_count}')


class UserCreateUpdateTest(BaseTestCase):
    number_of_user_in_db = 2

    user_data = {
        "password": "123",
        "first_name": "saber",
        "last_name": "solooki"
    }

    def test_create_in_for(self):
        for i in range(self.number_of_user_in_db):
            username = "ss" + str(i)
            User.objects.create(username=username, **self.user_data)

    def test_bulk_create(self):
        self.user_bulk_create()

    def test_update_user_in_for(self):
        self.user_bulk_create()

        # for u in User.objects.all().order_by('id')[:10]:
        #     print(u.username)

        for i in range(self.number_of_user_in_db):
            User.objects.filter(id=i).update(username=str(i))

        # for u in User.objects.all().order_by('id')[:10]:
        #     print(u.username)

    def test_bulk_update(self):
        self.user_bulk_create()

        user_for_update = []
        for user in User.objects.all().order_by('id'):
            user.username = "new username" + str(user.id)
            user_for_update.append(user)

        User.objects.bulk_update(user_for_update, ['username'])

        # for u in User.objects.all().order_by('id')[:10]:
        #     print(u.username)

    def user_bulk_create(self):
        user_for_create = []
        for i in range(self.number_of_user_in_db):
            username = "ss" + str(i)
            user_for_create.append(User(username=username, **self.user_data))

        User.objects.bulk_create(user_for_create)


class AddressAndUserTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.create_user_and_address()

    def create_user_and_address(self):
        user1 = User.objects.create(username="saber1", password="123")
        user2 = User.objects.create(username="saber2", password="123")
        user3 = User.objects.create(username="saber3", password="123")

        Address.objects.create(user=user1, plain_address='address 1', postal_code='1', lat='35.123', long='52.345')
        Address.objects.create(user=user1, plain_address='address 2', postal_code='2', lat='35.123', long='52.345')
        Address.objects.create(user=user2, plain_address='address 3', postal_code='3', lat='35.123', long='52.345')
        Address.objects.create(user=user3, plain_address='address 4', postal_code='4', lat='35.123', long='52.345')

        product1 = Product.objects.create(name="product 1", code='1')
        product2 = Product.objects.create(name="product 2", code='2')

        sd = SalesDoc.objects.create(user=user1, payment_method=1, total_price="3000", description="tozihat")
        SalesDocItem.objects.create(sale_doc=sd, product=product1, quantity=1)
        SalesDocItem.objects.create(sale_doc=sd, product=product2, quantity=2)

    @query_reporter
    def test_read_all_address_field(self):
        for address in Address.objects.all():
            print(address.plain_address)

    @query_reporter
    def test_read_all_address_field_in_correct_way(self):
        for address in Address.objects.all().only('plain_address'):
            print(address.plain_address)

    @query_reporter
    def test_read_all_address_with_user_info(self):
        for address in Address.objects.all().only('user__username'):
            print(address.user.username)

    @query_reporter
    def test_read_all_address_with_user_info_in_correct_way(self):
        for address in Address.objects.all().select_related('user').only('user__username'):
            print(address.user.username)

    @query_reporter
    def test_read_all_user_with_address_info(self):
        for user in User.objects.all():
            for address in user.user_ad.all():
                print(f'user {user.username} address is {address.plain_address}')

    @query_reporter
    def test_read_all_user_with_address_info_in_correct_way1(self):
        for user in User.objects.all().only('username').prefetch_related('user_ad'):
            for address in user.user_ad.all():
                print(f'user {user.username} address is {address.plain_address}')

    @query_reporter
    def test_read_all_user_with_address_info_in_correct_way2(self):
        for user in User.objects.all().only('username').prefetch_related(Prefetch('user_ad', Address.objects.only('plain_address'))):
            for address in user.user_ad.all():
                print(f'user {user.username} address is {address.plain_address}')

    @query_reporter
    def test_read_all_user_with_address_info_in_correct_way3(self):
        for user in User.objects.all().only('username').prefetch_related(Prefetch('user_ad', Address.objects.only('user_id', 'plain_address'))):
            for address in user.user_ad.all():
                print(f'user {user.username} address is {address.plain_address}')

    @query_reporter
    def test_read_user_with_buy_history(self):
        for user in User.objects.all().only('username').prefetch_related(
                Prefetch('user_sd', SalesDoc.objects.only('user_id', 'payment_method')),
                Prefetch('user_sd__sale_doc_sdi', SalesDocItem.objects.only('sale_doc_id', 'quantity', 'product_id')),
                Prefetch('user_sd__sale_doc_sdi__product', Product.objects.only('name', 'code'))):
            for sales_doc in user.user_sd.all():
                print(f'user {user.username} sales doc id is {sales_doc.id}')

                for doc_item in sales_doc.sale_doc_sdi.all():
                    print(f'doc item quantity for sales doc {sales_doc.id} is {doc_item.quantity}')
                    print(f'doc item product for sales doc {sales_doc.id} is {doc_item.product.name}')
