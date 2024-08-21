from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from courses.models import Course
from users.models import CustomUser, Balance

class CourseTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            author='Author',
            title='Test Course',
            start_date='2024-08-21T00:00:00Z',
            price=100.00
        )
        Balance.objects.create(user=self.user, amount=1000)

    def test_course_list(self):
        response = self.client.get('/api/v1/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('title', response.data[0])

    def test_course_pay(self):
        response = self.client.post(f'/api/v1/courses/{self.course.id}/pay/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.user.subscriptions.filter(course=self.course).exists())
        self.assertEqual(self.user.balance.amount, 900.00)

