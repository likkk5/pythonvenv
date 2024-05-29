from django.shortcuts import redirect, render
from statistics import median, mode
from django.views.generic import TemplateView
import datetime

import logging

from myproject import settings

from ..models import Product,Sale,Customer
from django.db.models import Avg,Count,Sum,F
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import os

logger = logging.getLogger(__name__)

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def calculate_statistics():
    sales = Sale.objects.all()
    if not sales.exists():
        return None

    average_sales = sales.aggregate(avg_sales=Avg('quantity'))['avg_sales']

    amounts = list(sales.values_list('quantity', flat=True))
    median_sales = median(amounts)

    return {
        'average_sales': average_sales,
        'median_sales': median_sales,
    }
    
def calculate_age_statistics():
    clients = Customer.objects.all()
    if not clients:
        return None
    current_date = datetime.date.today()
    total_years = sum((current_date - client.birth_date).days // 365 for client in clients)
    average_age = total_years / len(clients)
    
    ages = [(current_date - client.birth_date).days // 365 for client in clients]
    median_age = median(ages)
    
    return {
        'average_age': round(average_age, 2),  # Округляем до двух знаков после запятой
        'median_age': median_age,
    }


def calculate_popular_product_type():
    product_types = Sale.objects.values('product__product_type').annotate(quantity=Count('id')).order_by('-quantity')
    if not product_types:
        return None
    if product_types:
        most_popular_type = product_types[0]['product__product_type']
    else:
        most_popular_type = None
    
    return most_popular_type


def get_sales_by_product_type():
    sales_by_product_type = Sale.objects.values('product__product_type').annotate(
        total_sales=Count('id')).order_by('-total_sales')
    
    return sales_by_product_type


def sales_distribution_chart():
    sales_data = get_sales_by_product_type()
    types = [sale['product__product_type'] for sale in sales_data]
    total_sales = [sale['total_sales'] for sale in sales_data]

    plt.figure(figsize=(8, 6))
    plt.pie(total_sales, labels=types, autopct='%1.1f%%')
    plt.title('Распределение продаж по типам товаров')
    plt.axis('equal') 
    save_path = os.path.join(settings.MEDIA_ROOT, 'sales_distribution_chart.png')
    plt.savefig(save_path)



def home(request):
    
    if request.user.is_authenticated:
        if request.user.is_employee:
            return redirect('employee_home')
        if request.user.is_customer:
            return redirect('customer_home')
        if request.user.is_admin:
            return redirect('admin_home')
    return render(request, 'home.html')

