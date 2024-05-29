from django.test import TestCase
from .models import Vacancy, Question, Promo, News, User, Product, Order, Customer, Employee, Admin, Sale, Feedback
from datetime import datetime

# class ContactTest(TestCase):
#     def setUp(self):
#         # Создаем необходимые объекты моделей для тестирования
#         self.contact = Contact.objects.create(
#             employee_name='John Doe',
#             description='Lorem ipsum',
#             phone='123456789',
#             email='john@example.com'
#         )

#     def test_contact_str(self):
#         """Тестирование метода __str__ модели Contact"""
#         self.assertEqual(str(self.contact), 'John Doe')


# class ArticleTest(TestCase):
#     def setUp(self):
#         # Создаем объект модели для тестирования
#         self.article = Article.objects.create(
#             title='Test Article',
#             content='Lorem ipsum',
#         )

#     def test_article_str(self):
#         """Тестирование метода __str__ модели Article"""
#         self.assertEqual(str(self.article), 'Test Article')


class VacancyTest(TestCase):
    def setUp(self):
        self.vacancy = Vacancy.objects.create(
            title='Test Vacancy',
            description='Lorem ipsum',
            salary=1000.00,
            requirements='Lorem ipsum',
            job_type='full-time'
        )

    def test_vacancy_str(self):
        """Тестирование метода __str__ модели Vacancy"""
        self.assertEqual(str(self.vacancy), 'Test Vacancy')

class QuestionTest(TestCase):
    def setUp(self):
        self.question = Question.objects.create(
            question='Test Question',
            answer='Test Answer'
        )

    def test_question_str(self):
        """Тестирование метода __str__ модели Question"""
        self.assertEqual(str(self.question), 'Test Question')

class PromoCodeTest(TestCase):
    def setUp(self):
        self.promo_code = Promo.objects.create(
            code='TEST123',
            description='Lorem ipsum',
            expiration_date=datetime.now()
        )

    def test_promo_code_str(self):
        """Тестирование метода __str__ модели PromoCode"""
        self.assertEqual(str(self.promo_code), 'TEST123')

class UserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test_user',
            email='test@example.com'
        )

    def test_user_str(self):
        """Тестирование метода __str__ модели User"""
        self.assertEqual(str(self.user), 'test_user')

class ProductTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            code='12345',
            name='Test',
            characteristics='Test',
            price=10.0
        )

    def test_product_str(self):
        """Тестирование метода __str__ модели product"""
        expected_str = 'Test 12345 (10.0 рублей)'
        self.assertEqual(str(self.product), expected_str)


class CustomerTest(TestCase):
    def setUp(self):
        # Создаем объект модели для тестирования
        user = User.objects.create(username='test_user', email='test@example.com')
        self.customer = Customer.objects.create(
            user=user,
            phone_number='+375-25-111-11-11'
        )

    def test_customer_str(self):
        """Тестирование метода __str__ модели Customer"""
        self.assertEqual(str(self.customer), 'test_user')

class EmployeeTest(TestCase):
    def setUp(self):
        # Создаем объект модели для тестирования
        user = User.objects.create(username='test_user', email='test@example.com')
        self.employee = Employee.objects.create(
            user=user,
            phone_number='+375-25-111-11-11'
        )

    def test_employee_str(self):
        """Тестирование метода __str__ модели Employee"""
        self.assertEqual(str(self.employee), 'test_user')


from Autosalon.forms import EmployeeSignUpForm

class EmployeeSignUpFormTest(TestCase):
    def test_invalid_phone_number(self):
        form = EmployeeSignUpForm(data={
            'username': 'test_user',
            'phone_number': '123456789',
            'birth_date': '2000-01-01',
            'photo': None
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['phone_number'], ['Phone number must be in the format +375 -- --- -- --.'])

    def test_invalid_birth_date(self):
        form = EmployeeSignUpForm(data={
            'username': 'test_user',
            'phone_number': '+375 25 123 45 67',
            'birth_date': '2023-01-01',
            'photo': None
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['birth_date'], ['You must be at least 18 years old to register.'])
    
