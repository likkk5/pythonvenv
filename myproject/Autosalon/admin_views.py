from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncYear
from .models import Customer, Product, Order
from django.http import JsonResponse
import numpy as np
from sklearn.linear_model import LinearRegression

@staff_member_required
def customers_by_city(request):
    customers = Customer.objects.values('city').annotate(total=Count('id')).order_by('city')
    return render(request, 'admin/customers_by_city.html', {'customers': customers})

@staff_member_required
def product_popularity(request):
    popular_products = Product.objects.annotate(total_sales=Sum('order_items__quantity')).order_by('-total_sales')[:5]
    unpopular_products = Product.objects.annotate(total_sales=Sum('order_items__quantity')).order_by('total_sales')[:5]
    return render(request, 'admin/product_popularity.html', {'popular_products': popular_products, 'unpopular_products': unpopular_products})

@staff_member_required
def monthly_sales_report(request):
    sales = Order.objects.annotate(month=TruncMonth('order__sale_date')).values('month', 'product__product_type__name').annotate(total_sales=Sum('quantity')).order_by('month')
    return render(request, 'admin/monthly_sales_report.html', {'sales': sales})

@staff_member_required
def annual_sales_report(request):
    sales = Order.objects.annotate(year=TruncYear('order__sale_date')).values('year').annotate(total_sales=Sum('quantity')).order_by('year')
    return render(request, 'admin/annual_sales_report.html', {'sales': sales})

@staff_member_required
def sales_summary(request):
    sales = Order.objects.annotate(month=TruncMonth('order__sale_date')).values('month').annotate(total_sales=Sum('quantity')).order_by('month')
    labels = [sale['month'].strftime('%Y-%m') for sale in sales]
    data = [sale['total_sales'] for sale in sales]
    return render(request, 'admin/sales_summary.html', {'labels': labels, 'data': data})

@staff_member_required
def predict_sales(request):
    sales = Order.objects.annotate(month=TruncMonth('order__sale_date')).values('month').annotate(total_sales=Sum('quantity')).order_by('month')
    dates = [sale['month'] for sale in sales]
    quantities = [sale['total_sales'] for sale in sales]

    X = np.array(range(len(dates))).reshape(-1, 1)
    y = np.array(quantities)

    model = LinearRegression()
    model.fit(X, y)

    next_month = len(dates)
    predicted_sales = model.predict(np.array([[next_month]]))

    return JsonResponse({'predicted_sales': predicted_sales[0]})

@staff_member_required
def sales_trend(request):
    sales = Order.objects.annotate(month=TruncMonth('order__sale_date')).values('month').annotate(total_sales=Sum('quantity')).order_by('month')
    dates = [sale['month'] for sale in sales]
    quantities = [sale['total_sales'] for sale in sales]

    return render(request, 'admin/sales_trend.html', {'dates': dates, 'quantities': quantities})
