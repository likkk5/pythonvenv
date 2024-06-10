from .views.views import product_list
from django.urls import path

urlpatterns = [
    # path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='login'),
    # path('logout/', views.user_logout, name='logout'),
    # path('profile/', views.profile, name='profile'),
    # path('', views.public_dashboard, name='public_dashboard'),
]
urlpatterns = [
    path('products/', product_list, name='product_list'),
]
from Autosalon.views import views,customers,admins,employees,Autosalon

urlpatterns = [
    path('',Autosalon.home,name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('about/', views.about, name='about'),
    path('policy/',views.policy,name='policy'),
    path('vacancies/',views.vacancies,name='vacancies'),
    path('index/',views.index,name='index'),
    path('questions/',views.questions,name='questions'),
    path('promos/',views.promos,name='promos'),
    path('news/',views.news,name='news'),
    path('feedbacks/',views.feedbacks,name='feedbacks'),

    path('admin_home/home/', admins.AdminHome, name='admin_home'),

    path('add/product', admins.add_product, name='add_product'),
    path('products/', admins.view_products, name='view_products'),
    path('products/<int:product_id>/edit/', admins.edit_product, name='edit_product'),
    path('products/<int:product_id>/delete/', admins.delete_product, name='delete_product'),
    path('filter_product',admins.filter_products,name='filter_products'),
    path('view_most_demand_product',admins.view_most_demand_product,name='view_most_demand_product'),

    path('add_manufacturer/', admins.add_manufacturer, name='add_manufacturer'),
    path('manufacturers/', admins.view_manufacturers, name='view_manufacturers'),
    path('edit_manufacturer/<int:manufacturer_id>/edit/', admins.edit_manufacturer, name='edit_manufacturer'),

    path('search_product/', admins.search_product, name='search_product'),

    path('view_sales/',admins.view_sales,name='view_sales'),
    path('view_sales_by_month/',admins.view_sales_by_month,name='view_sales_by_month'),
    path('view_annual_sales_report/',admins.view_annual_sales_report,name='view_annual_sales_report'),
    path('sales_trend_forecast/',admins.sales_trend_forecast,name='sales_trend_forecast'),
    path('view_employees/',admins.view_employees,name='view_employees'),

    path('customer/home/', customers.CustomerHome, name='customer_home'),

    path('catalog/', customers.view_catalog, name='view_catalog'),
    path('buy_product/<int:product_id>/',customers.buy_product,name='buy_product'),
    path('customer/orders/', customers.customer_orders, name='customer_orders'),
    path('leave_feedback/',customers.leave_feedback,name='leave_feedback'),
    path('edit_feedback/<int:feedback_id>/', customers.edit_feedback, name='edit_feedback'),
    # path('get_age/',customers.get_age,name='get_age'),
    path('customers_by_city/',admins.customers_by_city,name='customers_by_city'),

    path('employee/home',employees.EmployeeHome,name='employee_home'),
    path('admin_home/statistics',admins.view_statistics,name='view_statistics'),
    path('get_age/',customers.get_age,name='get_age'),
    path('get_country/',customers.get_country,name='get_country'),

]

