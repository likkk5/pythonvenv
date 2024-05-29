from django.urls import path
from .admin_views import customers_by_city, product_popularity, monthly_sales_report, annual_sales_report, sales_summary, predict_sales, sales_trend

urlpatterns = [
    path('customers_by_city/', customers_by_city, name='customers_by_city'),
    path('product_popularity/', product_popularity, name='product_popularity'),
    path('monthly_sales_report/', monthly_sales_report, name='monthly_sales_report'),
    path('annual_sales_report/', annual_sales_report, name='annual_sales_report'),
    path('sales_summary/', sales_summary, name='sales_summary'),
    path('predict_sales/', predict_sales, name='predict_sales'),
    path('sales_trend/', sales_trend, name='sales_trend'),
]