from django.contrib import admin
from time import tzname
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from collections import defaultdict

from django.utils.timezone import get_current_timezone
import datetime
import calendar
from calendar import HTMLCalendar
import pytz

from django.db.models import Avg,Count,Sum,F
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from statistics import median, mode

from ..forms import  AdminSignUpForm,ProductForm,ManufacturerForm,ProductSearchForm
from ..models import Employee, ProductType, Manufacturer, Product, Customer, Order, User, Sale, News, Promo, Feedback, Question, Vacancy
from ..decorators import admin_required

import os
from myproject import settings



class AdminSignUpView(CreateView):
    model = User
    form_class = AdminSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('admin_home')
    

def AdminHome(request):
    tz = get_current_timezone()
    stored_date = datetime.datetime.now()
    m=stored_date.month
    y=stored_date.year
    desired_date = stored_date + tz.utcoffset(stored_date)

    ttimezone = pytz.timezone("Europe/Minsk") 
    mydt = ttimezone.localize(desired_date) 
    #timezone_name=mydt.tzname()
    #timezone_name=desired_date.tzname()
    timezone_name=desired_date.astimezone().tzinfo
    cal=HTMLCalendar().formatmonth(y,m)
    return render(request, 'admins/admin_home.html',{'date':desired_date,'calendar':cal,'timezone':timezone_name})
    

@login_required
@admin_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_home') 
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})



def view_products(request):
    products = Product.objects.all()
    return render(request, 'view_products.html', {'products': products})


@login_required
@admin_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('view_products') 
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})


@login_required
@admin_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('view_products')   

@login_required
@admin_required
def add_manufacturer(request):
    if request.method == 'POST':
        form = ManufacturerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_home')
    else:
        form = ManufacturerForm()
    return render(request, 'add_manufacturer.html', {'form': form})

@login_required
def view_manufacturers(request):
    manufacturers = Manufacturer.objects.all()
    return render(request, 'view_manufacturers.html', {'manufacturers': manufacturers})

@login_required
@admin_required
def edit_manufacturer(request, manufacturer_id):
    manufacturer = get_object_or_404(Manufacturer, id=manufacturer_id)
    if request.method == 'POST':
        form = ManufacturerForm(request.POST, instance=manufacturer)
        if form.is_valid():
            form.save()
            return redirect('view_manufacturers')
    else:
        form = ManufacturerForm(instance=manufacturer)
    return render(request, 'edit_manufacturer.html', {'form': form})


@login_required
@admin_required
def search_product(request):
    if request.method == 'GET':
        form = ProductSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            products = Product.objects.filter(name__icontains=query)
            return render(request, 'product_search_results.html', {'products': products, 'query': query})
    return render(request, 'search_product.html', {'form': ProductSearchForm()})
from decimal import Decimal

@login_required
def view_sales(request):
    sales = Sale.objects.all()
    
    # Список для хранения информации о каждой продаже
    sales_data = []

    total_revenue = 0
    for sale in sales:
        # Найти соответствующие заказы
        orders = Order.objects.filter(product=sale.product)
        total_for_product = 0

        for order in orders:
            if order.price is None:
                price = Decimal('0')  # Обработка случая, когда цена равна None
            else:
                price = order.price
            
            sale_info = {
                'product': sale.product.name,
                'quantity': order.quantity,
                'price': price,  # Используем изменённую цену из Order
                'total': price * order.quantity  # Вычисляем итоговую стоимость с учётом скидки
            }
            sales_data.append(sale_info)
            total_revenue += sale_info['total']
            total_for_product += sale_info['total']
        
        print(f"Product: {sale.product.name}, Total for product: {total_for_product}")

    # Вывод отладочной информации
    for sale in sales_data:
        print(f"Product: {sale['product']}, Quantity: {sale['quantity']}, Price: {sale['price']}, Total: {sale['total']}")

    print(f"Total revenue calculated manually: {total_revenue}")
    
    return render(request, 'view_sales.html', {'total_revenue': total_revenue, 'sales_data': sales_data})

from django.db.models.functions import TruncMonth
@login_required
def view_sales_by_month(request):
    # Группируем продажи по месяцам и типам товаров
    sales = (Order.objects
             .annotate(month=TruncMonth('date_sold'))
             .values('month', 'product__product_type__name')
             .annotate(monthly_revenue=Sum(F('quantity') * F('price')))  # Используем цену из Order
             .order_by('month', 'product__product_type__name'))

    # Форматируем данные для передачи в шаблон
    sales_by_month = {}
    for sale in sales:
        month = sale['month']
        product_type = sale['product__product_type__name']
        monthly_revenue = sale['monthly_revenue']

        if month not in sales_by_month:
            sales_by_month[month] = {}
        sales_by_month[month][product_type] = monthly_revenue

    return render(request, 'view_sales_by_month.html', {'sales_by_month': sales_by_month})
