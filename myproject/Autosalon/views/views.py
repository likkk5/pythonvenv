# Create your views here.
from ..models import Product
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import Order, Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

from ..models import Vacancy,Question,Promo,News,Feedback,Employee

def contacts(request):
    employees=Employee.objects.all()
    return render(request, 'contacts.html', {'employees': employees})

def about(request):
    return render(request, 'about.html')

def policy(request):
    return render(request, 'policy.html')

def vacancies(request):
    vacancies=Vacancy.objects.all()
    return render(request,'vacancies.html',{'vacancies':vacancies})

def index(request):
    latest_news = News.objects.latest('id')  # Assuming 'id' is the primary key and higher id means newer news
    context = {
        'latest_news': latest_news,
    }
    return render(request, 'index.html', context)

def questions(request):
    questions=Question.objects.all()
    return render(request,'questions.html',{'questions':questions})

def promos(request):
    active_promo_codes = Promo.objects.filter(is_active=True)
    archived_promo_codes = Promo.objects.filter(is_active=False)

    context = {
        'active_promo_codes': active_promo_codes,
        'archived_promo_codes': archived_promo_codes,
    }

    return render(request, 'promos.html', context)


def news(request):
    news = News.objects.all()
    return render(request, 'news.html', {'news': news})

def feedbacks(request):
    feedbacks=Feedback.objects.all()
    return render(request,'feedbacks.html',{'feedbacks':feedbacks})


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('profile')
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/register.html', {'form': form})

# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('profile')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'registration/login.html', {'form': form})

# def user_logout(request):
#     logout(request)
#     return redirect('login')

# @login_required
# def profile(request):
#     return render(request, 'profile.html')

# def public_dashboard(request):
#     form = ProductFilterForm(request.GET or None)
#     products = Product.objects.all()

#     if form.is_valid():
#         if form.cleaned_data['price_min']:
#             products = products.filter(price__gte=form.cleaned_data['price_min'])
#         if form.cleaned_data['price_max']:
#             products = products.filter(price__lte=form.cleaned_data['price_max'])
#         if form.cleaned_data['product_type']:
#             products = products.filter(product_type=form.cleaned_data['product_type'])

#     return render(request, 'public_dashboard.html', {'form': form, 'products': products})

# @login_required
# def personal_dashboard(request):
#     user = request.user
#     profile = Profile.objects.get(user=user)

#     if profile.user_type == 'employee':
#         orders = Order.objects.filter(customer=user)
#         return render(request, 'employee_dashboard.html', {'user': user, 'orders': orders})
#     elif profile.user_type == 'client':
#         products = Product.objects.all()  
#         promos = Promo.objects.filter(user=user)
#         return render(request, 'client_dashboard.html', {'user': user, 'products': products, 'promos': promos})
#     else:
#         return render(request, 'error.html', {'message': 'User type is not defined'})
