from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from myTimeOffRequest.myTimeOffRequest.models import Employee, TimeOffRequest

class TimeOffRequestModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.time_off_request = TimeOffRequest.objects.create(
            start_date=datetime.now(),
            end_date=datetime.now(),
            employee_id=self.user
        )

    def test_create_time_off_request(self):
        self.assertEqual(TimeOffRequest.objects.count(), 1)
        self.assertEqual(self.time_off_request.employee_id, self.user)

    def test_time_off_request_str(self):
        expected_object_name = f'{self.time_off_request.start_date} - {self.time_off_request.end_date}'
        self.assertEqual(str(self.time_off_request), expected_object_name)
