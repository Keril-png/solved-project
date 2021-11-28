from django.contrib.auth import get_user_model
from django.test import TestCase
from problems.models import Problem

User = get_user_model()


class ProblemModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.problem = Problem.objects.create(
            author = cls.user,
            text = 'Тестовый текст задачи!?'
        )
        
    