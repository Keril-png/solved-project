from django.test import TestCase, Client
from django.urls import reverse
from problems.models import Problem, User
from django.contrib.auth import get_user_model

from problems.views import problem_detail 

class NotAuthotizedURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
    
    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_NotAuthUserCantCreatePost(self): 
        response = self.client.get(reverse('new_problem'), follow=True) 
        self.assertRedirects(response, '/auth/login/?next=/problems/create/') 
        
    
        
class AuthorizedTests(TestCase): 
    def setUp(self): 
        self.client = Client() 
        self.myuser = User.objects.create( 
            username = 'biba',  
            password = 'boba' 
        ) 
        self.client.force_login(self.myuser) 
        
    def test_Profile(self): 
        response = self.client.get(reverse('profile', kwargs={'username': self.myuser.username})) 
        self.assertEqual(response.status_code, 200)
        
    def test_AuthUserCanCreateProblem(self):
        test_title = 'Задача номер ноль'
        test_text = 'Тестовый текст для задачки.'
        response = self.client.post(
            reverse('new_problem'),
            {'title': test_title, 'description': test_text},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        
        count_problem = Problem.objects.count()
        new_problem = Problem.objects.first()
        
        self.assertEqual(count_problem, 1) 
        self.assertEqual(new_problem.description, test_text) 
        self.assertEqual(new_problem.author, self.myuser)
        
    def test_PostIsEverywhere(self):
        test_title = 'Задача номер ноль'
        test_text = 'Тестовый текст для задачки.'
        problem = Problem.objects.create(
            title = test_title,
            description = test_text,
            author = self.myuser
        )
        urls = [
            reverse('index'),
            reverse('profile', kwargs={'username':self.myuser.username}),
            reverse(
                'problem_detail',
                kwargs={'problem_id': problem.id}
            )
        ]
        
        for url in urls:
            response = self.client.get(url)
            if response.context.get('paginator') is None:
                problem = response.context.get('problem')
            else:
                p = response.context.get('paginator')
                self.assertEqual(1, p.count)
                problem = p.page(1).object_list[0]
            
            self.assertEqual(problem.title, test_title)
            self.assertEqual(problem.description, test_text)
            self.assertEqual(problem.author, self.myuser)
                    
        
    def test_AuthUserCanEdit(self):
        test_title = 'Задача номер ноль'
        test_text = 'Тестовый текст для задачки.'
        
        new_title = 'Редактированная задача номер ноль'
        new_text = 'Новый текст для задачки'
        
        
        problem = Problem.objects.create(
            title = test_title,
            description = test_text,
            author = self.myuser
        )
        self.client.post(
            reverse('edit_problem', args=[problem.id]),
            {'title': new_title, 'description': new_text},
            Follow=True
        )
        
        urls = [
            reverse('index'),
            reverse('profile', kwargs={'username':self.myuser.username}),
            reverse(
                'problem_detail',
                kwargs={'problem_id': problem.id}
            )
        ]
        
        for url in urls:
            for url in urls:
                response = self.client.get(url)
            if response.context.get('paginator') is None:
                problem = response.context.get('problem')
            else:
                p = response.context.get('paginator')
                self.assertEqual(1, p.count)
                problem = p.page(1).object_list[0]
            
            self.assertEqual(problem.title, test_title)
            self.assertEqual(problem.description, new_text)
            self.assertEqual(problem.author, self.myuser)
        
        
    