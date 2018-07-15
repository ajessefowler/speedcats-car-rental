from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, timedelta
import pytz

from inventory.models import Store, Vehicle, Reservation
from inventory.forms import RegisterForm

# Test home page view and template
class HomePageTest(TestCase):

    def test_view_url_exists_at_location(self):
        resp = self.client.get('/inventory/home/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('inventory:home'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('inventory:home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'inventory/home.html')

# Test FAQs page view and template
class FAQPageTest(TestCase):

    def test_view_url_exists_at_location(self):
        resp = self.client.get('/inventory/faqs/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('inventory:faqs'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('inventory:faqs'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'inventory/faqs.html')

# Test contact page view and template
class ContactPageTest(TestCase):

    def test_view_url_exists_at_location(self):
        resp = self.client.get('/inventory/contact/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('inventory:contact'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('inventory:contact'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'inventory/contact.html')

# Test feedback page view and template
class FeedbackPageTest(TestCase):

    def test_view_url_exists_at_location(self):
        resp = self.client.get('/inventory/feedback/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('inventory:feedback'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('inventory:feedback'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'inventory/feedback.html')

# Test locations page view and template
class LocationsPageTest(TestCase):

    def test_view_url_exists_at_location(self):
        resp = self.client.get('/inventory/locations/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('inventory:locations'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('inventory:locations'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'inventory/locations.html')
'''
class RegisterTest(TestCase):
    def test_post_request(self):
        form = RegisterForm()
        test_user = User.objects.create_user(username='test', password='12345')
        resp = self.client.post()

    def test_get_request(self):
        pass
'''
# Test index view and logic
class IndexTest(TestCase):

    def test_store_locations(self):
        Store.objects.create(ID=1, address='test', city='test', state='OH', zipcode='43235', phone='1111111111', email='test@test.com')
        resp = self.client.get(reverse('inventory:index'))
        self.assertEqual(resp.context['locations'], '[{"address": "test", "city": "test", "state": "OH"}]')

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('inventory:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'inventory/index.html')

# Test vehicle list view and logic
class VehicleListTest(TestCase):

    def test_bad_store_selection(self):
        pickup_id = 500
        pickup_time = datetime.now() + timedelta(days=1)
        dropoff_id = 1
        dropoff_time = datetime.now() + timedelta(days=3)

        resp = self.client.post('/inventory/vehicles/', {'pickuplocationid':pickup_id, 'pickuptimeformat':pickup_time, 'dropofflocationid':dropoff_id, 'dropofftimeformat':dropoff_time})
        self.assertEqual(resp.status_code, 404)

    def test_empty_store_selection(self):
        resp = self.client.post('/inventory/vehicles/')
        self.assertEqual(resp.status_code, 404)

    def test_valid_store_selection(self):
        Store.objects.create(ID=1, address='test', city='test', state='OH', zipcode='43235', phone='1111111111', email='test@test.com')

        pickup_id = 1
        pickup_time = datetime(2019, 1, 1, 12, 0).strftime('%Y-%m-%d %H:%M')
        dropoff_id = 1
        dropoff_time = datetime(2019, 1, 3, 12, 0).strftime('%Y-%m-%d %H:%M')

        resp = self.client.post('/inventory/vehicles/', {'pickuplocationid':pickup_id, 'pickuptimeformat':pickup_time, 'dropofflocationid':dropoff_id, 'dropofftimeformat':dropoff_time})
        self.assertEqual(resp.status_code, 200)

    def test_vehicle_no_reservations(self):
        Store.objects.create(ID=1, address='test', city='test', state='OH', zipcode='43235', phone='1111111111', email='test@test.com')

class VehicleDetailTest(TestCase):

    def test_valid_vehicle(self):
        test_store = Store.objects.create(ID=1, address='test', city='test', state='OH', zipcode='43235', phone='1111111111', email='test@test.com')
        Vehicle.objects.create(VIN=111, store=test_store, year='2018', make='Honda', model='Civic', color='black', mileage=14794, description='test', price=85.99, status='a', vehicle_type='c')

        resp = self.client.get('/inventory/1/1/')
        self.assertEqual(resp.status_code, 200)

    def test_invalid_vehicle(self):
        test_store = Store.objects.create(ID=1, address='test', city='test', state='OH', zipcode='43235', phone='1111111111', email='test@test.com')
        Vehicle.objects.create(VIN=111, store=test_store, year='2018', make='Honda', model='Civic', color='black', mileage=14794, description='test', price=85.99, status='a', vehicle_type='c')

        resp = self.client.get('/inventory/1/2/')
        self.assertEqual(resp.status_code, 404)

class ReservationDetailTest(TestCase):

    def setUp(self):
        pickup_time = datetime(2019, 1, 1, 12, 0).strftime('%Y-%m-%d %H:%M')
        dropoff_time = datetime(2019, 1, 3, 12, 0).strftime('%Y-%m-%d %H:%M')

        test_user = User.objects.create_user(username='test', password='secret')
        test_user.save()

        test_store = Store.objects.create(ID=1, address='test', city='test', state='OH', zipcode='43235', phone='1111111111', email='test@test.com')
        test_store.save()

        test_vehicle = Vehicle.objects.create(VIN=111, store=test_store, year='2018', make='Honda', model='Civic', color='black', mileage=14794, description='test', price=85.99, status='a', vehicle_type='c')
        test_vehicle.save()

        test_reservation = Reservation.objects.create(user=test_user, vehicle=test_vehicle, pick_up_time=pickup_time, pick_up_location=test_store, drop_off_time=dropoff_time, drop_off_location=test_store)
        test_reservation.save()

    def test_logged_in(self):
        login = self.client.login(username='test', password='secret')
        resp = self.client.get('/inventory/reservation/1')

        self.assertEqual(str(resp.context['user']), 'test')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'inventory/reservation.html')

    def test_redirect_if_logged_out(self):
        resp = self.client.get('/inventory/reservation/1')
        self.assertRedirects(resp, '/accounts/login/?next=/inventory/reservation/1')

    def test_logged_in_viewing_other_user(self):
        test_user2 = User.objects.create_user(username='test2', password='secret2')
        test_user2.save()

        login = self.client.login(username='test2', password='secret2')
        resp = self.client.get('/inventory/reservation/1')

        self.assertEqual(resp.status_code, 404)

class ModifyReservationTest(TestCase):

    def setUp(self):
        pickup_time = datetime(2019, 1, 1, 12, 0).strftime('%Y-%m-%d %H:%M')
        dropoff_time = datetime(2019, 1, 3, 12, 0).strftime('%Y-%m-%d %H:%M')

        test_user = User.objects.create_user(username='test', password='secret')
        test_user.save()

        test_store = Store.objects.create(ID=1, address='test', city='test', state='OH', zipcode='43235', phone='1111111111', email='test@test.com')
        test_store.save()

        test_vehicle = Vehicle.objects.create(VIN=111, store=test_store, year='2018', make='Honda', model='Civic', color='black', mileage=14794, description='test', price=85.99, status='a', vehicle_type='c')
        test_vehicle.save()

        test_reservation = Reservation.objects.create(user=test_user, vehicle=test_vehicle, pick_up_time=pickup_time, pick_up_location=test_store, drop_off_time=dropoff_time, drop_off_location=test_store)
        test_reservation.save()

    def test_logged_in(self):
        login = self.client.login(username='test', password='secret')
        resp = self.client.get('/inventory/reservation/1/modify/')

        self.assertEqual(str(resp.context['user']), 'test')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'inventory/modify.html')

    def test_redirect_if_logged_out(self):
        resp = self.client.get('/inventory/reservation/1/modify/')
        self.assertRedirects(resp, '/accounts/login/?next=/inventory/reservation/1/modify/')

    def test_logged_in_viewing_other_user(self):
        test_user2 = User.objects.create_user(username='test2', password='secret2')
        test_user2.save()

        login = self.client.login(username='test2', password='secret2')
        resp = self.client.get('/inventory/reservation/1/modify/')

        self.assertEqual(resp.status_code, 404)