from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from coreapp.forms import UserForm, MealForm, RestaurantForm, AccountForm, CategoryForm, LoginUserForm, GeoJsonFileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import (
    AuthenticationForm,
)

from .models import Meal, Order, Customer, GeoJsonFile, Restaurant, RestaurantMeal
from django.db.models import Sum, Count, Case, When
from django.core.mail import EmailMessage

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

class LoginUser(LoginView):
    form_class = LoginUserForm

    def get_success_url(self):
        # Определите URL на основе условий
        if hasattr(self.request.user, 'driver'):
            return reverse_lazy('restaurant_driver')  # Имя URL для водителя
        else:
            return reverse_lazy('restaurant_home')

def home(request):
    return redirect(restaurant_home)

@login_required(login_url='/restaurant/sign_in/')
def restaurant_home(request):
    return render(request, 'restaurant/home.html', {})

@login_required(login_url='/restaurant/sign_in/')
def restaurant_driver(request):
    return render(request, 'restaurant/driver.html', {})

def restaurant_sign_up(request):
    user_form = UserForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
        
            email = EmailMessage('Subject', 'Body', to=[new_user.email])
            email.send()

            return redirect(restaurant_home)

    return render(request, 'restaurant/sign_up.html', { 
        'user_form': user_form,
    })

@login_required(login_url='/restaurant/sign_in/')
def restaurant_account(request):
    if request.method == "POST":
        account_form = AccountForm(request.POST, instance=request.user)
        restaurant_form = RestaurantForm(request.POST, request.FILES, instance=request.user.restaurant)

        if account_form.is_valid() and restaurant_form.is_valid():
            account_form.save()
            restaurant_form.save()

    account_form = AccountForm(instance=request.user)
    restaurant_form = RestaurantForm(instance=request.user.restaurant)  
    
    return render(request, 'restaurant/account.html', { 
        'account_form': account_form,
        'restaurant_form': restaurant_form
    })


@login_required(login_url='/restaurant/sign_in/')
def restaurant_meal(request):
    restaurant = request.user.restaurant
    restaurant_meals = RestaurantMeal.objects.filter(restaurant=restaurant).select_related('meal').order_by('-id')
    meals_data = []
    for restaurant_meal in restaurant_meals:
        meal_data = {
            'meal': restaurant_meal.meal,
            'price': restaurant_meal.price,
            'is_available': restaurant_meal.is_available,
        }
        meals_data.append(meal_data)

    meals_without_price = Meal.objects.exclude(restaurantmeal__restaurant=restaurant)

    return render(request, 'restaurant/meal.html', {
        'meals': meals_data,
        'meals_without_price': meals_without_price
    })

@require_POST
@csrf_exempt
def toggle_meal_availability(request):
    meal_id = request.POST.get('meal_id')
    is_available = request.POST.get('is_available') == 'true'
    restaurant = request.user.restaurant
    
    meal = get_object_or_404(Meal, id=meal_id)
    restaurant_meal, created = RestaurantMeal.objects.get_or_create(
        restaurant=restaurant,
        meal=meal
    )

    try:
        restaurant_meal.is_available = is_available
        restaurant_meal.save()
        return JsonResponse({'success': True})
    except Meal.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Meal not found'}, status=404)


@login_required(login_url='/restaurant/sign_in/')
def restaurant_add_meal(request):
    restaurant = request.user.restaurant

    if request.method == "POST":
        meal_form = MealForm(request.POST, request.FILES)

        if meal_form.is_valid():
            meal = meal_form.save(commit=False)
            meal.restaurant = restaurant
            meal.save()
            price = meal.price
            RestaurantMeal.objects.create(
                meal=meal,
                restaurant=restaurant,
                price=price
            )
            return redirect(restaurant_meal)

    # Получаем все блюда, которым ещё не добавили цену для текущего ресторана
    meals_without_price = Meal.objects.exclude(restaurantmeal__restaurant=restaurant)

    meal_form = MealForm()
    return render(request, 'restaurant/add_meal.html', {
        'meal_form': meal_form,
        'meals_without_price': meals_without_price
    })

