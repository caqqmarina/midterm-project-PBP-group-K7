from django.test import TestCase, Client
from django.urls import reverse
from .models import Faculty, Canteen
from django.contrib.auth.models import User

class MainViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        Faculty.objects.create(name="Engineering")
        self.canteen = Canteen.objects.create(name="Main Canteen", faculty_id=1)

    def test_homepage_url_is_exist(self):
        response = self.client.get(reverse('main:homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')

    def test_login_and_register_view(self):
        response = self.client.get(reverse('main:login_and_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_and_register.html')

    def test_faculty_view(self):
        response = self.client.get(reverse('main:faculty'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faculty.html')
        self.assertContains(response, "Engineering")

    def test_canteen_view(self):
        response = self.client.get(reverse('main:canteen', args=[self.canteen.name]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'canteen.html')
        self.assertContains(response, self.canteen.name)

    def test_add_faculty_view(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Non-admin user should be redirected to login
        response = self.client.get(reverse('main:add_faculty'))
        self.assertEqual(response.status_code, 302)  # Redirected due to permissions

        # Make user an admin and test again
        user.is_staff = True
        user.save()
        response = self.client.get(reverse('main:add_faculty'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_faculty.html')

    def test_show_json(self):
        response = self.client.get(reverse('main:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

