from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

import requests
from django.http import JsonResponse
from django.utils.timezone import get_current_timezone
from django.utils import timezone

# from ..decorators import student_required
from ..forms import  CustomerSignUpForm,OrderForm,FeedbackForm
from ..models import Customer, User,Product,Order,Sale, Feedback, Promo
from ..decorators import customer_required


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('customer_home')
    

def CustomerHome(request):
    return render(request, 'customers/customer_home.html')


# def view_pickup_points(request):
#     points = PickupPoint.objects.all()
#     return render(request, 'view_pickup_points.html', {'points': points})


def view_catalog(request):
    products = Product.objects.all()
    return render(request, 'view_products.html', {'products': products})


# @login_required
# @customer_required
# def buy_product(request, product_id):
#     auto = get_object_or_404(Product, pk=product_id)
#     customer = request.user.customer
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             quantity = form.cleaned_data['quantity']
#             product=auto
#             date_sold=datetime.now()
#             order = Order.objects.create(buyer=request.user, product=product,quantity=quantity,date_sold=date_sold)
#             #check if this sale already exists
#             existing_sale=Sale.objects.filter(product=auto)
#             if existing_sale:
#                 old_quantity = Sale.objects.get(product=auto).quantity
#                 new_quantity=old_quantity+quantity;
#                 Sale.objects.filter(product=auto).update(quantity=new_quantity)
#             else:
#                 sale=Sale.objects.create(product=product,quantity=quantity)
#             return redirect('customer_home') 
#     else:
#         form = OrderForm()
#     return render(request, 'buy_product.html', {'form': form, 'product': auto})

from decimal import Decimal

@login_required
@customer_required
def buy_product(request, product_id):
    auto = get_object_or_404(Product, pk=product_id)
    customer = request.user.customer
    available_promos = Promo.objects.filter(is_active=True, expiration_date__gte=timezone.now())

    if request.method == 'POST':
        print(request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            print(quantity)
            promo_code = form.cleaned_data.get('promo_code')
            print(promo_code)
            product = auto
            date_sold = timezone.now()

            # Применение промокода
            discount = Decimal('0') # Начальное значение скидки
            if promo_code:
                print('promo activated')
                try:
                    promo = Promo.objects.get(code=promo_code, is_active=True, expiration_date__gte=timezone.now())
                    discount = promo.discount_value
                except Promo.DoesNotExist:
                    messages.error(request, 'Invalid or expired promo code.')

            # Расчет новой цены с учетом скидки
            discounted_price = product.price * (Decimal(1) - discount)
            final_price = discounted_price * quantity
            print(final_price)

            order = Order.objects.create(
                buyer=request.user,
                product=product,
                quantity=quantity,
                date_sold=date_sold,
                price=final_price  # Используем цену с учетом скидки
            )

            # Проверка существующей продажи
            existing_sale = Sale.objects.filter(product=auto)
            if existing_sale.exists():
                old_quantity = existing_sale.first().quantity
                new_quantity = old_quantity + quantity
                existing_sale.update(quantity=new_quantity)
            else:
                Sale.objects.create(product=product, quantity=quantity)

            return redirect('customer_home')
    else:
        form = OrderForm()

    return render(request, 'buy_product.html', {
        'form': form,
        'product': auto,
        'available_promos': available_promos
    })

@login_required
@customer_required
def customer_orders(request):
    orders = Order.objects.filter(buyer=request.user)
    return render(request, 'customer_orders.html', {'orders': orders})
        

@login_required
@customer_required
def leave_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.author = request.user
            feedback.date = datetime.now()
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('customer_home')
    else:
        form = FeedbackForm()
    return render(request, 'leave_feedback.html', {'form': form})

@login_required
@customer_required
def edit_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id, author=request.user)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.date = datetime.now()  # Обновляем дату отзыва
            feedback.save()
            messages.success(request, 'Your feedback has been updated successfully!')
            return redirect('customer_home')
    else:
        form = FeedbackForm(instance=feedback)
    
    return render(request, 'edit_feedback.html', {'form': form})

def get_age(request):
    if request.method == 'GET' and 'name' in request.GET:
        name = request.GET['name']
        response = requests.get(f"https://api.agify.io?name={name}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"API response data: {data}")
            age = data.get('age')
            name = data.get('name')
            
            if age is not None and name is not None:
                print(f"Name: {name}, Age: {age}")  # Debug message
                return render(request, 'get_age.html', {'age': age, 'name': name})
            else:
                print("API response does not contain 'age' or 'name' keys.")
                return JsonResponse({'error': 'API response does not contain expected data.'})
        else:
            print(f"API request failed with status code {response.status_code}.")
            return JsonResponse({'error': f"API request failed with status code {response.status_code}."})
    else:
        return JsonResponse({'error': 'Invalid request'})


def get_country(request):
    if request.method == 'GET' and 'name' in request.GET:
        name = request.GET['name']
        response = requests.get(f"https://api.nationalize.io/?name={name}")
        data = response.json()
        name = data.get('name')
        countries = data.get('country')
        return render(request, 'get_country.html', {'countries': countries,'name':name})
    return JsonResponse({'error': 'Invalid request'})