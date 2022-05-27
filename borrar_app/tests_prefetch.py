from datetime import datetime
from django.test import TestCase
from borrar_app.models import UserProfile, Job
from django.contrib.auth.models import User


class SomeTest(TestCase):

    def setUp(self) -> None:
        self.m = User.objects.create(username="mauricio")
        UserProfile.objects.create(user=self.m, date_of_birth=datetime.now())
        self.j1 = Job.objects.create(employee=self.m)
        self.j2 = Job.objects.create(employee=self.m)

    def test_some_stupid(self):
        a = 1

        job_ids = UserProfile.get_all_profiles_with_job_ids().first().job_ids

        self.assertEqual(set(job_ids.split(",")), set([str(self.j1.id), str(self.j2.id)]))