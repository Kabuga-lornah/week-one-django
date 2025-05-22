from django.shortcuts import render, redirect, get_object_or_404

from .models import FoodItem

def food_list(request):
  
    food_items = FoodItem.objects.all()
    total_calories = sum(item.calories for item in food_items)
    context = {
        'food_items': food_items,
        'total_calories': total_calories,
        'year': 2025,  
    }
    return render(request, 'calorie_tracker/food_list.html', context)



def add_food(request):
  
    name = request.POST.get('name')
    calories = request.POST.get('calories')

    if name and calories:
        try:
            calories = int(calories)
            if calories < 0:
                raise ValueError("Calories cannot be negative")
        except ValueError:
           
            return redirect('calorie_tracker:food_list')

        FoodItem.objects.create(name=name, calories=calories)

    return redirect('calorie_tracker:food_list')



def delete_food(request, food_id):
   
    food_item = get_object_or_404(FoodItem, id=food_id)
    food_item.delete()
    return redirect('calorie_tracker:food_list')



def reset_calories(request):
   
    FoodItem.objects.all().delete()
    return redirect('calorie_tracker:food_list')