from django.db.models.functions import TruncYear
@login_required
def view_annual_sales_report(request):
    # Группируем продажи по годам
    annual_sales = (Order.objects
                    .annotate(year=TruncYear('date_sold'))
                    .values('year')
                    .annotate(annual_revenue=Sum(F('quantity') * F('price')))  # Используем цену из Order
                    .order_by('year'))

    # Форматируем данные для передачи в шаблон
    sales_by_year = {sale['year']: sale['annual_revenue'] for sale in annual_sales}

    return render(request, 'view_annual_sales_report.html', {'sales_by_year': sales_by_year})
def view_employees(request):
    employees=Employee.objects.all()
    return render(request, 'view_employees.html', {'employees': employees})

def filter_products(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'view_products.html', {'products': products})

from ..forms import CityForm

def customers_by_city(request):
    form = CityForm(request.POST or None)
    grouped_customers = {}

    if request.method == 'POST' and form.is_valid():
        city = form.cleaned_data['city']
        customers = Customer.objects.filter(city=city).select_related('user').order_by('city')
        
        if customers.exists():
            grouped_customers[city] = customers
        else:
            grouped_customers[city] = []

    return render(request, 'customers_by_city.html', {'grouped_customers': grouped_customers, 'form': form})

# @login_required
# def view_catalog(request):
#     min_sales = request.GET.get('min_sales')
#     max_sales = request.GET.get('max_sales')
#     order = request.GET.get('order', 'desc')

#     products = Product.objects.annotate(total_sales=Sum('sale__quantity'))

#     if min_sales:
#         products = products.filter(total_sales__gte=min_sales)
#     if max_sales:
#         products = products.filter(total_sales__lte=max_sales)

#     if order == 'asc':
#         products = products.order_by('total_sales')
#     else:
#         products = products.order_by('-total_sales')
        
#     return render(request, 'view_products.html', {'products': products })

# from collections import defaultdict
# @admin_required
# @login_required
# def view_catalog(request):
#     print("view_catalog function is called")
#     sales = Sale.objects.all()
#     if not sales.exists():
#         print("No sales found in the database.")  # Debug message

#     total_sales_by_product = defaultdict(int)

#     for sale in sales:
#         total_sales_by_product[sale.product.name] += sale.quantity
#     # Debug messages
#     print(f"Total sales by product: {total_sales_by_product}")
#     return render(request, 'view_products.html', {'total_sales_by_product': dict(total_sales_by_product)})
# @login_required
# @admin_required
# def view_catalog(request):
#     order = request.GET.get('order')
#     sales = Sale.objects.all()
#     if not sales.exists():
#         print("No sales found in the database.")  # Debug message

#     total_sales_by_product = defaultdict(int)

#     for sale in sales:
#         total_sales_by_product[sale.product.name] += sale.quantity

#     sorted_sales = list(total_sales_by_product.items())

#     if order == 'asc':
#         sorted_sales = sorted(sorted_sales, key=lambda x: x[1])
#     elif order == 'desc':
#         sorted_sales = sorted(sorted_sales, key=lambda x: x[1], reverse=True)

#     # Debug messages
#     print(f"Total sales by product: {total_sales_by_product}")
#     print(f"Sorted sales: {sorted_sales}")

#     return render(request, 'view_products.html', {'sorted_sales': sorted_sales, 'order': order})
@login_required
@admin_required
def view_most_demand_product(request):
    order = request.GET.get('order')
    total_sales_by_product = {}

    if order:
        orders = Order.objects.all()
        if not orders.exists():
            print("No orders found in the database.")  # Debug message
        else:
            total_sales_by_product = defaultdict(int)
            for order in orders:
                total_sales_by_product[order.product.name] += order.quantity

            # Сортируем данные по количеству продаж
            sorted_sales = sorted(total_sales_by_product.items(), key=lambda x: x[1], reverse=(order == 'desc'))
            total_sales_by_product = dict(sorted_sales)
            
            print(f"Total sales by product: {total_sales_by_product}")  # Debug message

    return render(request, 'view_most_demand_product.html', {'total_sales_by_product': total_sales_by_product, 'order': order})

from statistics import median, mode, StatisticsError
def calculate_statistics():
    orders = Order.objects.all()
    if not orders.exists():
        print("No orders found")  # Debug message
        return None

    average_sales = orders.aggregate(avg_sales=Avg('quantity'))['avg_sales']
    print(f"Average sales: {average_sales}")  # Debug message

    amounts = list(orders.values_list('quantity', flat=True))
    print(f"Sales amounts: {amounts}")  # Debug message

    if amounts:
        median_sales = median(amounts)
        try:
            mode_sales = mode(amounts)
        except StatisticsError:
            mode_sales = "No unique mode found"
    else:
        median_sales = 0
        mode_sales = "No data for mode"
    
    print(f"Median sales: {median_sales}")  # Debug message
    print(f"Mode sales: {mode_sales}")  # Debug message

    return {
        'average_sales': average_sales,
        'median_sales': median_sales,
        'mode_sales': mode_sales,
    }
    
