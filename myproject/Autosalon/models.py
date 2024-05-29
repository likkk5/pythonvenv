from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    position = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=18,default='+375-25-123-45-67')
    email = models.EmailField()
    start_date = models.DateField()
    birth_date = models.DateField(default='2000-01-01')
    photo=models.ImageField(default='contact_photos/default_photo.png',upload_to='contact_photos/')

    def __str__(self):
        return self.user.username

class ProductType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    characteristics = models.TextField()
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    photo = models.ImageField(default='default_photo.png', upload_to='product_photos/', blank=True)
    def __str__(self):
        return f"{self.name} ({self.price} рублей)"
    
        
class Order(models.Model):
    buyer = models.ForeignKey(User, related_name='buyer', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  
    date_sold = models.DateTimeField(default=datetime.now())
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Добавлено поле для цены с учетом скидки
    promo_code = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f"{self.buyer.username}'s purchase of {self.product.name}"
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='customer', related_query_name='customer')
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=18,default='+375-25-123-45-67')
    email = models.EmailField()
    birth_date = models.DateField(default='2000-01-01')
    city = models.CharField(max_length=100, default='Unknown')
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.username

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
#     quantity = models.PositiveIntegerField()

#     def __str__(self):
#         return f"{self.product.name} x {self.quantity}"
    
class Promo(models.Model):
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField(null=True, blank=True)
    discount_value = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def __str__(self):
        return self.code

    class Meta:
        ordering = ['-date_created']
     
class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    requirements = models.TextField()
    job_type = models.CharField(max_length=50, choices=[
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ])

    def __str__(self):
        return self.title

class News(models.Model):
    title = models.CharField(max_length=100)
    short_description = models.TextField()
    description = models.TextField()
    photo = models.ImageField(default='news_photos/default_photo.png', upload_to='news_photos/', blank=True)

    def __str__(self):
        return self.title
    class Meta:
        get_latest_by = 'id'


class Question(models.Model):
    question = models.TextField()
    answer = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class Feedback(models.Model):
    author = models.ForeignKey(User, related_name='feedbacks', on_delete=models.CASCADE)
    note = models.PositiveIntegerField()
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.author.username} on {self.date.strftime('%Y-%m-%d')}"  
    
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=18,default='+375-25-111-11-11')
    birth_date = models.DateField(default='2000-01-01')
    
    def __str__(self):
        return self.user.username
    
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

# class Profile(models.Model):
#     USER_TYPES = [
#         ('employee', 'Employee'),
#         ('client', 'Client'),
#     ]
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     user_type = models.CharField(max_length=20, choices=USER_TYPES)

#     def __str__(self):
#         return self.user.username
class Contact(models.Model):
    employee_name = models.CharField(max_length=100)
    description = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    photo = models.ImageField(default='contact_photos/default_photo.png',upload_to='contact_photos/',blank=True)

    def __str__(self):
        return self.employee_name
 