@login_required(login_url='/restaurant/sign_in/')
def restaurant_edit_meal(request, meal_id):
    restaurant = request.user.restaurant
    
    meal = get_object_or_404(Meal, id=meal_id)
    restaurant_meal, created = RestaurantMeal.objects.get_or_create(
        restaurant=restaurant,
        meal=meal
    )

    if request.method == "POST":
        meal_form = MealForm(request.POST, request.FILES, instance=Meal.objects.get(id=meal_id))

        if meal_form.is_valid():
            meal_form.save()

            price = meal.price
            restaurant_meal.price = price
            restaurant_meal.save()
            return redirect('restaurant_meal')

    meals_without_price = Meal.objects.exclude(restaurantmeal__restaurant=restaurant).exclude(id=meal_id)

    meal_form = MealForm(instance=meal)
    return render(request, 'restaurant/edit_meal.html', {
        'meal_form': meal_form,
        'meals_without_price': meals_without_price
    })

@login_required(login_url='/restaurant/sign_in/')
def restaurant_order(request):
    if request.method == "POST":
        order = Order.objects.get(id=request.POST['id'])

        category_form = CategoryForm(request.POST, request.FILES, instance=order)

        if category_form.is_valid():
            retOrder = category_form.save(commit=False)
            order.status = retOrder.status
            order.save()

    orders = Order.objects.filter(restaurant = request.user.restaurant).order_by('-id')
    category_form = CategoryForm()
    return render(request, 'restaurant/order.html', {
        'orders': orders,
        'category_form': category_form
    })

@login_required(login_url='/restaurant/sign_in/')
def restaurant_map(request):
    geoFile = GeoJsonFile.objects.last()

    if request.method == 'POST':
        form = GeoJsonFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('restaurant_map')
        else: 
            return render(request, 'restaurant/map.html', {
                'form':form,
                'geoFile': geoFile,
                'restaurantName': request.user.restaurant.name,
            })

    form = GeoJsonFileForm()

    return render(request, 'restaurant/map.html', {
        'form':form,
        'geoFile': geoFile,
        'restaurantName': request.user.restaurant.name,
    })

@login_required(login_url='/restaurant/sign_in/')
def restaurant_report(request):
    from datetime import datetime, timedelta 

    # Calculate the weeldays 

    revenue = []
    orders = []
    today = datetime.now()
    current_weekdays = [today + timedelta(days = i) for i in range(0 - today.weekday(), 7 - today.weekday())]

    for day in current_weekdays:
        delivered_orders = Order.objects.filter(
            restaurant = request.user.restaurant, 
            status = Order.DELIVERED, 
            created_at__year = day.year, 
            created_at__month = day.month, 
            created_at__day = day.day, 
        )

        revenue.append(sum(order.total for order in delivered_orders))
        orders.append(delivered_orders.count())

    # Getting Top 3 Meals

    top3_meals = Meal.objects.filter(restaurants__in=[request.user.restaurant])\
        .annotate(total_order = Sum('orderdetails__quantity'))\
        .order_by('-total_order')[:3]

    meal = {
        'labels': [meal.name for meal in top3_meals], 
        'data': [meal.total_order or 0 for meal in top3_meals]
    }

    # Getting Top 3 Customers 
    top3_customers = Customer.objects.annotate(
        total_order = Count(
            Case(
                When(order__restaurant = request.user.restaurant, then = 1)
            )
        )
    ).order_by('-total_order')[:3]

    customer = {
        'labels': [d.user.get_full_name() for d in top3_customers], 
        'data': [d.total_order for d in top3_customers]
    }


    return render(request, 'restaurant/report.html', {
        'revenue': revenue, 
        'orders': orders, 
        'meal': meal, 
        'customer': customer, 
    })