from collections import defaultdict

def calculate_popular_product_type():
    product_types = Order.objects.values('product__product_type__name').annotate(quantity=Count('id')).order_by('-quantity')
    popular_products_with_customers = defaultdict(dict)

    for order in Order.objects.all():
        product_type_name = order.product.product_type.name
        username = order.buyer.username
        
        # Increment purchase count for the product type and customer
        popular_products_with_customers[product_type_name][username] = popular_products_with_customers[product_type_name].get(username, 0) + 1

    if product_types:
        most_popular_type = product_types[0]['product__product_type__name']
        print(f"Most popular product type: {most_popular_type}")  # Debug message
        return most_popular_type, popular_products_with_customers
    else:
        print("No product types found")  # Debug message
        return None, {}
    
def get_sales_by_product_type():
    sales_by_product_type = Order.objects.values('product__product_type__name').annotate(total_sales=Count('id')).order_by('-total_sales')
    sales_with_customers = defaultdict(list)

    for order in Order.objects.all():
        sales_with_customers[order.product.product_type.name].append(order.buyer.username)

    print(f"Sales by product type: {sales_by_product_type}")  # Debug message
    return sales_by_product_type, sales_with_customers

def sales_distribution_chart():
    sales_data, _ = get_sales_by_product_type()
    if not sales_data:
        print("No sales data found")  # Debug message
        return

    types = [sale['product__product_type__name'] for sale in sales_data]
    total_sales = [sale['total_sales'] for sale in sales_data]

    plt.figure(figsize=(8, 6))
    plt.pie(total_sales, labels=types, autopct='%1.1f%%')
    plt.title('Распределение продаж по типам товаров')
    plt.axis('equal')
    save_path = os.path.join(settings.MEDIA_ROOT, 'sales_distribution_chart.png')
    plt.savefig(save_path)
    print(f"Chart saved at: {save_path}")  # Debug message
    
@login_required
def view_statistics(request):
    statistics = calculate_statistics()
    print(f"Statistics: {statistics}")  # Debug message
    most_popular_type, popular_products_with_customers = calculate_popular_product_type()
    sales_distribution_chart()
    image_path = os.path.join(settings.MEDIA_URL, 'sales_distribution_chart.png')
    print(f"Image path: {image_path}")  # Debug message
    return render(request, 'view_statistics.html', {
        'statistics': statistics,
        'popular': most_popular_type,
        'chart_image': image_path,
        'popular_products_with_customers': dict(popular_products_with_customers)
    })
    
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

import pandas as pd
import numpy as np
import statsmodels.api as sm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models.functions import TruncMonth
from django.db.models import Sum
import io
import base64
from matplotlib.figure import Figure

@login_required
@admin_required
def sales_trend_forecast(request):
    # Загрузка и обработка данных
    orders = Order.objects.annotate(month=TruncMonth('date_sold')).values('month').annotate(total_sales=Sum('price')).order_by('month')
    
    if not orders:
        return render(request, 'sales_trend_forecast.html', {'error': 'No sales data available'})

    data = pd.DataFrame(list(orders))
    data.set_index('month', inplace=True)
    data.index = pd.to_datetime(data.index)

    # Убедимся, что total_sales является числом и заполним пропущенные значения нулями
    data['total_sales'] = pd.to_numeric(data['total_sales'], errors='coerce').fillna(0)
    data = data.asfreq('M')
    data['time'] = np.arange(len(data))

    # Проверка на пустой DataFrame после обработки
    if data.empty:
        return render(request, 'sales_trend_forecast.html', {'error': 'No valid sales data available'})

    X = sm.add_constant(data['time'])
    y = data['total_sales']

    # Проверка на отсутствие данных для построения модели
    if len(y) == 0:
        return render(request, 'sales_trend_forecast.html', {'error': 'Not enough data to build model'})

    # Построение модели линейного тренда
    model = sm.OLS(y, X).fit()
    data['trend'] = model.predict(X)

    # Прогнозирование будущих значений
    forecast_periods = 12
    future_dates = [data.index[-1] + pd.DateOffset(months=i) for i in range(1, forecast_periods + 1)]
    future_time = np.arange(len(data), len(data) + forecast_periods)
    future_data = pd.DataFrame(index=future_dates)
    future_data['time'] = future_time
    future_data['trend'] = model.predict(sm.add_constant(future_data['time']))
    forecast = pd.concat([data, future_data])

    # Построение графика
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(forecast.index, forecast['total_sales'], label='Actual Sales')
    ax.plot(forecast.index, forecast['trend'], label='Trend/Forecast', linestyle='--')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sales')
    ax.set_title('Sales Trend and Forecast')
    ax.legend()
    ax.grid(True)

    # Сохранение графика в буфер
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return render(request, 'sales_trend_forecast.html', {'chart': image_base64})
