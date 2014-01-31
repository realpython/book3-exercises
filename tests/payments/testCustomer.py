from payments.views import Customer
from django.test import TestCase
import mock

class CustomerTests(TestCase):


    def test_create_subscription(self):
    
        with mock.patch('stripe.Customer.create') as create_mock:

            cust_data = {'description':'test user', 'email':'test@test.com',
                         'card':'4242','plan':'gold'}
            cust = Customer.create("subscription", **cust_data)

            create_mock.assert_called_with(**cust_data)            
                    
    def test_create_one_time_bill(self):

        with mock.patch('stripe.Charge.create') as charge_mock:

            cust_data = {'description' :'email',
                         'card' : '1234',
                         'amount':'5000',
                         'currency':'usd'}
            
            cust = Customer.create("one_time", **cust_data)

            charge_mock.assert_called_with(**cust_data)
