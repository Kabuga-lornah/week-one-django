from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'calorie_tracker'

urlpatterns = [
    path('', views.food_list, name='food_list'),
    path('add/', views.add_food, name='add_food'),
    path('delete/<int:food_id>/', views.delete_food, name='delete_food'),
    path('reset/', views.reset_calories, name='reset_calories'),
    path(
    'login/',
    auth_views.LoginView.as_view(
        template_name='registration/login.html',
        next_page='calorie_tracker:food_list'
    ),
    name='login'
),

    path('logout/', auth_views.LogoutView.as_view(next_page='calorie_tracker:login'), name='logout'),
    path('signup/', views.signup, name='signup'),
]
