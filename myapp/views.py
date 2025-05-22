from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from .models import FoodItem


class LogoutGetAllowedView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required
def food_list(request):
    food_items = FoodItem.objects.filter(user=request.user)
    total_calories = sum(item.calories for item in food_items)
    context = {
        'food_items': food_items,
        'total_calories': total_calories,
        'year': 2025,
    }
    return render(request, 'calorie_tracker/food_list.html', context)

@login_required
def add_food(request):
    if request.method == "POST":
        name = request.POST.get('name')
        calories = request.POST.get('calories')

        if name and calories:
            try:
                calories = int(calories)
                if calories < 0:
                    raise ValueError("Calories cannot be negative")
                FoodItem.objects.create(name=name, calories=calories, user=request.user)
            except ValueError:
                pass
    return redirect('calorie_tracker:food_list')

@login_required
def delete_food(request, food_id):
    food_item = get_object_or_404(FoodItem, id=food_id, user=request.user)
    food_item.delete()
    return redirect('calorie_tracker:food_list')

@login_required
def reset_calories(request):
    FoodItem.objects.filter(user=request.user).delete()
    return redirect('calorie_tracker:food_list')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
           
            return redirect('calorie_tracker:login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
